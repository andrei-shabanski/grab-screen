import click

from .conf import config as app_config
from .screen import grab_image
from .storages import get_storage
from .utils import open_url, copy_to_clipboard
from .version import __version__


@click.group("cloudapp-screenshots")
@click.help_option('-h', '--help')
@click.version_option(__version__, '-v', '--version')
def main():
    pass


@click.command(help="Set options.")
@click.help_option('-h', '--help')
@click.argument('key')
@click.argument('value', required=False, default='')
@click.option('--unset', is_flag=True, default=False)
def config(key, value, unset):
    key = key.replace('.', '_').upper()

    if unset:
        delattr(app_config, key)
    else:
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


main.add_command(config)
main.add_command(make)
