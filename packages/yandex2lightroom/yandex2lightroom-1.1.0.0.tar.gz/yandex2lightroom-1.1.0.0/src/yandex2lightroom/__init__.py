from __future__ import absolute_import
import sys


def run_main():
    from yandex2lightroom.image_download import main
    args = None
    if len(sys.argv) == 1:
        args = ["Firefox", "-k", "New Topographics", "-l", "5"]
    main(args)


if __name__ == '__main__':
    run_main()
