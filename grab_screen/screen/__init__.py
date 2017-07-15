import logging
import tempfile

import pyscreenshot

from .grabber import grab_area

logger = logging.getLogger(__name__)


def take_image():
    coords = grab_area()

    logger.info("Taking an image.")
    tmp_file = tempfile.mkstemp(prefix='screenshot-', suffix='.png')[1]

    image = pyscreenshot.grab(coords)
    image.save(tmp_file)

    return tmp_file
