""" Package setup."""
from pathlib import Path
from pathlib import PurePath

from setuptools import setup
from setuptools import find_packages

_HERE = PurePath(__file__).parent
_PATH_VERSION = Path() / _HERE / "pubsubs" / "__version__.py"

about = {}
with open(_PATH_VERSION) as file:
    exec(file.read(), about)

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    url="https://github.com/revolut-engineering/pubsubs",
    install_requires=about["__dependencies__"],
    extras_require={
        "kafka": ["confluent_kafka"],
        "dev": ["flake8", "pytest", "black"]
    },
    packages=find_packages(include=["pubsubs"]),
    python_requires=">=3.6",
)
