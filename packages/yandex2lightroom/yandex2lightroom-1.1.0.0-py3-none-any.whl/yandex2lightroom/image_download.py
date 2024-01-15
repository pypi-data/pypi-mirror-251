import os
import time
import logging
import pathlib
import sys

from multiprocessing import Pool
from .downloader import YandexImagesDownloader, get_driver, download_single_image, save_json
from .parse import parse_args


def scrap(args):
    keywords = []

    if args.keywords:
        keywords.extend([
            str(item).strip() for item in args.keywords.split(",") if len(item)
        ])

    if args.keywords_from_file:
        with open(args.keywords_from_file, "r") as f:
            keywords.extend([line.strip() for line in f])

    driver = get_driver(args.browser, args.driver_path, args.show_browser)

    try:
        pool = Pool(args.num_workers) if args.num_workers else None

        downloader = YandexImagesDownloader(driver, args.output_directory,
                                            args.limit, args.isize,
                                            args.exact_isize, args.iorient,
                                            args.extension, args.color,
                                            args.itype, args.commercial,
                                            args.recent, pool, args.skip_existing, args.show_browser,
                                            args.delay_for_refresh, args.delay_for_captcha_handling,
                                            args.wait_for_captcha_handling)

        start_time = time.time()
        total_errors = 0
        total_skipped = 0

        if keywords:
            downloader_result = downloader.download_images(keywords, args.isize)
            total_errors += sum(
                keyword_result.errors_count
                for keyword_result in downloader_result.keyword_results)
            total_skipped += sum(
                keyword_result.skipped_count
                for keyword_result in downloader_result.keyword_results)
    finally:
        driver.quit()
        if args.num_workers:
            pool.close()
            pool.join()

    if args.single_image:
        img_url_result = download_single_image(
            args.single_image, pathlib.Path(args.output_directory))
        total_errors += 1 if img_url_result.status == "fail" else 0

    total_time = time.time() - start_time

    logging.info("Download completed.")
    logging.info(f"Total errors: {total_errors}")
    logging.info(f"Total skipped: {total_skipped}")
    logging.info(
        f"Total files downloaded: {len(keywords) * args.limit - total_errors - total_skipped}")
    logging.info(f"Total time taken: {total_time} seconds.")
    if keywords and args.json:
        save_json(args, downloader_result)


def setup_logging(quiet_mode, output_directory):
    log_file = os.path.join(output_directory, 'yandex2lightroom.log')
    logging.basicConfig(filename=log_file, level=logging.WARNING if quiet_mode else logging.INFO,
                        format="%(asctime)s %(levelname)-8s %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    selenium_logger = logging.getLogger('seleniumwire')
    selenium_logger.setLevel(logging.WARNING)


def main(arguments=None):
    try:
        args = parse_args(arguments)
        if args.output_directory[0] != "/" and args.output_directory[1] != ":":
            # output_directory is relative path
            home_directory = os.path.expanduser('~')
            args.output_directory = os.path.join(home_directory, args.output_directory)
        setup_logging(args.quiet_mode, args.output_directory)
        logging.info(f"arg: show_browser={args.show_browser}")
        scrap(args)

    except KeyboardInterrupt as e:
        errlog = args.error_log
        if errlog:
            with open(errlog, "w") as f:
                f.write(e.msg)
        logging.error("KeyboardInterrupt")
        sys.exit(1)

    except Exception as e:
        errlog = args.error_log
        if errlog:
            with open(errlog, "w") as f:
                f.write(str(e))

        logging.error(e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
