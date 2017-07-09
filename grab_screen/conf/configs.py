import logging.config
import os
import ConfigParser
from collections import namedtuple
from shutil import copyfile

logger = logging.getLogger(__name__)

Option = namedtuple('Option', ('key', 'section', 'option', 'value'))


class Config(object):
    _path = os.path.join(os.path.expanduser('~'), '.config', 'grab-screen', 'config.ini')

    _auto_save = True

    _default_section = 'app'
    _sections = ('app', 'logger', 'storages', 'cloudapp')

    _default_option = 'default'

    def __init__(self):
        self._config = ConfigParser.ConfigParser()

    def __iter__(self):
        for section in self._sections:
            if not self._config.has_section(section):
                continue

            for option, value in self._config.items(section):
                key = '{}_{}'.format(section, option).upper()
                yield Option(key, section, option, value)

    def __getattribute__(self, key):
        if key.isupper():
            return self._get_value(key)

        return object.__getattribute__(self, key)

    def __setattr__(self, key, value):
        if key.isupper():
            return self._set_value(key, value)

        return object.__setattr__(self, key, value)

    def __delattr__(self, key):
        if key.isupper():
            return self._del_value(key)

        return object.__delattr__(self, key)

    def load(self):
        if not os.path.exists(self._path):
            self.reset()

        self._config.read(self._path)

        self._load_logger()

    def save(self):
        self._create_path()

        with open(self._path, 'w') as config_file:
            self._config.write(config_file)

    def reset(self, reload=True):
        self._create_path()

        default_config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'default.ini'))
        copyfile(default_config_path, self._path)

        if reload:
            self.load()

    def _create_path(self):
        directory = os.path.dirname(self._path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def _load_logger(self):
        level = self.LOGGER_LEVEL.upper()
        if level not in logging._levelNames.keys():
            logger.warning("Invalid logger level '%s'", level)
            level = 'INFO'

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
                    'level': self.LOGGER_LEVEL.upper(),
                    'handlers': ['console'],
                },
            }
        })

    def _get_value(self, key):
        key = key.lower()

        section, option = self._split_key(key)
        type_ = self._get_value_type(option)

        if not self._config.has_option(section, option):
            return None

        if type_ == 'int':
            getter = self._config.getint
        elif type_ == 'float':
            getter = self._config.getfloat
        elif type_ == 'boolean':
            getter = self._config.getboolean
        else:
            getter = self._config.get

        return getter(section, option)

    def _set_value(self, key, value):
        if value is None:
            return self._del_value(key)

        key = key.lower()

        section, option = self._split_key(key)

        self._config.set(section, option, str(value))

        if self._auto_save:
            self.save()

    def _del_value(self, key):
        key = key.lower()

        section, option = self._split_key(key)
        self._config.remove_option(section, option)

        if self._auto_save:
            self.save()

    def _split_key(self, key):
        words = key.split('_', 1)

        try:
            section = filter(lambda s: s == words[0], self._sections)[0]
            option = words[1] or self._default_option
        except IndexError:
            section = self._default_section
            option = key

        if not self._config.has_section(section):
            self._config.add_section(section)

        return section, option

    def _get_value_type(self, key):
        if key.startswith('is_'):
            return 'boolean'

        return ''
