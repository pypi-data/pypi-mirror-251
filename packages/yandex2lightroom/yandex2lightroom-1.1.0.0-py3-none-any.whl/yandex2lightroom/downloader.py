import itertools
import json
import logging
import os
import pathlib
import time
import urllib
from dataclasses import dataclass
from math import floor
from typing import List, Union, Optional
from urllib.parse import urlparse, urlencode

import requests
from bs4 import BeautifulSoup
from dataclasses_json import dataclass_json
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .exiftool import ExifTool
import sys

Driver = Union[webdriver.Chrome, webdriver.Edge, webdriver.Firefox, webdriver.Safari]

DRIVER_NAME_TO_CLASS = {
    'Chrome': webdriver.Chrome,
    'Edge': webdriver.Edge,
    'Firefox': webdriver.Firefox,
    'Safari': webdriver.Safari,
}  # type Dict[str, Driver]


def get_driver(name: str, path: Optional[str], show_browser: Optional[bool]) -> Driver:
    driver_class = DRIVER_NAME_TO_CLASS[name]
    service = Service(executable_path=path) if path else None
    if driver_class == DRIVER_NAME_TO_CLASS['Chrome']:
        option = webdriver.ChromeOptions()
        if not show_browser:
            option.add_argument('headless')
        args = {'service': service, 'chrome_options': option} if path else {'chrome_options': option}
    else:
        args = {}

    return driver_class(**args)


#####
@dataclass_json
@dataclass
class ImgUrlResult:
    status: str
    message: str
    img_url: str
    img_path: str


@dataclass_json
@dataclass
class PageResult:
    status: str
    message: str
    page: int
    errors_count: int
    skipped_count: int
    img_url_results: List[ImgUrlResult]


@dataclass_json
@dataclass
class KeywordResult:
    status: str
    message: str
    keyword: str
    errors_count: int
    skipped_count: int
    page_results: List[PageResult]


@dataclass_json
@dataclass
class DownloaderResult:
    status: str
    message: str
    keyword_results: List[KeywordResult]


def save_json(args, downloader_result: DownloaderResult):
    downloader_result_json = downloader_result.to_dict()  # pylint: disable=no-member
    json_path = pathlib.Path(args.output_directory) / pathlib.Path(args.json)
    pretty_json = json.dumps(downloader_result_json,
                             indent=4,
                             ensure_ascii=False)
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(pretty_json)
        f.close()
    logging.info(f"Result information saved: {json_path}.")


#####


def filepath_fix_existing(directory_path: pathlib.Path, name: str,
                          filepath: pathlib.Path) -> pathlib.Path:
    """Expands name portion of filepath with numeric "(x)" suffix.
    """
    new_filepath = filepath
    if filepath.exists():
        for i in itertools.count(start=1):
            new_name = f'{name} ({i}){filepath.suffix}'
            new_filepath = directory_path / new_name
            if not new_filepath.exists():
                break

    return new_filepath


def download_single_image(img_url: str,
                          output_directory: pathlib.Path,
                          sub_directory: str = "",
                          multiproccess=False,
                          keyword: str = "",
                          skip_existing=False) -> ImgUrlResult:
    img_url_result = ImgUrlResult(status="",
                                  message="",
                                  img_url=img_url,
                                  img_path="")

    debug = False
    if debug:
        img_url_result.status = "planned"
        img_url_result.message = "download omitted"
        return img_url_result

    # log_file = os.path.join(output_directory, 'yandex2lightroom.log')
    # logging.basicConfig(filename=log_file, level=logging.INFO,
    #                    format="%(asctime)s %(levelname)-8s %(message)s", datefmt='%Y-%m-%d %H:%M:%S')

    img_extensions = (".jpg", ".jpeg", ".jfif", "jpe", ".gif", ".png", ".bmp",
                      ".svg", ".webp", ".ico")
    content_type_to_ext = {
        "image/gif": ".gif",
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/svg+xml": ".svg",
        "image/x-icon": ".ico"
    }

    try:
        logging.info(f"Download image '{img_url}'")
        response = requests.get(img_url, timeout=10)

        data = response.content
        content_type = response.headers["Content-Type"]

        if response.ok:
            logging.info("Response ok")

            img_name = pathlib.Path(urlparse(img_url).path).name
            img_host = pathlib.Path(urlparse(img_url).hostname).name

            # print("Image: " + img_name)

            img_name = img_name[:YandexImagesDownloader.MAXIMUM_FILENAME_LENGTH]

            directory_path = output_directory / sub_directory / img_host
            directory_path.mkdir(parents=True, exist_ok=True)

            if multiproccess:
                img_name = f"[{os.getpid()}] {img_name}"

            img_path = directory_path / img_name
            if not any(img_path.name.endswith(ext) for ext in img_extensions):
                img_path = img_path.with_suffix(
                    content_type_to_ext[content_type])

            if img_path.exists() and skip_existing:
                img_url_result.status = "skipped"
                img_url_result.message = "Skipped image download."
                img_url_result.img_path = str(img_path)
            else:
                img_path = filepath_fix_existing(directory_path, img_name, img_path)
                with open(img_path, "wb") as f:
                    f.write(data)
                    f.close()
                    exiftool = ExifTool(img_path)
                    if not exiftool.set_creator_work_url(img_url):
                        sys.exit(-1)
                    if not exiftool.set_keywords(keyword):
                        sys.exit(-1)

                img_url_result.status = "success"
                img_url_result.message = "Downloaded the image."
                img_url_result.img_path = str(img_path)
        else:
            logging.info(f"Response {response}")
            logging.info(f"Image could not be downloaded.")
            img_url_result.status = "fail"
            img_url_result.message = (f"img_url response is not ok."
                                      f" response: {response}.")

    except (KeyboardInterrupt, SystemExit):
        raise

    except (requests.exceptions.SSLError,
            requests.exceptions.ConnectionError) as e:
        img_url_result.status = "fail"
        img_url_result.message = f"{type(e)}"

    except Exception as exception:
        img_url_result.status = "fail"
        img_url_result.message = (f"Something is wrong here.",
                                  f" Error: {type(exception), exception}")

    if img_url_result.status == "fail":
        logging.info(f"    fail: {img_url} error: {img_url_result.message}")
    else:
        logging.info(f"    {img_url_result.message} ==> {img_url_result.img_path}")

    return img_url_result


#####


class YandexImagesDownloader:
    """Class to download images from yandex.ru
    """

    MAIN_URL = "https://yandex.com/images/search"
    MAXIMUM_PAGES_PER_SEARCH = 51
    MAXIMUM_IMAGES_PER_PAGE = 30
    MAXIMUM_FILENAME_LENGTH = 50

    def __init__(self,
                 driver: Driver,
                 output_directory="download/",
                 limit=100,
                 isize=None,
                 exact_isize=None,
                 iorient=None,
                 extension=None,
                 color=None,
                 itype=None,
                 commercial=None,
                 recent=None,
                 pool=None,
                 skip_existing=False,
                 show_browser=False,
                 delay_for_refresh=2,
                 delay_for_captcha_handling=30,
                 wait_for_captcha_handling=False):
        self.driver = driver
        self.output_directory = pathlib.Path(output_directory)
        self.limit = limit
        self.isize = isize
        self.exact_isize = exact_isize
        self.iorient = iorient
        self.extension = extension
        self.color = color
        self.itype = itype
        self.commercial = commercial
        self.recent = recent
        self.skip_existing = skip_existing
        self.show_browser = show_browser
        self.delay_for_refresh = delay_for_refresh
        self.delay_for_captcha_handling = delay_for_captcha_handling
        self.wait_for_captcha_handling = wait_for_captcha_handling

        self.url_params = self.init_url_params()
        self.requests_headers = {
            'User-Agent':
                ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML,"
                 " like Gecko) Chrome/41.0.2228.0 Safari/537.36")
        }
        self.cookies = {}
        self.pool = pool

        logging.info(f'Output directory is set to "{self.output_directory}/"')
        logging.info(f"Limit of images is set to {self.limit}")
        if self.skip_existing:
            logging.info(f"Existing images will be skipped.")

    def get_response(self):
        urls = [request.url for request in self.driver.requests]
        request = self.driver.requests[urls.index(self.driver.current_url)]
        return request.response

    def init_url_params(self):
        params = {
            "nomisspell": 1,
            "isize": self.isize,
            "wp": None,
            "iw": None,
            "ih": None,
            "iorient": self.iorient,
            "type": self.extension,
            "color": self.color,
            "itype": self.itype,
            "commercial": self.commercial,
            "recent": self.recent
        }

        if self.exact_isize:
            width, height = self.exact_isize
            params["isize"] = "eq"
            params["iw"] = width
            params["ih"] = height

        if self.isize == "wallpaper":
            params["wp"] = "wh16x10_2560x1600"
        return params

    def get_url_params(self, page, text):
        params = {"p": page, "text": text}
        params.update(self.url_params)

        return params

    def count_available_images(self):
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        image_cover_list = soup.find_all("a", class_="Link SimpleImage-Cover")
        if not image_cover_list:
            return 0
        else:
            return len(image_cover_list)

    def wait_for_images(self):
        logging.info("wait_for_images() start")
        images_available = self.count_available_images()
        logging.info(f"available={images_available} limit={self.limit}")
        last_images_available = 0
        while images_available < self.limit:
            if last_images_available == images_available:
                break
            last_images_available = images_available

            # Get scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")

            while True:
                # Scroll down to bottom
                logging.info("scroll down and wait")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(self.delay_for_refresh)
                images_available = self.count_available_images()
                logging.info(f"available={images_available} limit={self.limit}")
                if images_available >= self.limit:
                    break

                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                logging.info(f"last_height={last_height}")
                logging.info(f"new_height={new_height}")
                if new_height == last_height:
                    # Show more results
                    logging.info("End of page reached")
                    logging.info("Show more images")
                    self.driver.find_element(By.XPATH, "//div[@class='SerpList-LoadContent']/button").click()
                    time.sleep(self.delay_for_refresh)
                    images_available = self.count_available_images()
                else:
                    last_height = new_height

                if last_images_available == images_available:
                    logging.info("No more images found. Break.")
                    break
                else:
                    last_images_available = images_available

        logging.info("wait_for_images() end")

    def download_images_by_keyword(self, keyword, isize,
                                   sub_directory="") -> KeywordResult:
        keyword_result = KeywordResult(status="",
                                       message="",
                                       keyword=keyword,
                                       errors_count=0,
                                       skipped_count=0,
                                       page_results=[])

        if isize == "wallpaper":
            self.check_captcha_and_get(YandexImagesDownloader.MAIN_URL,
                                       params={
                                           'text': keyword,
                                           'isize': isize,
                                           'wp': "wh16x10_2560x1600",
                                           "nomisspell": 1
                                       })
        else:
            self.check_captcha_and_get(YandexImagesDownloader.MAIN_URL,
                                   params={
                                       'text': keyword,
                                       'isize': isize,
                                       "nomisspell": 1
                                   })
        response = self.get_response()

        if response.status_code != 200:
            keyword_result.status = "fail"
            keyword_result.message = (
                "Failed to fetch a search page."
                f" url: {YandexImagesDownloader.MAIN_URL},"
                f" params: {{'text': {keyword}}},"
                f" status_code: {response.status_code}")
            return keyword_result

        self.wait_for_images()

        soup = BeautifulSoup(self.driver.page_source, "lxml")
        image_cover_list = soup.find_all("a", class_="Link SimpleImage-Cover")

        if not image_cover_list:
            keyword_result.status = "success"
            keyword_result.message = f"No images with keyword {keyword} found."
            keyword_result.errors_count = 0
            return keyword_result

        image_urls = []
        count = 0
        for item in image_cover_list:
            if count >= self.limit:
                break
            href = urllib.parse.unquote(item.attrs["href"])
            logging.info(f"href={href}")
            for value in href.split("&"):
                if value.startswith("img_url="):
                    url_img = value[8:]
                    image_urls.append(url_img)
                    logging.info(f"url_img={url_img}")
                    count = count + 1

        logging.info(f"Found at least {len(image_urls)} images for download.")

        errors_count = 0
        skipped_count = 0
        image_count = 0

        page_result = PageResult(status="",
                                 message="",
                                 page=0,
                                 errors_count=0,
                                 skipped_count=0,
                                 img_url_results=[])

        for image_url in image_urls:

            if image_count >= self.limit:
                break

            if self.pool:
                img_url_result = self.pool.apply_async(
                    download_single_image,
                    args=(image_url, self.output_directory, sub_directory, False, keyword, self.skip_existing))
            else:
                img_url_result = download_single_image(image_url,
                                                       self.output_directory,
                                                       sub_directory,
                                                       skip_existing=self.skip_existing,
                                                       keyword=keyword)

            page_result.img_url_results.append(img_url_result)

            image_count += 1

        if self.pool:
            for i, img_url_result in enumerate(page_result.img_url_results):
                page_result.img_url_results[i] = img_url_result.get()
        errors_count += sum(1 if page_result.status == "fail" else 0
                            for page_result in page_result.img_url_results)
        skipped_count += sum(1 if page_result.status == "skipped" else 0
                             for page_result in page_result.img_url_results)

        keyword_result.status = "success"
        keyword_result.message = f"Images for keywords '{keyword}' downloaded"
        keyword_result.errors_count = errors_count
        keyword_result.skipped_count = skipped_count

        return keyword_result

    def download_images(self, keywords: List[str], isize) -> DownloaderResult:
        downloader_result = DownloaderResult(status="",
                                             message="",
                                             keyword_results=[])

        downloader_result.status = "fail"

        for keyword in keywords:
            logging.info(f"Downloading images for {keyword}...")

            keyword_result = self.download_images_by_keyword(
                keyword, isize, sub_directory=keyword)
            downloader_result.keyword_results.append(keyword_result)

            logging.info(keyword_result.message)

        downloader_result.status = "success"
        downloader_result.message = "Everything is downloaded!"

        return downloader_result

    class StopCaptchaInput(Exception):
        pass

    def check_captcha_and_get(self, url, params=None):
        """Checking for captcha on url and get url after that.
        If there is captcha, you have to type it in input() or quit."""

        url_with_params = f"{url}?{urlencode(params)}"

        del self.driver.requests
        logging.info("Get URL: " + url_with_params)
        self.driver.get(url_with_params)

        if self.wait_for_captcha_handling:
            logging.info(f"Wait {self.delay_for_captcha_handling} seconds for captcha handling.")
            time.sleep(self.delay_for_captcha_handling)
        else:
            logging.info("Looking for cookies button.")
            x_path = f"//div[@class='gdpr-popup-v3-button gdpr-popup-v3-button_id_all']"
            try:
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(
                    (By.XPATH, x_path))).click()
                logging.info("Cookies button was pushed.")
            except Exception as e:
                logging.error(f"Cookie handling failed. {e}")
                logging.info("Expect captcha request.")
                logging.info(f"Wait {self.delay_for_captcha_handling} seconds for captcha handling.")
