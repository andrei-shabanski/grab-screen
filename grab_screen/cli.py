import sys

import click

from .conf import config
from .exceptions import ScreenError, StorageError
from .images import capture_image
from .screen import Grabber
from .storages import get_storage
from .utils import copy_to_clipboard, open_path
from .version import __version__

echo_error = lambda text: click.echo(click.style(text, fg='red'), err=True)


def prompt_config_value(ctx, param, value):
    if value is not None:
        return value

    if ctx.params['unset']:
        return None

    return click.prompt('Secret', hide_input=True)


@click.group("cloudapp-screenshots")
@click.help_option('-h', '--help')
@click.version_option(__version__, '-v', '--version', message="v%(version)s")
def main():
    pass


@main.group('config', help="Get and set options.")
@click.help_option('-h', '--help')
def config_group():
    pass


@config_group.command('set', help="Set the option.")
@click.argument('key')
@click.argument('value', required=False, callback=prompt_config_value)
@click.help_option('-h', '--help')
@click.option('-U', '--unset', is_flag=True, default=False, is_eager=True, help="Remove the option.")
def config_set(key, value, unset):
    key = key.replace('.', '_').upper()

    if unset:
        delattr(config, key)
    else:
        setattr(config, key, value)


@config_group.command('reset', help="Remove all options.")
@click.help_option('-h', '--help')
@click.option('-f', '--force', is_flag=True, default=False)
def config_reset(force):
    if not force and not click.confirm("Are you sure?"):
        echo_error('Aborted!')
        sys.exit(1)

    config.reset()


@config_group.command('list', help="Show options.")
@click.help_option('-h', '--help')
def config_list():
    lines = []

    for option in config:
        value = config.get(option)
        lines.append('{} = {}'.format(option, value))

    output = '\n'.join(lines)
    click.echo_via_pager(output)


@main.command('image', help="Make a screenshot and upload to a storage.")
@click.help_option('-h', '--help')
@click.option('-b', '--browse', 'is_browse', is_flag=True, help="Open a screenshot.")
@click.option('-c', '--clipboard', 'is_copy_to_clipboard', is_flag=True, help="Copy a screenshot path to clipboard.")
@click.option('-s', '--storage', 'storage_name', help="Choose a storage.")
def take_image(is_browse, is_copy_to_clipboard, storage_name):
    try:
        storage = get_storage(storage_name)

        coords = Grabber.select_area()
        image = capture_image(coords)

        file_detail = storage.save_image(image)
    except (ScreenError, StorageError) as e:
        echo_error(e.message)
        sys.exit(1)

    if is_browse:
        open_path(file_detail.path)

    if is_copy_to_clipboard:
        copy_to_clipboard(file_detail.path)
