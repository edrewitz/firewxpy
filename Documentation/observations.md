# **Observations**
1) [graphical_daily_summary(station_id)](#graphical_daily_summarystation_id)

### graphical_daily_summary(station_id)

This function creates a graphical daily weather summary and solar information for the previous day's ASOS observations at any particular ASOS site. 

Required Arguments: 1) station_id (String) - The 4-letter station identifier of the ASOS station

Optional Arguments: None

Returns: A saved figure to the observations folder showing a graphical daily weather summary and solar information for the previous day's ASOS observations. 
     The parameters on this daily weather summary are: 
     
     1) Temperature
     2) Relative Humidity
     3) Wind Speed
     4) Solar Elevation Angle
     5) Solar Radiation
