import logging.config
import os
from shutil import copyfile

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

logger = logging.getLogger(__name__)

DEFAULT_LEVEL = 'WARNING'
LOGGER_LEVELS = ('CRITICAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG', 'NOTSET')

TEXT = 1
BOOLEAN = 2


class Config(object):
    _path = os.path.join(os.path.expanduser('~'), '.config', 'grab-screen', 'config.ini')

    _default_section = 'app'
    _sections = ('app', 'logger', 'cloudapp')

    _default_option = 'default'

    def __init__(self, auto_save=True):
        self._auto_save = auto_save
        self._config = ConfigParser()

    def __iter__(self):
        for section in self._sections:
            if not self._config.has_section(section):
                continue

            for option in self._config.options(section):
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
        key = key.lower()

        section, option = self._split_key(key)
        option_type = self._get_value_type(option)

        if not self._config.has_option(section, option):
            return None

        if option_type == BOOLEAN:
            getter = self._config.getboolean
        else:
            getter = self._config.get

        return getter(section, option)

    def set(self, key, value):
        """Sets an option."""
        key = key.lower()

        section, option = self._split_key(key)

        self._config.set(section, option, str(value))

        if self._auto_save:
            self.save()

    def delete(self, key):
        """Deletes an option."""
        key = key.lower()

        section, option = self._split_key(key)
        self._config.remove_option(section, option)

        if self._auto_save:
            self.save()

    def load(self):
        """Reads settings from the file."""
        if not os.path.exists(self._path):
            self.reset()
            return

        self._config.read(self._path)

        self._load_logger()

    def save(self):
        """Writes settings to the file."""
        self._create_config_directory()

        with open(self._path, 'w') as config_file:
            self._config.write(config_file)

    def reset(self):
        """Restores the default settings."""
        self._create_config_directory()

        default_config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'default.ini'))
        copyfile(default_config_path, self._path)

        self.load()

    def _create_config_directory(self):
        directory = os.path.dirname(self._path)
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
        words = key.split('_', 1)

        try:
            section = tuple(filter(lambda s: s == words[0], self._sections))[0]
            option = words[1] or self._default_option
        except IndexError:
            section = self._default_section
            option = key

        if not self._config.has_section(section):
            self._config.add_section(section)

        return section, option

    def _get_value_type(self, key):
        """Determines an option type."""
        if key.startswith('is_'):
            return BOOLEAN

        return TEXT
