Grab Screen
===========

.. image:: https://api.codacy.com/project/badge/Grade/0f2d7aaac9684b728fd45fbab2fbca3b
    :target: https://www.codacy.com/app/andrei-shabanski/grab-screen?utm_source=github.com&utm_medium=referral&utm_content=andrei-shabanski/grab-screen&utm_campaign=badger
.. image:: https://travis-ci.org/andrei-shabanski/grab-screen.svg?branch=master
    :target: https://travis-ci.org/andrei-shabanski/grab-screen
.. image:: https://img.shields.io/pypi/pyversions/grab-screen.svg
    :target: https://pypi.python.org/pypi/grab-screen
.. image:: https://img.shields.io/pypi/l/grab-screen.svg
    :target: https://github.com/andrei-shabanski/grab-screen/blob/master/LICENSE

Take screenshots and upload anywhere!

Installing
----------

You install ``grab-screen`` with pip:

.. code:: shell

    $ pip install grab-screen

Usage
-----

.. code:: shell

    $ grab-screen --help
    Usage: grab-screen [OPTIONS] COMMAND [ARGS]...

    Options:
      -h, --help     Show this message and exit.
      -v, --version  Show the version and exit.

    Commands:
      config  Get and set options.
      image   Make a screenshot and upload to a storage.

Configurations
^^^^^^^^^^^^^^

``$ grab-screen config list`` - show configs.

``$ grab-screen config set NAME [VALUE]`` - set an option. You can add
``--upset`` to remove the option.

``$ grab-screen config reset`` - remove all options.

Taking screenshots
^^^^^^^^^^^^^^^^^^

``$ grab-screen image`` - take a screenshot.

Use ``-h``/``--help`` to see more options.

Storages
--------

**CloudApp**

    Before uploading screenshots to CloudApp, provider your credentials:

    .. code:: shell

        $ grab-screen config set cloudapp_username YOUR-USERNAME
        $ grab-screen config set cloudapp_password

    Then take a screenshot:

    .. code:: shell

        $ grab-screen image --browse --storage cloudapp

Licensing
---------

MIT License
