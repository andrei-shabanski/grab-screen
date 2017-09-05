import logging.config
import os
from shutil import copyfile

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

logger = logging.getLogger(__name__)

DEFAULT_LEVEL = 'WARNING'
LOGGER_LEVELS = ('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET')


class Config(object):
    _default_section = 'app'
    _default_config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'default.ini'))

    def __init__(self, auto_save=True, path=None):
        if not path:
            if 'GRAB_SCREEN_CONFIG_FILE' in os.environ:
                path = os.environ['GRAB_SCREEN_CONFIG_FILE']
            else:
                path = os.path.join(os.path.expanduser('~'), '.config', 'grab-screen', 'config.ini')

        self.auto_save = auto_save
        self.path = path
        self._parser = None

        self.load()

    def __iter__(self):
        for section in self._parser.sections():
            for option in self._parser.options(section):
                key = '{}_{}'.format(section, option).upper()
                yield key

    def __getattribute__(self, key):
        if key.isupper():
            return self.get(key)

        return object.__getattribute__(self, key)

    def __setattr__(self, key, value):
        if key.isupper():
            return self.set(key, value)

        return object.__setattr__(self, key, value)

    def __delattr__(self, key):
        if key.isupper():
            return self.delete(key)

        return object.__delattr__(self, key)

    def get(self, key):
        """Gets an option."""
        section, option = self._split_key(key)

        if not self._parser.has_option(section, option):
            return None

        return self._parser.get(section, option)

    def set(self, key, value):
        """Sets an option."""
        if value is None:
            self.delete(key)
            return

        section, option = self._split_key(key)

        self._parser.set(section, option, str(value))

        if self.auto_save:
            self.save()

    def delete(self, key):
        """Deletes an option."""
        section, option = self._split_key(key)
        removed = self._parser.remove_option(section, option)

        if removed and self.auto_save:
            self.save()

    def load(self):
        """Reads settings from the file."""
        if not os.path.exists(self.path):
            self.reset()
            return

        self._parser = ConfigParser()
        self._parser.read(self.path)

        self._load_logger()

    def save(self):
        """Writes settings to the file."""
        self._create_config_directory()

        for section in self._parser.sections():
            if not self._parser.options(section):
                self._parser.remove_section(section)

        with open(self.path, 'w') as config_file:
            self._parser.write(config_file)

    def reset(self):
        """Restores the default settings."""
        self._create_config_directory()

        copyfile(self._default_config_file_path, self.path)

        self.load()

    def _create_config_directory(self):
        directory = os.path.dirname(self.path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def _load_logger(self):
        """
        Setup the logger configs.

        User can set `LOGGER_LEVEL` setting to change the logger level.
        """
        level = self.LOGGER_LEVEL
        if level:
            level = level.upper()
        if level not in LOGGER_LEVELS:
            logger.warning("Invalid logger level '%s'", level)
            level = DEFAULT_LEVEL

        logging.config.dictConfig({
            'version': 1,
            'formatters': {
                'simple': {
                    'format': '%(asctime)s [%(levelname)s] %(message)s'
                },
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple',
                },
            },
            'loggers': {
                'grab_screen': {
                    'level': level,
                    'handlers': ['console'],
                },
            }
        })

    def _split_key(self, key):
        """Gets a section and an option names by the key."""
        key = key.lower()

        try:
            section, option = key.split('_', 1)
        except (ValueError, IndexError):
            section = self._default_section
            option = key

        if not self._parser.has_section(section):
            self._parser.add_section(section)

        return section, option
