from os import path as os_path

from loguru import logger
from setuptools import find_packages
from setuptools import setup


def read_long_description():
    with open('README.md', 'r') as f:
        long_description = f.read()
    return long_description


def read_version():
    version_file = os_path.join(os_path.dirname(__file__), 'chimera', 'version.py')
    with open(version_file) as file:
        exec(file.read())
    version = locals()['__version__']
    logger.debug(f"Building {PACKAGE_NAME} v{version}")
    return version


PACKAGE_NAME = 'zf-chimera'
PACKAGE_VERSION = read_version()
AUTHOR_NAME = 'zeffmuks'
AUTHOR_EMAIL = 'zeffmuks@gmail.com'

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description='chimera simulates the diffusion of innovations in a society',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    install_requires=[
        "wheel",
        "contourpy",
        "cycler",
        "fonttools",
        "Jinja2",
        "kiwisolver",
        "MarkupSafe",
        "matplotlib",
        "mpld3",
        "networkx",
        "numpy",
        "packaging",
        "pillow",
        "pyparsing",
        "python-dateutil",
        "scipy",
        "six"
    ],
    packages=find_packages(
        include=['chimera', 'chimera.*'],
        exclude=['venv', 'venv.*']
    ),
    entry_points={
        'console_scripts': [
            'chimera=chimera.__main__:main'  # Invokes chimera/__main__.py::main()
        ]
    },
)
