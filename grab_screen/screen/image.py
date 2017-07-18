import logging
from io import BytesIO

from .grabber import grab_area

logger = logging.getLogger(__name__)

__all__ = ['take_image']


def take_image(storage):
    logger.info("Taking an image.")

    coords = grab_area()

    logger.info("Capturing a screen.")
    stream, format = _capture_screen_via_mss(coords)

    logger.info("Saving the image in the storage.")
    file_detail = storage.upload_image(stream, format)

    return file_detail


def _capture_screen_via_mss(coords):
    from mss import mss
    from ._mss import to_png

    monitor = {
        'top': coords[1],
        'left': coords[0],
        'width': coords[2] - coords[0] + 1,
        'height': coords[3] - coords[1] + 1,
    }

    screen = mss()
    image = screen.grab(monitor)

    stream = to_png(image.rgb, image.size)
    fmt = 'png'

    return stream, fmt


def _capture_screen_via_pyscreenshot(coords):
    import pyscreenshot

    stream = BytesIO()
    fmt = 'png'

    image = pyscreenshot.grab(coords)
    image.save(stream, format=fmt)

    return stream, fmt
