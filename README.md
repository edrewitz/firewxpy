
<img width="120" alt="firewxpy logo" src="https://github.com/user-attachments/assets/27d7353c-89ae-4827-a1fb-0d64d80599ad">


# FireWxPy

[![Anaconda-Server Badge](https://anaconda.org/conda-forge/firewxpy/badges/version.svg)](https://anaconda.org/conda-forge/firewxpy)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/firewxpy/badges/latest_release_date.svg)](https://anaconda.org/conda-forge/firewxpy)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/firewxpy/badges/latest_release_relative_date.svg)](https://anaconda.org/conda-forge/firewxpy)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/firewxpy/badges/platforms.svg)](https://anaconda.org/conda-forge/firewxpy)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/firewxpy/badges/license.svg)](https://anaconda.org/conda-forge/firewxpy)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/firewxpy/badges/downloads.svg)](https://anaconda.org/conda-forge/firewxpy)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14318635.svg)](https://doi.org/10.5281/zenodo.14318635)


Thank you for checking out FireWxPy! A user friendly Python package to create visualizations of data specific to fire weather and fire weather forecasting. 

This repository consists of functions to make plots of weather data with an emphasis on fire weather. 

This open source project will help meteorologists download, sort and plot both analysis and forecast data. 

This package focuses on fire weather, however some modules will be universally useful across the entire field of meteorology. 

This package makes it easier for users to access and parse through the 2.5km × 2.5km Real Time Mesoscale Analysis data from the UCAR THREDDS server.

This package makes it easier for users to access and parse through the National Weather Service NDFD gridded forecast data.

This package makes it easier for users to automate their weather graphics since the plotting functions of FireWxPy handle different run times so users will be able to automate their scripts in either the Windows Task Scheduler or a Cron Job.

Copyright (C) Meteorologist Eric J. Drewitz 2024

# Inspiration
This package is largely inspired by the MetPy package which was developed and is currently being maintained by Unidata (please see citation below in the citations section).

# FireWxPy Documentation 
[Documentation Landing Page](https://github.com/edrewitz/firewxpy/edit/main/Documentation/Landing_Page.md)

# Author
Eric J. Drewitz

USDA/USFS Predictive Services Meteorologist

Southern California Geographic Area Coordination Center

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

**Pandas**: 
    author       = {The pandas development team},
    title        = {pandas-dev/pandas: Pandas},
    publisher    = {Zenodo},
    version      = {latest},
    doi          = {10.5281/zenodo.3509134},
    url          = {https://doi.org/10.5281/zenodo.3509134}
}



