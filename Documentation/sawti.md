# **SANTA ANA WILDFIRE THREAT INDEX**

### sawti()
        
This function calculates the The Santa Ana Wildfire Threat Index from Rolinski et al. 2016. The function downloads the .CSV files holding the data, performs the Large Fire Potential (LFP) calculation and makes a bar graph
for each zone. 

Literature Citation: Rolinski, T., S. B. Capps, R. G. Fovell, Y. Cao, B. J. D’Agostino, and S. Vanderburg, 2016: The Santa Ana Wildfire Threat Index: Methodology and Operational Implementation. Wea. Forecasting, 31, 1881–1897, https://doi.org/10.1175/WAF-D-15-0141.1.

Required Arguments: None

Optional Arguments: 

1) zone_1_threshold_1 (Integer) - Default = 10. This is the LFP threshold that seprates no rating (green zone) and a marginal risk (yellow zone) for zone 1. 
2) zone_1_threshold_2 (Integer) - Default = 15. This is the LFP threshold that seprates a marginal risk (yellow zone) and a moderate risk (orange zone) for zone 1. 
3) zone_1_threshold_3 (Integer) - Default = 21. This is the LFP threshold that seprates a moderate risk (orange zone) and a high risk (red zone) for zone 1. 
4) zone_1_threshold_4 (Integer) - Default = 40. This is the LFP threshold that seprates a high risk (red zone) and an extreme risk (purple zone) for zone 1. 
5) zone_2_threshold_1 (Integer) - Default = 9. This is the LFP threshold that seprates no rating (green zone) and a marginal risk (yellow zone) for zone 2. 
6) zone_2_threshold_2 (Integer) - Default = 13. This is the LFP threshold that seprates a marginal risk (yellow zone) and a moderate risk (orange zone) for zone 2. 
7) zone_2_threshold_3 (Integer) - Default = 20. This is the LFP threshold that seprates a moderate risk (orange zone) and a high risk (red zone) for zone 2. 
8) zone_2_threshold_4 (Integer) - Default = 28. This is the LFP threshold that seprates a high risk (red zone) and an extreme risk (purple zone) for zone 2. 
9) zone_3_threshold_1 (Integer) - Default = 10. This is the LFP threshold that seprates no rating (green zone) and a marginal risk (yellow zone) for zone 3. 
10) zone_3_threshold_2 (Integer) - Default = 16. This is the LFP threshold that seprates a marginal risk (yellow zone) and a moderate risk (orange zone) for zone 3. 
11) zone_3_threshold_3 (Integer) - Default = 24. This is the LFP threshold that seprates a moderate risk (orange zone) and a high risk (red zone) for zone 3. 
12) zone_3_threshold_4 (Integer) - Default = 36. This is the LFP threshold that seprates a high risk (red zone) and an extreme risk (purple zone) for zone 3. 
13) zone_4_threshold_1 (Integer) - Default = 9. This is the LFP threshold that seprates no rating (green zone) and a marginal risk (yellow zone) for zone 4. 
14) zone_4_threshold_2 (Integer) - Default = 12. This is the LFP threshold that seprates a marginal risk (yellow zone) and a moderate risk (orange zone) for zone 4. 
15) zone_4_threshold_3 (Integer) - Default = 15. This is the LFP threshold that seprates a moderate risk (orange zone) and a high risk (red zone) for zone 4. 
16) zone_4_threshold_4 (Integer) - Default = 25. This is the LFP threshold that seprates a high risk (red zone) and an extreme risk (purple zone) for zone 4.
17) zone_1_W_weight (Float or Integer) - Default = 1. This is the weight to multiply the wind-squared value by for zone 1. 
18) zone_1_DD_weight (Float or Integer) - Default = 1. This is the weight to multiply the dew point depression value by for zone 1. 
19) zone_1_FMC_weight (Float or Integer) - Default = 1. This is the weight to multiply the fuel moisture component value by for zone 1. 
20) zone_2_W_weight (Float or Integer) - Default = 1. This is the weight to multiply the wind-squared value by for zone 2. 
21) zone_2_DD_weight (Float or Integer) - Default = 1. This is the weight to multiply the dew point depression value by for zone 2. 
22) zone_2_FMC_weight (Float or Integer) - Default = 1. This is the weight to multiply the fuel moisture component value by for zone 2. 
23) zone_3_W_weight (Float or Integer) - Default = 1. This is the weight to multiply the wind-squared value by for zone 3. 
24) zone_3_DD_weight (Float or Integer) - Default = 1. This is the weight to multiply the dew point depression value by for zone 3. 
25) zone_3_FMC_weight (Float or Integer) - Default = 1. This is the weight to multiply the fuel moisture component value by for zone 3. 
26) zone_4_W_weight (Float or Integer) - Default = 1. This is the weight to multiply the wind-squared value by for zone 4. 
27) zone_4_DD_weight (Float or Integer) - Default = 1. This is the weight to multiply the dew point depression value by for zone 4. 
28) zone_4_FMC_weight (Float or Integer) - Default = 1. This is the weight to multiply the fuel moisture component value by for zone 4. 

Returns: A graphic showing the LFP forecast for each zone saved to f:Weather Data/SAWTI. 
