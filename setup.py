import os
import sys

from setuptools import Command, find_packages, setup


def parse_requirements(path):
    with open(path) as file:
        requirements = tuple(filter(lambda line: line and not line.startswith('#'), file))

    return requirements


class LintCommand(Command):
    """Support setup.py lint."""

    description = 'Check the code style.'
    user_options = []

    @staticmethod
    def status(msg):
        """Prints things in bold."""
        sys.stdout.write('\033[1m{0}\033[0m\n'.format(msg))
        sys.stdout.flush()

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.status('Checking flake8 rules...')
        flake8_status = os.system('flake8')

        self.status('Checking bandit rules...')
        bandit_status = os.system('bandit -r .')

        status = 1 if flake8_status or bandit_status else 0
        sys.exit(status)


# load the description from the README file
with open('README.rst') as readme_file:
    long_description = readme_file.read()

# load the python dependencies
main_requirements = parse_requirements('requirements/main.txt')
test_requirements = parse_requirements('requirements/test.txt')

# load the package info
about = {}
with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'grab_screen', 'version.py'))) as version_file:
    exec(version_file.read(), about)

setup(
    name='grab-screen',
    description='Take screenshots and upload anywhere',
    long_description=long_description,
    version=about['__version__'],
    license='MIT',
    url='https://github.com/andrei-shabanski/grab-screen',
    author='Andrei Shabanski',
    author_email='andrei.shabanski@gmail.com',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,

    install_requires=main_requirements,
    tests_require=test_requirements,
    setup_requires=['pytest-runner'],
    extras_require={
        'dev': test_requirements,
    },

    entry_points={
        'console_scripts': [
            'grab-screen=grab_screen:main'
        ]
    },

    cmdclass={
        'lint': LintCommand,
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Graphics :: Capture',
        'Topic :: Multimedia :: Graphics :: Capture :: Screen Capture',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='screenshot image capture grab cloudapp'
)
