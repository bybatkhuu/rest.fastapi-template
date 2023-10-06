# -*- coding: utf-8 -*-

## Standard libraries
import os
import sys

os.chdir("./app")
sys.path.append(os.getcwd())

## Internal modules
from .main import app
from .__version__ import __version__


__all__ = ["app", "__version__"]
