"""
Middle Variant of Program. Something average between usability and robustness.
"""

import argparse  # <-- imports in alphabetical order
import validators
import logging
import os
import pathlib
import requests


class Downloader:

    def __init__(self, store_path=None, logger=None):
        self.current_dir = pathlib.Path(__file__).resolve().parent
        self.log_file_path = pathlib.Path(self.current_dir, "result.log")
        self.logger = logger
        if not self.logger:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
                handlers=[
                    logging.FileHandler(self.log_file_path),
                    logging.StreamHandler()
                ])
            self.logger = logging.getLogger()

        self.store_path = store_path
        if not self.store_path:
            self.store_path = pathlib.Path(self.current_dir, "storage")
            if not self.store_path.exists():
                os.mkdir(self.store_path)

    def validate_url(self, url: str) -> True:
        try:
            res = validators.url(url)
        except Exception as e:
            self.logger.log(logging.INFO, "failed validate URL '{0}': '{1}'".format(url, e))
            return False

        if not type(res) == bool:
            self.logger.log(logging.INFO, "failed verify validation: '{0}'".format(res))
            return False

        return res

    def store_response(self, response: requests.Response, file_path: pathlib.Path):
        try:
            with file_path.open(mode='wb') as f:
                for chunk in response.iter_content(chunk_size=8196):
                    f.write(chunk)
        except Exception as e:
            self.logger.log(logging.INFO, "failed store '{0}': '{1}'".format(response.url, e))

    def run(self):
        user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/70.0.3538.102 Safari/537.36'}

        # Instantiate the parser
        parser = argparse.ArgumentParser(description='Middle Variant of Program')
        parser.add_argument('--url_file', type=str, default="", required=True, help='Absolute path to file with URLs')
        args = parser.parse_args()

        if not args.url_file:
            logging.log(logging.INFO, 'URL file is not provided')
            return

        url_file_path = pathlib.Path(args.url_file)
        if not url_file_path.exists():
            logging.log(logging.INFO, 'URL file does not exists')
            return

        logging.log(logging.INFO, "File size: {0}".format(url_file_path.stat().st_size))

        with url_file_path.open(mode='r', buffering=1024, errors='strict', newline='\n') as url_file:
            counter = 0
            for file_line in url_file:
                raw_url = file_line.rstrip('\r').rstrip('\r\n')

                logging.log(logging.INFO, raw_url)
                if not self.validate_url(raw_url):
                    logging.log(logging.INFO, "Skip: '{0}'".format(raw_url))
                    continue

                response = requests.get(raw_url, headers=user_agent)
                file_name = "{0}".format(counter - 1)  # adjust file name to match line number in URLs file
                store_file_path = pathlib.Path(self.store_path, str(file_name))
                self.store_response(response, store_file_path)
                counter = counter + 1

        logging.log(logging.INFO, 'Success! Processed: {0}'.format(counter))


if __name__ == '__main__':
    Downloader().run()
