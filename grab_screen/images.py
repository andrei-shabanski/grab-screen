import io
import logging
import struct
import zlib
from collections import namedtuple

from mss import mss

__all__ = ['capture_image']

logger = logging.getLogger(__name__)

Image = namedtuple('Image', ('stream', 'format'))


def capture_image(coords):
    """Take a screenshot."""
    logger.info("Capturing a screen.")
    screen = mss()
    mss_image = screen.grab({
        'top': coords.top,
        'left': coords.left,
        'width': coords.right - coords.left + 1,
        'height': coords.bottom - coords.top + 1,
    })

    stream = to_png(mss_image.rgb, mss_image.size)

    return Image(stream, 'png')


def to_png(data, size):
    """
    Dump data to a PNG file.

    This code is a part of the MSS library.
    Source: https://github.com/BoboTiG/python-mss/blob/d740fa774cae4b8ccaddf980cbf417ebe33117e7/mss/tools.py#L10
    MSS License: MIT
    2017-07-18

    :param bytes data: RGBRGB...RGB data.
    :param tuple size: The (width, height) pair.
    """

    width, height = size
    line = width * 3
    png_filter = struct.pack('>B', 0)
    scanlines = b''.join(
        [png_filter + data[y * line:y * line + line]
         for y in range(height)])

    magic = struct.pack('>8B', 137, 80, 78, 71, 13, 10, 26, 10)

    # Header: size, marker, data, CRC32
    ihdr = [b'', b'IHDR', b'', b'']
    ihdr[2] = struct.pack('>2I5B', width, height, 8, 2, 0, 0, 0)
    ihdr[3] = struct.pack('>I', zlib.crc32(b''.join(ihdr[1:3])) & 0xffffffff)
    ihdr[0] = struct.pack('>I', len(ihdr[2]))

    # Data: size, marker, data, CRC32
    idat = [b'', b'IDAT', zlib.compress(scanlines), b'']
    idat[3] = struct.pack('>I', zlib.crc32(b''.join(idat[1:3])) & 0xffffffff)
    idat[0] = struct.pack('>I', len(idat[2]))

    # Footer: size, marker, None, CRC32
    iend = [b'', b'IEND', b'', b'']
    iend[3] = struct.pack('>I', zlib.crc32(iend[1]) & 0xffffffff)
    iend[0] = struct.pack('>I', len(iend[2]))

    # store data in memory
    fileh = io.BytesIO()
    fileh.write(magic)
    fileh.write(b''.join(ihdr))
    fileh.write(b''.join(idat))
    fileh.write(b''.join(iend))
    fileh.seek(0)

    return fileh
