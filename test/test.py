# This script simulates downloading data outside of the function and passing it in (for users who want to generate a lot of graphics at once)
# Imports the needed modules and functions
from firewxpy.data_access import FTP_Downloads
from firewxpy import nws_relative_humidity_forecast, nws_temperature_forecast

# Data Access
grbs_maxt, ds_maxt, count_short_maxt, count_extended_maxt = FTP_Downloads.download_NDFD_grids('/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/', 'ds.maxt.bin')
grbs_mint, ds_mint, count_short_mint, count_extended_mint = FTP_Downloads.download_NDFD_grids('/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/', 'ds.mint.bin')
grbs_minrh, ds_minrh, count_short_minrh, count_extended_minrh = FTP_Downloads.download_NDFD_grids('/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/', 'ds.minrh.bin')
grbs_maxrh, ds_maxrh, count_short_maxrh, count_extended_maxrh = FTP_Downloads.download_NDFD_grids('/SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/', 'ds.maxrh.bin')

# Making firewxpy NWS Forecast Graphics
nws_temperature_forecast.plot_extreme_heat_forecast(file_path='ds.maxt.bin', data_array=ds_maxt, count_short=count_short_maxt, count_extended=count_extended_maxt)
nws_temperature_forecast.plot_maximum_temperature_forecast(file_path='ds.maxt.bin', data_array=ds_maxt, count_short=count_short_maxt, count_extended=count_extended_maxt)
nws_temperature_forecast.plot_maximum_temperature_trend_forecast(file_path='ds.maxt.bin', data_array=ds_maxt, count_short=count_short_maxt, count_extended=count_extended_maxt)

nws_temperature_forecast.plot_extremely_warm_low_temperature_forecast(file_path='ds.mint.bin', data_array=ds_mint, count_short=count_short_mint, count_extended=count_extended_mint)
nws_temperature_forecast.plot_frost_freeze_forecast(file_path='ds.mint.bin', data_array=ds_mint, count_short=count_short_mint, count_extended=count_extended_mint)
nws_temperature_forecast.plot_minimum_temperature_forecast(file_path='ds.mint.bin', data_array=ds_mint, count_short=count_short_mint, count_extended=count_extended_mint)
nws_temperature_forecast.plot_minimum_temperature_trend_forecast(file_path='ds.mint.bin', data_array=ds_mint, count_short=count_short_mint, count_extended=count_extended_mint)

nws_relative_humidity_forecast.plot_excellent_overnight_recovery_relative_humidity_forecast(file_path='ds.maxrh.bin', data_array=ds_maxrh, count_short=count_short_maxrh, count_extended=count_extended_maxrh)
nws_relative_humidity_forecast.plot_poor_overnight_recovery_relative_humidity_forecast(file_path='ds.maxrh.bin', data_array=ds_maxrh, count_short=count_short_maxrh, count_extended=count_extended_maxrh)
nws_relative_humidity_forecast.plot_maximum_relative_humidity_forecast(file_path='ds.maxrh.bin', data_array=ds_maxrh, count_short=count_short_maxrh, count_extended=count_extended_maxrh)
nws_relative_humidity_forecast.plot_maximum_relative_humidity_trend_forecast(file_path='ds.maxrh.bin', data_array=ds_maxrh, count_short=count_short_maxrh, count_extended=count_extended_maxrh)

nws_relative_humidity_forecast.plot_low_minimum_relative_humidity_forecast(file_path='ds.minrh.bin', data_array=ds_minrh, count_short=count_short_minrh, count_extended=count_extended_minrh)
nws_relative_humidity_forecast.plot_minimum_relative_humidity_forecast(file_path='ds.minrh.bin', data_array=ds_minrh, count_short=count_short_minrh, count_extended=count_extended_minrh)
nws_relative_humidity_forecast.plot_minimum_relative_humidity_trend_forecast(file_path='ds.minrh.bin', data_array=ds_minrh, count_short=count_short_minrh, count_extended=count_extended_minrh)
'''
nws_temperature_forecast.plot_extreme_heat_forecast(temp_scale_warm_start=80, temp_scale_warm_stop=100, state='me')
nws_temperature_forecast.plot_extremely_warm_low_temperature_forecast(temp_scale_warm_start=60, temp_scale_warm_stop=80, state='me')
nws_temperature_forecast.plot_frost_freeze_forecast(state='me')
nws_temperature_forecast.plot_maximum_temperature_forecast(state='me')
nws_temperature_forecast.plot_maximum_temperature_trend_forecast(state='me')
nws_temperature_forecast.plot_minimum_temperature_forecast(state='me')
nws_temperature_forecast.plot_minimum_temperature_trend_forecast(state='me')

nws_relative_humidity_forecast.plot_excellent_overnight_recovery_relative_humidity_forecast(state='me')
nws_relative_humidity_forecast.plot_low_minimum_relative_humidity_forecast(low_minimum_rh_threshold=50, state='me')
nws_relative_humidity_forecast.plot_maximum_relative_humidity_forecast(state='me')
nws_relative_humidity_forecast.plot_maximum_relative_humidity_trend_forecast(state='me')
nws_relative_humidity_forecast.plot_minimum_relative_humidity_forecast(state='me')
nws_relative_humidity_forecast.plot_minimum_relative_humidity_trend_forecast(state='me')
nws_relative_humidity_forecast.plot_poor_overnight_recovery_relative_humidity_forecast(low_minimum_rh_threshold=60, state='me')
'''