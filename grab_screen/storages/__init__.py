import importlib

from ..conf import config


def get_storage(name=config.STORAGES_DEFAULT):
    module_path = 'grab_screen.storages.{}'.format(name)
    module_ = importlib.import_module(module_path)
    return module_.Storage()
