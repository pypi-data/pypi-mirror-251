
"""
This module is the entry point for the mtbp3 package.
It imports all the functions and classes from the util module.
"""

# read version from installed package
from importlib.metadata import version
__version__ = version(__package__)

from .util import *


