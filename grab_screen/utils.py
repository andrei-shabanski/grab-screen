import logging
import webbrowser
import pyperclip

logger = logging.getLogger(__name__)


def open_path(path):
    logger.info('Opening %s.', path)
    webbrowser.open(path)


def copy_to_clipboard(text):
    logger.info('Copying text to clipboard: %s', text)
    pyperclip.copy(text)
