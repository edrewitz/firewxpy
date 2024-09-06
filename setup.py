import sys
from setuptools import setup, find_packages

if sys.version_info[0] < 3:
  print("ERROR: User is running Python 2.7.\nTo use FireWxPy, the user must be using Python 3.")

setup(
    name = "firewxpy",
    version = "1.0.0",
    package_dir = {"":"src"}
    packages = find_packages(package_dir),
    install_requires=[
        "matplotlib>=3.7",
        "metpy>=1.5.1",
        "netcdf4>=1.7.1",
        "numpy>=1.24",
        "pandas>=2",
        "siphon>=0.9",
        "xarray>=2023.1.0",
        "pysolar>=0.11",
        "pygrib>=2.1.4",
        "cfgrib>=0.9.10.4",
        "cartopy>=0.21.0",
         "imageio>=2.34.0",
    ],
    author="Eric J. Drewitz",
    description="Provides automated weather graphics with a focus on fire weather.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"

)
