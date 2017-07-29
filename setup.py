from setuptools import setup, find_packages

from grab_screen import __version__

# get the description from the README file
with open('README.md') as readme_file:
    long_description = readme_file.read()

# get the python dependencies
with open('requirements/main.txt') as req_file:
    requirements = req_file.readlines()

setup(
    name='grab-screen',
    description='Take screenshots and upload anywhere',
    long_description=long_description,
    version=__version__,
    license='MIT',
    url='https://github.com/andrei-shabanski/grab-screen',
    author='Andrei Shabanski',
    author_email='andrei.shabanski@gmail.com',
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'grab-screen=grab_screen:main'
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Information Technology',
        'Topic :: Multimedia :: Graphics :: Capture',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='screenshot cloudapp'
)
