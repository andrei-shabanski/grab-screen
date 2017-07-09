import importlib
import logging

from ..conf import config
from ..exceptions import StorageError

logger = logging.getLogger(__name__)


def get_storage(name=None):
    if not name:
        name = config.STORAGES_DEFAULT

    module_path = 'grab_screen.storages.{}'.format(name)

    try:
        module_ = importlib.import_module(module_path)
        return module_.Storage()
    except (ImportError, AttributeError):
        logger.error("Cannot find storage '%s' by path '%s", name, module_path)
        raise StorageError("Storage '%s' doesn't exist." % name)
