import os
import tempfile

import pytest

_TEMP_DIR = tempfile.mkdtemp(prefix='grab-screen')


@pytest.fixture(scope='session', autouse=True)
def set_global_envs():
    os.environ['GRAB_SCREEN_CONFIG_FILE'] = os.path.join(_TEMP_DIR, 'config.ini')


@pytest.fixture()
def config_factory(monkeypatch, tmpdir):
    from grab_screen.conf.configs import Config

    def create_config(content=None, **config_args):
        config_file = tmpdir.join('config.ini')
        config_file_path = str(config_file)
        if content is not None:
            config_file.write(content)

        monkeypatch.setenv('GRAB_SCREEN_CONFIG_FILE', config_file_path)

        return Config(**config_args)

    yield create_config
