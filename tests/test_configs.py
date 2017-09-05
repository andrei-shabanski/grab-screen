import logging
import os

import pytest


def test_default_config_object():
    from grab_screen.conf import config

    assert os.path.exists(config.path)
    assert config.APP_STORAGE == 'cloudapp'  # default option


@pytest.mark.parametrize('input_value,expected_value', [
    ('test', 'test'),
    (12345, '12345'),
    (1.25, '1.25'),
    (False, 'False'),
    (None, None),
])
def test_get_value(config_factory, mocker, input_value, expected_value):
    config = config_factory()
    mocker.spy(config, 'get')

    config.TEST_OPTION = input_value
    actual_value = config.TEST_OPTION

    config.get.assert_called_with('TEST_OPTION')
    assert actual_value == expected_value


def test_get_not_existing_value(config_factory):
    config = config_factory()
    not_existing_value = config.NOT_EXISTING_VALUE

    assert not_existing_value is None


def test_get_lower_key(config_factory, mocker):
    config = config_factory()
    mocker.spy(config, 'get')

    with pytest.raises(AttributeError):
        not_existing_attr = config.test_value  # noqa: F841

    assert config.get.call_count == 0


def test_set_value(config_factory, mocker):
    config = config_factory()
    mocker.spy(config, 'set')

    config.TEST_VALUE = 'test value'

    config.set.assert_called_with('TEST_VALUE', 'test value')
    assert config.TEST_VALUE == 'test value'


def test_set_option_at_default_section(config_factory):
    config = config_factory()

    config.WITHOUTSECTION = 'test value'

    assert config.WITHOUTSECTION == 'test value'
    assert config.APP_WITHOUTSECTION == 'test value'


def test_set_option_at_specific_section(config_factory):
    config = config_factory()

    config.PART1_PART2_PART3 = 'test value'

    assert config.PART1_PART2_PART3 == 'test value'
    assert config.APP_PART1_PART2_PART3 is None


def test_delete_option(config_factory, mocker):
    config = config_factory()
    mocker.spy(config, 'delete')

    config.TEST_VALUE = 'test value'
    del config.TEST_VALUE

    assert config.TEST_VALUE is None
    config.delete.assert_called_with('TEST_VALUE')


def test_delete_not_existing_option(config_factory, mocker):
    config = config_factory()
    mocker.spy(config, 'delete')

    del config.NOT_EXISTING_VALUE

    config.delete.assert_called_with('NOT_EXISTING_VALUE')


def test_load_config(config_factory):
    config_content = """
[app]
option = option of default section

[test]
option = test load method
"""
    config = config_factory(content=config_content)

    config.load()

    assert config.OPTION == 'option of default section'
    assert config.APP_OPTION == 'option of default section'
    assert config.TEST_OPTION == 'test load method'


def test_load_logger_config(config_factory):
    config_factory(content='[logger]\nlevel = DEBUG')

    logger = logging.getLogger('grab_screen')

    assert logger.level == logging.DEBUG


def test_save_config(config_factory):
    config = config_factory(content='', auto_save=False)

    config.TEST_TEXT = 'test save method'
    config.TEST_NUMBER = 12345
    config.TEST_NONE = None
    config.TEST_BOOLEAN = True
    config.save()

    with open(config.path) as config_file:
        actual_config_content = config_file.read()

    expected_config_content = """[test]
text = test save method
number = 12345
boolean = True

"""

    assert actual_config_content == expected_config_content


def test_reset_configs(config_factory):
    config = config_factory(auto_save=False)

    assert config.APP_STORAGE == 'cloudapp'
    assert config.TEST_VALUE is None

    config.APP_STORAGE = 'other_storage'  # default option
    config.TEST_VALUE = 'test value'
    config.save()
    config.reset()

    with open(config.path) as config_file:
        actual_config_content = config_file.read()

    with open(config._default_config_file_path) as default_config_file:
        expected_config_content = default_config_file.read()

    assert config.APP_STORAGE == 'cloudapp'
    assert config.TEST_VALUE is None
    assert actual_config_content == expected_config_content


def test_default_autosave(config_factory, mocker):
    from grab_screen.conf import config

    assert config.auto_save


def test_enable_autosave(config_factory, mocker):
    config = config_factory(auto_save=True)
    mocker.spy(config, 'save')

    config.TEST_VALUE = 'test value'
    assert config.save.call_count == 1

    del config.TEST_VALUE
    assert config.save.call_count == 2


def test_disable_autosave(config_factory, mocker):
    config = config_factory(auto_save=False)
    mocker.spy(config, 'save')

    config.TEST_VALUE = 'test value'
    del config.TEST_VALUE

    assert config.save.call_count == 0
