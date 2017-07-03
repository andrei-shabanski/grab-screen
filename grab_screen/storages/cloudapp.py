import logging
import os
import requests
from requests.auth import HTTPDigestAuth

from .base import BaseStorage
from ..conf import config

logger = logging.getLogger(__name__)


class Storage(BaseStorage):
    base_url = 'https://my.cl.ly/'
    version = 'v3'

    def __init__(self, username=config.CLOUDAPP_USERNAME, password=config.CLOUDAPP_PASSWORD):
        self._auth = HTTPDigestAuth(username, password)
        self._session = requests.Session()
        self._session.headers = {
            'Accept': 'application/json',
        }

    def upload_file(self, path):
        logger.info('Uploading file %s', path)
        filename = os.path.basename(path)

        s3_meta = self._call('POST', 'items', data={'name': filename})

        s3_url = s3_meta['url']
        s3_data = s3_meta['s3']
        s3_files = {'file': (filename, open(path, 'rb'))}

        logger.debug('Sending a POST request to %s: data=%s files=%s', s3_url, s3_data, s3_files)
        response = self._session.post(s3_url, data=s3_data, files=s3_files)

        return response.json()

    def _call(self, method, path, **kwargs):
        url = self._build_url(path)

        logger.debug('Sending a %s request to %s: %s', method, url, kwargs)
        response = self._session.request(method, url, auth=self._auth, **kwargs)

        if not response.ok:
            logger.debug('Request to %s failed: status=%s body=%s', url, response.status_code, response.text)
            raise Exception('Oops')

        return response.json()

    def _build_url(self, path):
        if path.startswith('/'):
            path = path[1:]

        return os.path.join(self.base_url, self.version, path)
