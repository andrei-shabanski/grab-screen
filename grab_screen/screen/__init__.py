import logging
import os
import tempfile

import pyscreenshot

from .grabber import grab_area

logger = logging.getLogger(__name__)


def take_image(storage):
    coords = grab_area()

    logger.info("Taking an image.")
    tmp_file_path = tempfile.mkstemp(prefix='screenshot-', suffix='.png')[1]

    image = pyscreenshot.grab(coords)
    image.save(tmp_file_path)

    logger.info("Saving the image in the storage.")
    file_detail = storage.upload_image(tmp_file_path)

    os.unlink(tmp_file_path)

    return file_detail
