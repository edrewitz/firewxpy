
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

Copyright (C) Meteorologist Eric J. Drewitz 2025

# Inspiration
This package is largely inspired by the MetPy package which was developed and is currently being maintained by Unidata (please see citation below in the citations section).

# FireWxPy Documentation 

**Table Of Contents**

This is the landing page for all of the firewxpy documentation. The links below will direct you to the documentation for each firewxpy module. 

To visit the firewxpy tutorials page where you can see examples in jupyter lab - [click here](https://github.com/edrewitz/FireWxPy-Jupyter-Labs/blob/main/Examples_Guide.md)

For video tutorials/demostrations checkout the FireWxPy Tutorial Series on the South Ops YouTube Channel - [click here](https://www.youtube.com/playlist?list=PLLKWSry9WlbPfeTWEQjuKIdNhYuxd8r96)

**FireWxPy Graphics Classes And Functions**

1) [rtma](https://github.com/edrewitz/firewxpy/blob/main/Documentation/RTMA.md)
2) [spc](https://github.com/edrewitz/firewxpy/blob/main/Documentation/SPC_Outlook_Graphics.md)
3) [nws_temperature_forecast](https://github.com/edrewitz/firewxpy/blob/main/Documentation/NWS_Forecasts.md#temperature-class)
4) [nws_relative_humidity_forecast](https://github.com/edrewitz/firewxpy/blob/main/Documentation/NWS_Forecasts.md#relative-humidity-class)
5) [nws_critical_firewx_forecast](https://github.com/edrewitz/firewxpy/blob/main/Documentation/NWS_Forecasts.md#critical-fire-weather-class)
6) [model_dynamics](https://github.com/edrewitz/firewxpy/blob/main/Documentation/forecast_models.md#dynamics-class)
7) [model_temperature](https://github.com/edrewitz/firewxpy/blob/main/Documentation/forecast_models.md#temperature-class)
8) [model_relative_humidity](https://github.com/edrewitz/firewxpy/blob/main/Documentation/forecast_models.md#relative-humidity-class)
9) [model_critical_firewx_conditions](https://github.com/edrewitz/firewxpy/blob/main/Documentation/forecast_models.md#critical-firewx-conditions-class)
10) [model_precipitation](https://github.com/edrewitz/firewxpy/blob/main/Documentation/forecast_models.md#precipitation-class)
11) [time_cross_sections](https://github.com/edrewitz/firewxpy/blob/main/Documentation/cross_sections.md#time-cross-sections)
12) [two_point_cross_sections](https://github.com/edrewitz/firewxpy/blob/main/Documentation/cross_sections.md#cross-sections-between-two-points)
13) [gridded_obs](https://github.com/edrewitz/firewxpy/blob/main/Documentation/observations.md#gridded-observations-class)
14) [scatter_obs](https://github.com/edrewitz/firewxpy/blob/main/Documentation/observations.md#scatter-plot-observations-class)
15) [metar_obs](https://github.com/edrewitz/firewxpy/blob/main/Documentation/observations.md#metar-observations-class)
16) [plot_observed_sounding](https://github.com/edrewitz/firewxpy/blob/main/Documentation/soundings.md#plot_observed_soundingstation_id)
17) [plot_observed_sounding_custom_date_time](https://github.com/edrewitz/firewxpy/blob/main/Documentation/soundings.md#plot_observed_sounding_custom_date_timestation_id-year-month-day-hour)
18) [plot_forecast_soundings](https://github.com/edrewitz/firewxpy/blob/main/Documentation/soundings.md#plot_forecast_soundingsmodel-station_id)
19) [sawti](https://github.com/edrewitz/firewxpy/blob/main/Documentation/sawti.md)
20) [plot_daily_solar_information](https://github.com/edrewitz/firewxpy/blob/main/Documentation/solar_information.md#plot_daily_solar_informationlatitude-longitude)
21) [fuels charts](https://github.com/edrewitz/firewxpy/blob/main/Documentation/fuels_charts.md)
22) [ensemble_8_day_mean_eofs](https://github.com/edrewitz/firewxpy/blob/main/Documentation/forecast_models.md#ensemble-8-day-mean-and-eofs)

**Additional Resources For Users Who Download The Data Outside Of The Function And Pass It In**

*This is recommended for users generating a lot of graphics with the same dataset (i.e. a lot of RTMA graphics etc.)*

*This method reduces the amount of data requests on the servers hosting the data*

1) [RTMA (Data Access)](https://github.com/edrewitz/firewxpy/blob/main/Documentation/miscellaneous.md#rtma)
2) [NDFD_GRIDS (Data Access)](https://github.com/edrewitz/firewxpy/blob/main/Documentation/miscellaneous.md#ndfd_grids)
3) [obs (Data Access)](https://github.com/edrewitz/firewxpy/blob/main/Documentation/miscellaneous.md#obs)
4) [model_data (Data Access)](https://github.com/edrewitz/firewxpy/blob/main/Documentation/miscellaneous.md#model_data)
5) [FEMS (Data Access)](https://github.com/edrewitz/firewxpy/blob/main/Documentation/miscellaneous.md#fems)
6) [plot_creation_time](https://github.com/edrewitz/firewxpy/blob/main/Documentation/miscellaneous.md#plot_creation_time)
7) [get_metar_mask](https://github.com/edrewitz/firewxpy/blob/main/Documentation/miscellaneous.md#get_metar_maskstate-gacc_region-rtma_wsfalse)

**Regional Abbreviations for Model Data**

If the user wants to analyze model data in the U.S. the regional abbreviations consist of the following:

- CONUS & South Canada & North Mexico
- CONUS
- NA
- 2-letter state abbreviation
- 4-letter Geographic Area Coordination Center abbreviation

If the user wants to analyze model data for an area outside of the U.S:

*One important thing to note is only global models (GFS, GEFS etc.) are available here*

International Regional Selections:

- Canada
- Mexico & Central America
- Caribbean
- South America
- Western Europe & Iceland
- Central & Eastern Europe
- West Africa
- Saharan Africa
- Sub Saharan Africa
- Middle East
- Asia
- East Asia
- Southeast Asia
- India
- Australia New Zealand
- Guyana

# Author
Eric J. Drewitz

USDA/USFS Predictive Services Meteorologist

Southern California Geographic Area Coordination Center

# Citing FireWxPy

[click here](https://zenodo.org/records/15620392) to find information on how to cite FireWxPy. 

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

**geopandas**: Kelsey Jordahl, Joris Van den Bossche, Martin Fleischmann, Jacob Wasserman, James McBride, Jeffrey Gerard, … François Leblanc. (2020, July 15). geopandas/geopandas: v0.8.1 (Version v0.8.1). Zenodo. http://doi.org/10.5281/zenodo.3946761


