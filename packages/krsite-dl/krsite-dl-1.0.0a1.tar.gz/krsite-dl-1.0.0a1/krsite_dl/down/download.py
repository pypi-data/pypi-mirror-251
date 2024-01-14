import requests
import os
import re
import time
import pytz
import email.utils

from datetime import timezone
from rich.progress import Progress
from urllib.parse import unquote, urlparse
from client.user import User
from common.url_selector import select_url
from common.logger import Logger

import krsite_dl.krsite_dl as kr

class DownloadHandler():
    logger = Logger("downloader")
    duplicate_counts = {}
    MAX_RETRIES = 3
    RETRY_DELAY = 5 #seconds
    def __init__(self):
        user = User()

        self.args = kr.args
        self.reserved_pattern = r'[\\/:*?"<>|]'
        self.user_agent = user.get_user_agent()
        self.certificate = user.get_certificate()
        self.session = self._session()

    
    # sanitize string to remove windows reserved characters
    def __sanitize_string(self, string):
        if not self.args.no_windows_filenames:
            string = re.sub(self.reserved_pattern, '', string)
        return string
    

    # location list for timezone
    def _location(self, loc):
        # list country codes here as json so i can call them by matching its keys
        country_codes = {
            "KR": "Asia/Seoul", "JP": "Asia/Tokyo", "SG": "Asia/Singapore"
        }

        return country_codes.get(loc, "UTC")
        

    # korean filename encoder
    def _encode_kr(self, img_name):
        decoded = unquote(img_name)

        if '%EC' in decoded or '%EB' in decoded:
            korean_filename = decoded.encode('utf-8')
        else:
            korean_filename = decoded.encode('euc-kr', errors='ignore')

        filename = self.__sanitize_string(korean_filename.decode('euc-kr'))

        return filename
    

    def _get_filename(self, item):
        # check if its url or not
        if not item.startswith('http'):
            base, x = os.path.splitext(item)
            return base, x
        
        parsed_url = urlparse(item)
        filename = os.path.basename(unquote(parsed_url.path))
        base, x = os.path.splitext(filename)
        # print(base, x)
        return base, x
    

    def _process_item(self, item):
        if isinstance(item, list) and len(item) == 2:
            url, filename = item[0], item[1]
        else:
            url, filename = item, self._get_filename(item)

        return url, filename
    

    def _media_selector(self, img_list):
        logger = Logger("media_selector")
        logger.log_info("Selecting images to download...")
        selected = select_url(img_list)

        if not selected:
            logger.log_info("No images selected.")
        return selected
    

    def _file_exists(self, dirs, filename):
        path = os.path.join(dirs, filename)
        if os.path.exists(path):
            self.logger.log_warning(f"File: {filename} already exists. Skipping...")
            return True


    def _extension_to_mime(self, ext):
        extensions = {
            '.jpg' or '.jpeg': '.jpg',
            '.JPG' or '.JPEG': '.jpg',
            '.png': '.png',
            '.PNG': '.png',
            '.gif': '.gif',
            '.GIF': '.gif',
            '.webp': '.webp',
            '.WEBP': '.webp',
        }
        return extensions.get(ext, '.jpg')


    def _session(self):
        session = requests.Session()
        session.headers = requests.models.CaseInsensitiveDict(
            {'User-Agent': self.user_agent, 
             'Accept-Encoding': 'identity', 
             'Connection': 'keep-alive'})
        return session
    

    def _retry_request(self, url, certificate, session):
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                response = session.get(url, verify=certificate, stream=True)
                return response
            except (requests.exceptions.SSLError, requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
                self.logger.log_error(f"{type(e).__name__}. Retrying... ({attempt}/{self.MAX_RETRIES})")
                time.sleep(self.RETRY_DELAY)
                session.close()
                session = self._session()

        return None  # Return None if maximum retries exceeded

    
    def _download_logic(self, medialist, dirs, option=None):
        for url in medialist:
            # get url and separate the filename as a new variable
            base, ext = self._get_filename(url)
            filename = self._encode_kr(base)
            ext = self._extension_to_mime(ext)
            
            if option == "naverpost":
                if filename in self.duplicate_counts:
                    self.duplicate_counts[filename] += 1
                    filename = f"{filename} ({self.duplicate_counts[filename]})"
                else:
                    self.duplicate_counts[filename] = 0
            if option == "combine":
                if len(medialist) > 1:
                    filename = f'{filename} ({medialist.index(url)+1})'

            # request
            certificate = self.certificate
            # response = self.session.get(url, verify=certificate, stream=True)
            response = self._retry_request(url, certificate, self.session)

            if response is None:
                self.logger.log_error(f"Max retries exceeded. Skipping...")
                continue

            # get headers
            headers = response.headers
            content_type = headers.get('content-type')
            content_length = headers.get('content-length')
            last_modified = headers.get('last-modified')
            content_disposition = headers.get('content-disposition')

            # get file extension
            if content_type is None:
                pass
            else:
                file_extensions = {
                    'image/jpeg': '.jpg',
                    'image/png': '.png',
                    'image/gif': '.gif',
                    'image/webp': '.webp',
                }

            content_length = int(content_length) # get the content length

            # if filename is provided on content_disposition, use it
            if content_disposition is not None:
                filename = content_disposition.split('filename=')[1].strip('"')
                filename = self.__sanitize_string(filename)
                base, ext = self._get_filename(filename)
                filename = self._encode_kr(base)

            file_extension = file_extensions.get(content_type, '.jpg')
    
            # print out information about the source and filename
            self.logger.log_info(f"{url}")

            # check if file already exists
            if self._file_exists(dirs, f"{filename}{file_extension}"):
                continue

            self.logger.log_info(f"filename: {filename}{file_extension}")
            file_part = os.path.join(dirs, f"{filename}{file_extension}.part")
            file_real = os.path.join(dirs, f"{filename}{file_extension}")
            try:
                current_size = os.path.getsize(file_part)
            except FileNotFoundError:
                current_size = 0

            if current_size < content_length:
            # download file
                with open(file_part, 'wb') as f:
                    with Progress(refresh_per_second=1) as prog:
                        task = prog.add_task("Downloading...", total=content_length)
                        for chunk in response.iter_content(chunk_size=20480):
                            current_size += len(chunk)
                            f.write(chunk)
                            prog.update(task, completed=current_size)


                os.rename(file_part, file_real)

                #convert GMT to local time for last_modified
                #Thu, 07 Dec 2023 02:01:31 GMT
                if last_modified is not None:
                    dt = email.utils.parsedate_to_datetime(last_modified)
                    dt = dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
                    timestamp = int(dt.timestamp())
                    os.utime(file_real, (timestamp, timestamp))
                    os.utime(dirs, (timestamp, timestamp))
                continue

    
    def downloader(self, payload):
        medialist, dirs, option = (
            payload.media,
            payload.directory,
            payload.option,
        )

        if kr.args.select:
            medialist = self._media_selector(medialist)

        self._download_logic(medialist, dirs, option=option)
        self.session.close()