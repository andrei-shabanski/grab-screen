import sys

import click

from .conf import config as app_config
from .exceptions import StorageError, ScreenError
from .screen import grab_image
from .storages import get_storage
from .utils import open_path, copy_to_clipboard
from .version import __version__

echo_error = lambda text: click.echo(click.style(text, fg='red'))


def prompt(ctx, param, value):
    if value is not None:
        return value

    return click.prompt('Value', hide_input=ctx.params['secret'], show_default=False)


@click.group("cloudapp-screenshots")
@click.help_option('-h', '--help')
@click.version_option(__version__, '-v', '--version')
def main():
    pass


@main.command(help="Set options.")
@click.help_option('-h', '--help')
@click.argument('key')
@click.argument('value', required=False, callback=prompt)
@click.option('-s', '--secret', is_flag=True, default=False, is_eager=True, help="Prompt a secret value.")
@click.option('--unset', is_flag=True, default=False, help="Remove an option.")
@click.option('--reset', is_flag=True, default=False, help="Remove all options.")
def config(key, value, secret, unset, reset):
    if reset:
        app_config.reset()
        return

    key = key.replace('.', '_').upper()

    if unset:
        delattr(app_config, key)
    else:
        setattr(app_config, key, value)


@main.command(help="Make a screenshot and upload to CloudApp.")
@click.help_option('-h', '--help')
@click.option('-b', '--browser', is_flag=True, help="Open a uploaded file in the browser.")
@click.option('-c', '--clipboard', is_flag=True, help="Copy a url to clipboard.")
@click.option('-s', '--storage', help="Choose a storage.")
def image(browser, clipboard, storage):
    try:
        tmp_file_path = grab_image()
    except ScreenError as e:
        echo_error(e.message)
        sys.exit(1)

    try:
        storage = get_storage(storage)
        file = storage.upload_image(tmp_file_path)
    except StorageError as e:
        echo_error(e.message)
        sys.exit(1)

    if browser:
        open_path(file.path)

    if clipboard:
        copy_to_clipboard(file.path)
