Here are several tutorials on how users will be able to use FireWxPy to make customized weather graphics with a focus on fire weather while having MINIMAL coding proficiency. My motto is: "I want my software to do all the work so you don't have to!"

In FireWxPy users can make graphics in the following categories: NWS Forecasts, Real Time Mesoscale Analysis (RTMA), 
Observed Soundings and Daily Weather Summaries for the previous day for an ASOS. 

These functions download the data, unpack, parse and plot the data automatically. These functions also build the directory that hosts the images and downloads, unzips and files the .SHP files and their components to where they need to go. That is the beauty of FireWxPy, it requires MINIMAL work on the part of the user (remember my motto!). 

If users wish to download and create a lot of graphics at once, the recommended way is to download the data outside of the 
plotting function and pass it into the plotting function. The plotting function will do all the rest of the work such as
parsing the data, plotting the data and building the branches of the directory if the user adds a new FireWxPy function to the
script they are running. 

Here are links to jupyter lab tutorials for all the aforementioned scenarios:

1) First Time User plotting the RTMA Temperature and 24-Hour RTMA Temperature Comparison Across CONUS - [click here](https://github.com/edrewitz/firewxpy/blob/main/tutorials/CONUS_RTMA_Temperature_Example.ipynb)
2) User creates a lot of RTMA plots for the state of California in one script - [click here](https://github.com/edrewitz/firewxpy/blob/main/tutorials/RTMA_CA_Example.ipynb)
3) User creates 3 different types of graphics of the NWS Relative Humidity Forecast across Arizona - [click here](https://github.com/edrewitz/firewxpy/blob/main/tutorials/NWS_RH_Forecasts_AZ_Example.ipynb)
4) User creates a lot of graphics showing the NWS Temperature and RH Forecasts across Texas - [click here](https://github.com/edrewitz/firewxpy/blob/main/tutorials/NWS_Temperature_RH_Forecasts_TX_Example.ipynb)
5) User creates an upper air profiles graphic for San Diego, CA (NKX) - [click here](https://github.com/edrewitz/firewxpy/blob/main/tutorials/NKX_Sounding_Example.ipynb)
6) User creates a daily weather summary graphic for the previous day for Ontario International Airport ASOS (KONT) - [click here](https://github.com/edrewitz/firewxpy/blob/main/tutorials/KONT_Daily_Weather_Summary_Example.ipynb)
7) User creates an upper air profile for a custom date/time. In this example we will look at the onset of Santa Ana Winds in San Diego, CA on October 30th, 2023 00z. - [click here](https://github.com/edrewitz/firewxpy/blob/main/tutorials/Santa_Ana_Wind_Sounding.ipynb)
8) User creates an RTMA Temperature plot for a custom area with a custom reference system. - [click here](https://github.com/edrewitz/firewxpy/blob/main/tutorials/Custom_Plot.ipynb)
9) User creates an RTMA Temperature plot and an 24 Hour RTMA Temperature Comparison graphic for Alaska. - [click here](https://github.com/edrewitz/firewxpy/blob/main/tutorials/Alaska_RTMA_Temperature_Example.ipynb)
10) User creates an RTMA Temperature plot and an 24 Hour RTMA Temperature Comparison graphic for NWS Anchorage East Domain. - [click here](https://github.com/edrewitz/firewxpy/blob/main/tutorials/AER_RTMA_Temperature_Example.ipynb)
11) User creates a lot of RTMA plots for the NWS Anchorage East Domain in one script. - [click here](https://github.com/edrewitz/firewxpy/blob/main/tutorials/RTMA_AER_Example.ipynb)
12) User creates an RTMA Temperature plot and an 24 Hour RTMA Temperature Comparison graphic for Hawaii. - [click here](https://github.com/edrewitz/firewxpy/blob/main/tutorials/Hawaii_RTMA_Temperature_Example.ipynb)
13) User creates graphics for the NWS Maximum Temperature and NWS Minimum Relative Humidity Forecast for Alaska. -[click here](https://github.com/edrewitz/firewxpy/blob/main/tutorials/NWS_AK_example.ipynb)
14) User creates a few graphics for the NWS Forecast for the NWS Juneau Domain. - [click here](https://github.com/edrewitz/firewxpy/blob/main/tutorials/NWS_AJK_example.ipynb)
15) User creates a couple of NWS Forecast graphics for Hawaii. [click here](https://github.com/edrewitz/firewxpy/blob/main/tutorials/NWS_HI_example.ipynb)
16) User creates a few graphics of the NWS Forecast for Oahu. [click here](https://github.com/edrewitz/firewxpy/blob/main/tutorials/NWS_Oahu_example.ipynb)

