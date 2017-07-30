import sys

import click

from .conf import config
from .exceptions import ScreenError, StorageError
from .screen import take_image
from .storages import get_storage
from .utils import copy_to_clipboard, open_path
from .version import __version__

echo_error = lambda text: click.echo(click.style(text, fg='red'), err=True)


def prompt_config_value(ctx, param, value):
    if value is not None:
        return value

    if ctx.params['unset']:
        return None

    return click.prompt('Value', hide_input=True)


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

    config.reset(reload=False)


@config_group.command('list', help="Show options.")
@click.help_option('-h', '--help')
def config_list():
    lines = []

    prev_option = None
    for option in config:
        if not prev_option or prev_option.section != option.section:
            lines.append('[{}]'.format(option.section))
        lines.append("\t{} = '{}'".format(option.option, option.value))

        prev_option = option

    output = '\n'.join(lines)
    click.echo_via_pager(output)


@main.command('image', help="Make a screenshot and upload to a storage.")
@click.help_option('-h', '--help')
@click.option('-b', '--browse', 'is_browse', is_flag=True, help="Open a screenshot.")
@click.option('-c', '--clipboard', 'is_copy_to_clipboard', is_flag=True, help="Copy a screenshot path to clipboard.")
@click.option('-s', '--storage', 'storage_name', help="Choose a storage.")
def make_image(is_browse, is_copy_to_clipboard, storage_name):
    try:
        image_stream, fmt = take_image()
    except ScreenError as e:
        echo_error(e.message)
        sys.exit(1)

    try:
        storage = get_storage(storage_name)
        file_detail = storage.upload_image(image_stream, fmt)
    except StorageError as e:
        echo_error(e.message)
        sys.exit(1)

    if is_browse:
        open_path(file_detail.path)

    if is_copy_to_clipboard:
        copy_to_clipboard(file_detail.path)
