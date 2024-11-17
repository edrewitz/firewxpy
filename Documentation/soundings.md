# **Soundings**

### **Functions**
1) [plot_observed_sounding(station_id)](#plot_observed_soundingstation_id)
2) [plot_observed_sounding_custom_date_time(station_id, year, month, day, hour)](#plot_observed_sounding_custom_date_timestation_id-year-month-day-hour)

### plot_observed_sounding(station_id)

This function downloads the latest avaliable sounding data from the University of Wyoming and plots the upper-air profiles. 

Required Arguments: 

1) station_id (String) - The 3 or 4 letter station identifier for the upper-air site. 

Example: San Diego, CA will be entered as plot_observed_sounding('nkx')

Optional Arguments: None

Returns: Saves the upper-air profiles graphic to the Soundings folder. 

### plot_observed_sounding_custom_date_time(station_id, year, month, day, hour)

This function downloads the latest avaliable sounding data from the University of Wyoming and plots the upper-air profiles. 

Required Arguments: 

1) station_id (String) - The 3 or 4 letter station identifier for the upper-air site. 
Example: San Diego, CA will be entered as plot_observed_sounding('nkx')

2) year (Integer) - The four digit year (i.e. 2024)

3) month (Integer) - The one or two digit month. 

4) day (Integer) - The nth day of the month. 

5) hour (Integer) - The hour of the sounding in UTC. 

Optional Arguments: None

Returns: Saves the upper-air profiles graphic to the Soundings folder. 
