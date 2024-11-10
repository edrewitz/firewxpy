# **Data Access Module**

### **Classes**
1) [RTMA_CONUS]
2) [NDFD_CONUS]

#### RTMA_CONUS Class

This class hosts the active functions that download the 2.5km x 2.5km Real Time Mesoscale Analysis (RTMA) Data. 

This class hosts the functions the users will import and call if the users wish to download the data outside of the 
plotting function and pass the data into the plotting function.

This is the recommended method for users who wish to create a large amount of graphics at one time to limit the number of server requests. 

***Functions***

1) [get_RTMA_dataset()]
2) [get_RTMA_24_hour_comparison_datasets()]
