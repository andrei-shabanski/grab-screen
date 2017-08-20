import logging
import os
from datetime import datetime

import requests
from requests.auth import HTTPDigestAuth

from .base import BaseStorage, File
from ..conf import config
from ..exceptions import StorageError

logger = logging.getLogger(__name__)


class Storage(BaseStorage):
    cloudapp_base_url = 'https://my.cl.ly/v3'

    def __init__(self):
        username = config.CLOUDAPP_USERNAME
        password = config.CLOUDAPP_PASSWORD
        if not username or not password:
            raise StorageError("Set 'cloudapp_username' and 'cloudapp_password' configs.")

        self._cloudapp_auth = HTTPDigestAuth(username, password)
        self._session = requests.Session()
        self._session.headers = {
            'Accept': 'application/json',
        }

    def save_image(self, image):
        logger.info('Uploading an image to CloudApp.')
        now = datetime.now()
        filename = 'Image %s.%s' % (now.strftime('%Y-%m-%d at %H:%M:%S'), image.format)

        file_detail = self._upload_file(image.stream, filename)

        return File(File.IMAGE, file_detail['share_url'])

    def _upload_file(self, stream, filename):
        cl_file_meta_url = self._build_cloudapp_url('items')
        cl_file_meta = self._request('POST', cl_file_meta_url, auth=self._cloudapp_auth, data={'name': filename})

        s3_url = cl_file_meta['url']
        s3_data = cl_file_meta['s3']
        s3_files = {'file': (filename, stream)}
        file_detail = self._request('POST', s3_url, data=s3_data, files=s3_files)

        return file_detail

    def _request(self, method, url, **kwargs):
        try:
            logger.debug('Sending a %s request to %s: %s', method, url, kwargs)
            response = self._session.request(method, url, **kwargs)
            logger.debug('Response from %s: status=%s body=%s', url, response.status_code, response.text)
        except requests.RequestException as e:
            logger.error(e)
            raise StorageError("Can't send a request to url: {}".format(e))

        self._handle_bad_request(response)

        return response.json()

    def _build_cloudapp_url(self, path):
        if path.startswith('/'):
            path = path[1:]

        return os.path.join(self.cloudapp_base_url, path)

    def _handle_bad_request(self, response):
        if response.ok:
            return

        if response.status_code >= 500:
            error_msg = "CloudApp broken :("
        elif response.status_code == 400:
            error_msg = "CloudApp doesn't want to accept our request. Sorry :("
        elif response.status_code in (401, 403):
            error_msg = "Invalid credentials for CloudApp."
        else:
            error_msg = "Bad response from Cloudapp ({}): {}".format(response.status_code, response.text)

        raise StorageError(error_msg)
