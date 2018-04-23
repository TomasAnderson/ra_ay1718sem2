library(dplyr)


setwd("/Volumes/WD/zhouyou/vehicle_location/dec rda")
dt <- load(file = "vehicle_location_morning_20161231_20170101.rda")
veh_loc$log_dt <- as.POSIXct(veh_loc$log_dt)

atimeframe <- subset(veh_loc,
                     log_dt >= as.POSIXct('2016-12-31 08:00:00') &
                       log_dt <= as.POSIXct('2016-12-31 08:05:00')
)
btimeframe <- subset(veh_loc,
                     log_dt >= as.POSIXct('2016-12-31 10:55:00') &
                       log_dt <= as.POSIXct('2016-12-31 11:00:00')
)

out <- rbind(atimeframe, btimeframe)
write.csv(out, file = "./processed/2016-12-31.csv")
