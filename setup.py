import sys
from setuptools import setup, find_packages

if sys.version_info[0] < 3:
  print("ERROR: User is running Python 2.7.\nTo use FireWxPy, the user must be using Python 3.")

setup()
