import logging
import pyperclip
import webbrowser

logger = logging.getLogger(__name__)


def open_url(url):
    logger.info('Opening %s in the browser.', url)
    webbrowser.open(url)


def copy_to_clipboard(text):
    logger.info('Copying text to clipboard: %s', text)
    pyperclip.copy(text)
