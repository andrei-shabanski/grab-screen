import logging
import os
import tempfile
import subprocess

from .exceptions import ScreenError

logger = logging.getLogger(__name__)


def grab_image():
    tmp_file = tempfile.mkstemp(prefix='screenshot-', suffix='.png')[1]

    _gnome_screenshot(tmp_file)

    return tmp_file


def _gnome_screenshot(file_path):
    logger.info("Grabbing screen via gnome-screenshot")
    code = subprocess.call(['gnome-screenshot', '-a', '-f', file_path])

    if code != 0 or not os.path.exists(file_path):
        raise ScreenError("Oops, can't take screenshot.")

    if not os.path.getsize(file_path):
        raise ScreenError("Abort.")
