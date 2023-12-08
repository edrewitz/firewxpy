# FireWxPy
This repository consists of functions to make plots of weather data with an emphasis on fire weather. 

This open source project will help meteorologists download, sort and plot both analysis and forecast data. 

This package focuses on fire weather, however some modules will be universally useful across the entire field of meteorology. 

This package makes it easier for users to access and parse through the 2.5km × 2.5km Real Time Mesoscale Analysis data from the UCAR THREDDS server.

This package makes it easier for users to access and parse through the National Weather Service NDFD gridded forecast data.

This package makes it easier for users to automate their weather graphics since the plotting functions of FireWxPy handle different run times so users will be able to automate their scripts in either the Windows Task Scheduler or a Cron Job.

Copyright (C) Eric J. Drewitz 2023

# Inspiration
This package is largely inspired by the MetPy package which was developed and is currently being maintained by Unidata (please see citation below in the citations section).

# Python Module Dependencies
1. PyGrib
2. Xarray
3. os
4. ftplib
5. MetPy
6. Siphon
7. NumPy
8. cartopy

# FireWxPy Documentation 
https://github.com/edrewitz/FireWxPy/blob/main/FireWxPy_docs.md

# Citations

**MetPY**: May, R. M., Goebbert, K. H., Thielen, J. E., Leeman, J. R., Camron, M. D., Bruick, Z.,
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

**NumPy**: Harris, C.R., Millman, K.J., van der Walt, S.J. et al. Array programming with NumPy. Nature 585, 357–362 (2020). DOI: 10.1038/s41586-020-2649-2. (Publisher link).




