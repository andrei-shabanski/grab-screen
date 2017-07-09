from setuptools import setup

from grab_screen import __version__

with open('requirements/main.txt') as req_file:
    requirements = req_file.readlines()

setup(
    name='grab-screen',
    version=__version__,
    py_modules=['grab_screen'],
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        grab-screen=grab_screen:main
    """,
)
