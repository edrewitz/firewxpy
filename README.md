
<img width="200" alt="firewxpy logo" src="https://github.com/user-attachments/assets/27d7353c-89ae-4827-a1fb-0d64d80599ad"> ![image](https://github.com/user-attachments/assets/da1b43c0-2b6a-4a5c-9eb4-f08b30cab42b)


# FireWxPy

[![Conda Version](https://img.shields.io/conda/vn/conda-forge/firewxpy.svg)](https://anaconda.org/conda-forge/firewxpy)
![PyPI](https://img.shields.io/pypi/v/firewxpy?label=pypi%20firewxpy)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/firewxpy/badges/latest_release_date.svg)](https://anaconda.org/conda-forge/firewxpy)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/firewxpy/badges/latest_release_relative_date.svg)](https://anaconda.org/conda-forge/firewxpy)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/firewxpy/badges/platforms.svg)](https://anaconda.org/conda-forge/firewxpy)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/firewxpy/badges/license.svg)](https://anaconda.org/conda-forge/firewxpy)
[![Conda Recipe](https://img.shields.io/badge/recipe-firewxpy-green.svg)](https://anaconda.org/conda-forge/firewxpy) 
      <a href="https://dev.azure.com/conda-forge/feedstock-builds/_build/latest?definitionId=23735&branchName=main">
        <img src="https://dev.azure.com/conda-forge/feedstock-builds/_apis/build/status/firewxpy-feedstock?branchName=main">
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14318635.svg)](https://doi.org/10.5281/zenodo.14318635)


Anaconda Downloads: 

[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/firewxpy.svg)](https://anaconda.org/conda-forge/firewxpy)

PIP Downloads:

![PyPI - Downloads](https://img.shields.io/pypi/dm/firewxpy)

Thank you for checking out FireWxPy! An open-source user friendly Python package to create visualizations of data specific to fire weather and fire weather forecasting. 
There are also graphics in FireWxPy that can be used in the meteorological field universally as well. 

This package makes it easy for meteorologists to create analysis & forecast graphics specific to their needs. 

Copyright (C) Meteorologist Eric J. Drewitz 2024-2026

***Table of Contents***

1) [Documentation](https://github.com/edrewitz/firewxpy/tree/main#documentation)
2) [Jupyter Lab Tutorials](https://github.com/edrewitz/firewxpy/tree/main#jupyter-lab-tutorials)
3) [Citations](https://github.com/edrewitz/firewxpy/tree/main#citations)


# Documentation

***Observational Data***
1) [Soundings](https://github.com/edrewitz/firewxpy/blob/main/Documentation/firewxpy%202.0/observed%20soundings.md#observed-soundings)
2) [Vertical Profiles](https://github.com/edrewitz/firewxpy/blob/main/Documentation/firewxpy%202.0/vertical%20profiles.md#observed-vertical-profiles)

# Jupyter Lab Tutorials

***Observational Data***
1) [Observed Soundings (Current and Archived)](https://github.com/edrewitz/FireWxPy-Jupyter-Labs/blob/main/FireWxPy%202%20Tutorials/observed_soundings.ipynb)
2) [Vertical Profiles (Current and Archived)](https://github.com/edrewitz/FireWxPy-Jupyter-Labs/blob/main/FireWxPy%202%20Tutorials/vertical_profiles.ipynb)

# Installation Instructions

**How To Install**

Copy and paste either command into your terminal or anaconda prompt:

*Install via Anaconda*

`conda install firewxpy`

*Install via pip*

`pip install firewxpy`

**How To Update To The Latest Version**

Copy and paste either command into your terminal or anaconda prompt:

*Update via Anaconda*

***This is for users who initially installed FireWxPy through Anaconda***

`conda update firewxpy`

*Update via pip*

***This is for users who initially installed FireWxPy through pip***

`pip install --upgrade firewxpy`

***FireWxPy < 2.0 is Depreciated***

[Click Here for the legacy FireWxPy < 2.0 Documentation](https://github.com/edrewitz/firewxpy/blob/main/Documentation/firewxpy%201.0/Landing_Page.md#table-of-contents)

# Citations

**MetPy**: May, R. M., Goebbert, K. H., Thielen, J. E., Leeman, J. R., Camron, M. D., Bruick, Z.,
    Bruning, E. C., Manser, R. P., Arms, S. C., and Marsh, P. T., 2022: MetPy: A
    Meteorological Python Library for Data Analysis and Visualization. Bull. Amer. Meteor.
    Soc., 103, E2273-E2284, https://doi.org/10.1175/BAMS-D-21-0125.1.

**xarray**: Hoyer, S., Hamman, J. (In revision). Xarray: N-D labeled arrays and datasets in Python. Journal of Open Research Software.

**pygrib**: Jeff Whitaker, daryl herzmann, Eric Engle, Josef Kemetmüller, Hugo van Kemenade, Martin Zackrisson, Jos de Kloe, Hrobjartur Thorsteinsson, Ryan May, Benjamin R. J. Schwedler, OKAMURA Kazuhide, ME-Mark-O, Mike Romberg, Ryan Grout, Tim Hopper, asellappenIBM, Hiroaki Itoh, Magnus Hagdorn, & Filipe. (2021). jswhit/pygrib: version 2.1.4 release (v2.1.4rel). Zenodo. https://doi.org/10.5281/zenodo.5514317

**siphon**: May, R. M., Arms, S. C., Leeman, J. R., and Chastang, J., 2017:
    Siphon: A collection of Python Utilities for Accessing Remote Atmospheric
    and Oceanic Datasets. Unidata, Accessed 30 September 2017.
    [Available online at https://github.com/Unidata/siphon.]
    doi:10.5065/D6CN72NW.

**cartopy**: Phil Elson, Elliott Sales de Andrade, Greg Lucas, Ryan May, Richard Hattersley, Ed Campbell, Andrew Dawson, Bill Little, Stephane Raynaud, scmc72, Alan D. Snow, Ruth Comer, Kevin Donkers, Byron Blay, Peter Killick, Nat Wilson, Patrick Peglar, lgolston, lbdreyer, … Chris Havlin. (2023). SciTools/cartopy: v0.22.0 (v0.22.0). Zenodo. https://doi.org/10.5281/zenodo.8216315

**SAWTI**: Rolinski, T., S. B. Capps, R. G. Fovell, Y. Cao, B. J. D’Agostino, and S. Vanderburg, 2016: The Santa Ana Wildfire Threat Index: Methodology and Operational Implementation. Wea. Forecasting, 31, 1881–1897, https://doi.org/10.1175/WAF-D-15-0141.1.

**NumPy**: Harris, C.R., Millman, K.J., van der Walt, S.J. et al. Array programming with NumPy. Nature 585, 357–362 (2020). DOI: 10.1038/s41586-020-2649-2. (Publisher link).

**PySolar**: Stafford, B. et. al, PySolar (2007), [https://pysolar.readthedocs.io/en/latest/#contributors] 

**Pandas**: Pandas: McKinney, W., & others. (2010). Data structures for statistical computing in python. In Proceedings of the 9th Python in Science Conference (Vol. 445, pp. 51–56).

**xeofs**: xeofs: Rieger, N. & Levang, S. J. (2024). xeofs: Comprehensive EOF analysis in Python with xarray. Journal of Open Source Software, 9(93), 6060. DOI: https://doi.org/10.21105/joss.06060

**WxData**: Eric J. Drewitz. (2026). edrewitz/WxData: WxData 2.0.1 (WxData2.0.1). Zenodo. https://doi.org/10.5281/zenodo.20350029

**shapeography**: Eric J. Drewitz. (2026). edrewitz/shapeography: Shapeography 1.2 Released (shapeography1.2). Zenodo. https://doi.org/10.5281/zenodo.19141532

**geopandas**: Kelsey Jordahl, Joris Van den Bossche, Martin Fleischmann, Jacob Wasserman, James McBride, Jeffrey Gerard, … François Leblanc. (2020, July 15). geopandas/geopandas: v0.8.1 (Version v0.8.1). Zenodo. http://doi.org/10.5281/zenodo.3946761


