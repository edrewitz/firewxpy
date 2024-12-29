# **Solar Information**

**Functions**
[plot_daily_solar_information(latitude, longitude)](#plot_daily_solar_informationlatitude-longitude)

### plot_daily_solar_information(latitude, longitude)

This function plots a daily solar graph and gives other types of solar information. 

Required Arguments: 

1) latitude (Float) - The latitude coordinate in decimal degrees format. 
2) longitude (Float) - The longitude coordinate in decimal degrees format. 

Optional Arguments: None

Return: A graphic showing the following information saved to f:Weather Data/Solar Information:

1) Daily solar elevation graphic
2) A data table showing the following information:
    i) Maximum Daily Solar Elevation (solar-noon sun angle)
    ii) Minimum Daily Solar Elevation (solar-midnight sun angle)
    iii) Difference in daily solar elevation between current day, equinox, summer solstice and winter solstice
    iv) Total Daily Solar Radiation [W/m^2]
