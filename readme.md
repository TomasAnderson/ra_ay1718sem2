## File hierachy

- `lib/`: shape files used to mapping from latitude/longtitude to planning area
- `notebook`: jupyter notebook for data visualisation and illustration of driver pattern
- `src`: source code for two tasks
  - driver pattern analysis
  - supply estimation
- `document` some useful mappings such as postal2zone and weather

## Supply Estimation

We estimate the supply for each region in a time interval by counting the number of available cars. The scripts should be run in the following order

1. `sample_free_vehicle.py` Given raw data files and time intervals (e.g. 8:00-8:05), select rows that only when the status is **FREE**. 
2. `map_loc_to_sub_zone.py` Map the latitude/longtitue to planning area
3. `aggregate_supply.py` Output supply per time interval per planning area. 

## Driver Pattern Analysis

We study the driver's pattern in terms of their customer seeking and time distribution. 

To start with, it is best to look at two notebooks. Install iPython and enter the command `jupyter notebook`

The purpose of all scripts are listed here: 

* `sample_individual_driver.py` and `sample_multiple_driver.py` It reads all raw data files and aggregate one or multiple drivers. 
* `sample_driver_over_time` calculate the driver's time distribution ovver different activities
* `aggregate_info` calculate the driver's customer seeking meta information