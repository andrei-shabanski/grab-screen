import logging
import webbrowser

import pyperclip

logger = logging.getLogger(__name__)


def open_path(path):
    """Open a local path or URL."""
    logger.info('Opening %s.', path)
    webbrowser.open(path)


def copy_to_clipboard(text):
    """Writes a text to clipboard."""
    logger.info('Copying text to clipboard: %s', text)
    pyperclip.copy(text)
