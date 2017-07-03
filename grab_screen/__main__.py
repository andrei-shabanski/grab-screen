import click

from . import __version__
from .storages import get_storage
from .screen import grab_image
from .conf import config as app_config
from .utils import open_url, copy_to_clipboard


@click.group("cloudapp-screenshots")
@click.help_option('-h', '--help')
@click.version_option(__version__, '-v', '--version')
def cli():
    pass


@click.command(help="Set options.")
@click.help_option('-h', '--help')
@click.option('-k', '--key', prompt=True)
@click.option('-v', '--value', prompt=True)
def config(key, value):
    key = key.replace('.', '_').upper()
    setattr(app_config, key, value)


@click.command(help="Make a screenshot and upload to CloudApp.")
@click.help_option('-h', '--help')
@click.option('-b', '--browser', is_flag=True, help="Open a uploaded file in the browser.")
@click.option('-c', '--clipboard', is_flag=True, help="Copy url to clipboard.")
def make(browser, clipboard):
    file_path = grab_image()

    storage = get_storage()
    file_detail = storage.upload_file(file_path)

    file_url = file_detail['share_url']

    if browser:
        open_url(file_url)

    if clipboard:
        copy_to_clipboard(file_url)


cli.add_command(config, 'config')
cli.add_command(make, 'make')


if __name__ == '__main__':
    cli()
