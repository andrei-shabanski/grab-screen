import sys

import click

from .conf import config as app_config
from .exceptions import StorageError, ScreenError
from .screen import take_image
from .storages import get_storage
from .utils import open_path, copy_to_clipboard
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
@click.version_option(__version__, '-v', '--version')
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
        delattr(app_config, key)
    else:
        setattr(app_config, key, value)


@config_group.command('reset', help="Remove all options.")
@click.help_option('-h', '--help')
@click.option('-f', '--force', is_flag=True, default=False)
def config_reset(force):
    if not force and not click.confirm("Are you sure?"):
        echo_error('Aborted!')
        sys.exit(1)

    app_config.reset(reload=False)


@config_group.command('list', help="Show options.")
@click.help_option('-h', '--help')
def config_list():
    lines = []

    prev_option = None
    for option in app_config:
        if not prev_option or prev_option.section != option.section:
            lines.append('[{}]'.format(option.section))
        lines.append("\t{} = '{}'".format(option.option, option.value))

        prev_option = option

    output = '\n'.join(lines)
    click.echo_via_pager(output)


@main.command('image', help="Make a screenshot and upload to a storage.")
@click.help_option('-h', '--help')
@click.option('-b', '--browser', is_flag=True, help="Open a uploaded file in the browser.")
@click.option('-c', '--clipboard', is_flag=True, help="Copy a url to clipboard.")
@click.option('-s', '--storage', help="Choose a storage.")
def make_image(browser, clipboard, storage):

    try:
        storage = get_storage(storage)
        file_detail = take_image(storage)
    except (ScreenError, StorageError) as e:
        echo_error(e.message)
        sys.exit(1)

    if browser:
        open_path(file_detail.path)

    if clipboard:
        copy_to_clipboard(file_detail.path)
