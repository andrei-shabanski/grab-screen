import logging
import os
import time

import requests
from requests.auth import HTTPDigestAuth

from .base import BaseStorage, File
from ..conf import config
from ..exceptions import StorageError

logger = logging.getLogger(__name__)


class Storage(BaseStorage):
    base_url = 'https://my.cl.ly/v3'

    def __init__(self, username=config.CLOUDAPP_USERNAME, password=config.CLOUDAPP_PASSWORD):
        self._auth = HTTPDigestAuth(username, password)
        self._session = requests.Session()
        self._session.headers = {
            'Accept': 'application/json',
        }

    def upload_image(self, stream, fmt='png'):
        logger.info('Uploading an image to CloudApp.')
        filename = 'screenshot-%s.%s' % (time.time(), fmt)

        file_detail = self._upload_file(stream, filename)

        return File(File.IMAGE, file_detail['share_url'])

    def _upload_file(self, stream, filename):
        s3_meta = self._request('POST', 'items', data={'name': filename})

        s3_url = s3_meta['url']
        s3_data = s3_meta['s3']
        s3_files = {'file': (filename, stream)}

        logger.debug('Sending a POST request to %s: data=%s files=%s', s3_url, s3_data, s3_files)
        response = self._session.post(s3_url, data=s3_data, files=s3_files)

        return response.json()

    def _request(self, method, path, **kwargs):
        url = self._build_url(path)

        logger.debug('Sending a %s request to %s: %s', method, url, kwargs)
        try:
            response = self._session.request(method, url, auth=self._auth, **kwargs)
        except requests.RequestException as e:
            logger.error(e)
            raise StorageError("Can't send a request to CloudApp. {}".format(e))

        logger.debug('Request to %s failed: status=%s body=%s', url, response.status_code, response.text)

        if not response.ok:
            if response.status_code >= 500:
                error_msg = "CloudApp broken :("
            elif response.status_code == 400:
                error_msg = "CloudApp doesn't want to accept our request. Sorry :("
            elif response.status_code in (401, 403):
                error_msg = "Invalid credentials for CloudApp."
            else:
                error_msg = None
            raise StorageError(error_msg)

        return response.json()

    def _build_url(self, path):
        if path.startswith('/'):
            path = path[1:]

        return os.path.join(self.base_url, path)
