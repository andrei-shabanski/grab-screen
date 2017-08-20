# Grab Screen

[![Build Status](https://travis-ci.org/andrei-shabanski/grab-screen.svg?branch=master)](https://travis-ci.org/andrei-shabanski/grab-screen)
[![PyPI](https://img.shields.io/pypi/pyversions/grab-screen.svg)](https://github.com/andrei-shabanski/grab-screen)
[![PyPI](https://img.shields.io/pypi/l/grab-screen.svg)](https://github.com/andrei-shabanski/grab-screen)

Take screenshots and upload anywhere!

## Installing

You install `grab-screen` with pip:

```shell
pip install grab-screen
```

## Usage

```shell
$ grab-screen --help
Usage: grab-screen [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help     Show this message and exit.
  -v, --version  Show the version and exit.

Commands:
  config  Get and set options.
  image   Make a screenshot and upload to a storage.
```

#### Configurations

`grab-screen config list` - show configs.

`grab-screen config set NAME [VALUE]` - set an option. You can add `--upset` to remove the option.

`grab-screen config reset` - remove all options.

#### Taking screenshots

`grab-screen image` - take a screenshot. 

Use `-h`/`--help` to see more options.

## Storages

* **CloudApp** ([website](https://getcloudapp.com/))

    Before uploading screenshots to CloudApp, provider your credentials:
    
    ```shell
    grab-screen config set cloudapp_username YOUR-USERNAME
    grab-screen config set cloudapp_password
    ```

    Then take a screenshot:
    
    ```shell
    grab-screen image --browse --storage cloudapp
    ```

## Licensing

MIT License
