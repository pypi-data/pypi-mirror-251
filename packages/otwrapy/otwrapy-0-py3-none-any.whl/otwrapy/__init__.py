"""
General purpose OpenTURNS python wrapper tools
"""

# flake8: noqa

import os

__author__ = "Felipe Aguirre Martinez"
__copyright__ = "Copyright 2015-2024 Phimeca"
__version__ = "0"
__email__ = "aguirre@phimeca.fr"

base_dir = os.path.dirname(__file__)

from ._otwrapy import *

__all__ = (_otwrapy.__all__)
