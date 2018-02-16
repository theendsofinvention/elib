"""
Placeholder for future personal library
"""
import logging

from pkg_resources import DistributionNotFound, get_distribution

LOGGER = logging.getLogger('ELIB')
LOGGER.addHandler(logging.NullHandler())

from . import config, console, custom_logging, custom_random, downloader, hash_, paste, path, settings, tts
from ._run import run
from .pretty import pretty_format

try:
    __version__ = get_distribution('elib').version
except DistributionNotFound:  # pragma: no cover
    # package is not installed
    __version__ = 'not installed'
