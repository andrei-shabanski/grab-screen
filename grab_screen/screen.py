import logging
import tempfile
import subprocess

logger = logging.getLogger(__name__)


def grab_image():
    tmp_file = tempfile.mktemp(prefix='screenshot-', suffix='.png')

    _gnome_screenshot(tmp_file)

    return tmp_file


def _gnome_screenshot(file_path):
    logger.info("Grabbing screen via gnome-screenshot")
    code = subprocess.call(['gnome-screenshot', '-a', '-f', file_path])
    if code != 0:
        raise Exception('Oops')
