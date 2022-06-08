from setuptools import setup
from randomfiles import __name__, __version__

setup(
    name=__name__,
    version=__version__,
    install_requires=[],
    extras_require={
        "lint": [
            "pylint==2.14.1"
        ],
        "build": [
            "pyinstaller==5.1"
        ]
    }
)
