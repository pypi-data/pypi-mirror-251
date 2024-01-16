import os
import logging
import tempfile
import requests
from tqdm import tqdm
from functools import partial
from argparse import ArgumentParser
from requests.adapters import Retry


API_FILE_DOWNLOAD_RETRY_TIMES = 5
API_FILE_DOWNLOAD_TIMEOUT = 60 * 5
API_FILE_DOWNLOAD_CHUNK_SIZE = 4096
LOCAL_DIR = os.path.join(os.path.expanduser('~'), '.cubeai_model_cache')
if not os.path.exists(LOCAL_DIR):
    os.mkdir(LOCAL_DIR)


def get_model_path(file_name):
    return os.path.join(LOCAL_DIR, file_name)


def download_model_file(url, file_name):
    filepath = os.path.join(LOCAL_DIR, file_name)
    if os.path.exists(filepath):
        logging.critical(f'File {filepath} already exist!')
        return

    temp_file_manager = partial(tempfile.NamedTemporaryFile, mode='wb', dir=LOCAL_DIR, delete=False)
    get_headers = {}
    with temp_file_manager() as temp_file:
        logging.critical('downloading %s to %s', url, temp_file.name)
        # retry sleep 0.5s, 1s, 2s, 4s
        retry = Retry(total=API_FILE_DOWNLOAD_RETRY_TIMES, backoff_factor=1)
        while True:
            try:
                downloaded_size = temp_file.tell()
                get_headers['Range'] = 'bytes=%d-' % downloaded_size
                r = requests.get(url, stream=True, headers=get_headers, timeout=API_FILE_DOWNLOAD_TIMEOUT)
                r.raise_for_status()
                content_length = r.headers.get('Content-Length')
                total = int(content_length) if content_length is not None else None
                progress = tqdm(
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    total=total,
                    initial=downloaded_size,
                    desc='Downloading',
                )
                for chunk in r.iter_content(chunk_size=API_FILE_DOWNLOAD_CHUNK_SIZE):
                    if chunk:  # filter out keep-alive new chunks
                        progress.update(len(chunk))
                        temp_file.write(chunk)
                progress.close()
                break
            except (Exception) as e:  # no matter what happen, we will retry.
                retry = retry.increment('GET', url, error=e)
                retry.sleep()

    logging.critical('storing %s in cache at %s', url, LOCAL_DIR)
    downloaded_length = os.path.getsize(temp_file.name)
    if total != downloaded_length:
        os.remove(temp_file.name)
        msg = 'File %s download incomplete, content_length: %s but the \
                    file downloaded length: %s, please download again' % (
            file_name, total, downloaded_length)
        logging.critical(msg)
        raise Exception(msg)

    os.replace(temp_file.name, os.path.join(LOCAL_DIR, file_name))


def download_model():
    parser = ArgumentParser()
    parser.add_argument('--url', default=None, help='待下载文件URL')
    parser.add_argument('--file-name', default=None, help='下载后保存至该文件名')
    args = parser.parse_args()

    if args.url is None or args.file_name is None:
        parser.print_usage()
        return

    download_model_file(url=args.url, file_name=args.file_name)
