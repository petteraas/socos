""" socos is a commandline tool for controlling Sonos speakers """

# Will be parsed by setup.py to determine package metadata
__author__ = 'SoCo team <python-soco@googlegroups.com>'
__version__ = '0.2'
__website__ = 'https://github.com/SoCo/socos'
__license__ = 'MIT License'

from .core import SoCos

__all__ = ['SoCos']
