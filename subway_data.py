import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np


def create_mean_per_hour(df ,set_names,column):
    """From DataFrame creates DataFrame with columns with mean values by column per hour"""
    mean_per_hours = []
    for unit in set_names:
        d = dict()
        d['UNIT'] = unit
        d['00:00:00'] = np.mean(df[df['UNIT'] == unit][df['hour'] == 0][column])
        d['4:00:00'] = np.mean(df[df['UNIT'] == unit][df['hour'] == 4][column])
        d['8:00:00'] = np.mean(df[df['UNIT'] == unit][df['hour'] == 8][column])
        d['12:00:00'] = np.mean(df[df['UNIT'] == unit][df['hour'] == 12][column])
        d['16:00:00'] = np.mean(df[df['UNIT'] == unit][df['hour'] == 16][column])
        d['20:00:00'] = np.mean(df[df['UNIT'] == unit][df['hour'] == 20][column])
        d['Total mean'] = np.mean(df[df['UNIT'] == unit][column])
        mean_per_hours.append(d)
    return pd.DataFrame(mean_per_hours)


def mean_per_col(df, names, column):
    """From DataFrame Creates DataFrame with column with mean values"""
    mean = []
    for unit in names:
        d = dict()
        d['UNIT'] = unit
        d['Value'] = np.mean(df[df['UNIT'] == unit][column])
        mean.append(d)
    return pd.DataFrame(mean)


# Read csv file as pandas DataFrame
subway_weather_df = pd.read_csv('turnstile_weather_v2.csv')

# Subway station corresponding to the remote unit.
stations = set(subway_weather_df['station'])

# Remote unit that collects turnstile information. Can collect from multiple banks of turnstiles. Large
# subway stations can have more than one unit.
units = set(subway_weather_df['UNIT'])

# Temperature series
temperature_series = subway_weather_df['meantempi']
# Entries series
entries_series = subway_weather_df['ENTRIESn']

# Correlation between temperature and entries
corr_temp_entr = subway_weather_df[['meantempi', 'ENTRIESn']].corr()
print('Correlation between temperature and entries')
print(corr_temp_entr)

# Correlation between Barometric pressure and entries
corr_ber_pressure_entr = subway_weather_df[['pressurei', 'ENTRIESn']].corr()
print('Correlation between barometric pressure and entries')
print(corr_ber_pressure_entr)

# Mean values of ENTRIESn_hourly and EXITn_hourly by hours each 4 hours
# mean_entries_per_hour = create_mean_per_hour(subway_weather_df, units, 'ENTRIESn_hourly')
# mean_exits_per_hour = create_mean_per_hour(subway_weather_df, units, 'EXITSn_hourly')

# Write DataFrames to pickle
# mean_entries_per_hour.to_pickle('mean_entries_hour.pickle')
# mean_exits_per_hour.to_pickle('mean_exits_per_hour.pickle')

# Read data from pickle
mean_entries_per_hour_df = pd.read_pickle('mean_entries_hour.pickle')
mean_exits_per_hour_df = pd.read_pickle('mean_exits_per_hour.pickle')

# Mean values ENTRIESn and EXITSn
# mean_ENTRIESn = mean_per_col(subway_weather_df, units, 'ENTRIESn')
# mean_EXITSn = mean_per_col(subway_weather_df, units, 'EXITSn')

# Write to pickle
# mean_ENTRIESn.to_pickle('mean_ENTRIESn.pickle')
# mean_EXITSn.to_pickle('mean_EXITSn.pickle')

# Read mean_ENTRIESn.pickle mean_EXITSn.pickle
mean_ENTRIESn_df = pd.read_pickle('mean_ENTRIESn.pickle')
mean_EXITSn_df = pd.read_pickle('mean_EXITSn.pickle')

# Get lat, lon
units_lat = mean_per_col(subway_weather_df, units, 'latitude')
units_lon = mean_per_col(subway_weather_df, units, 'longitude')
# Assign it
mean_ENTRIESn_df['latitude'] = units_lat['Value']
mean_ENTRIESn_df['longitude'] = units_lon['Value']
mean_EXITSn_df['latitude'] = units_lat['Value']
mean_EXITSn_df['longitude'] = units_lon['Value']

# Visualisation for EXITS
m = Basemap(projection="mill", resolution='f', llcrnrlon= -74.2, llcrnrlat= 40.5,urcrnrlon= -73.6, urcrnrlat=40.9)
for unit in mean_EXITSn_df.values:
    xpt, ypt = m(unit[3], unit[2])
    m.plot(xpt, ypt, 'r.', ms=unit[1]/ 2500000, alpha=1/unit[1] + 0.7)
m.drawcoastlines()
m.bluemarble()
plt.title("NYC subway stations EXIT")
plt.savefig("NYC_subway_stations_EXITS")

# Visualisation for ENTRIES
m = Basemap(projection="mill", resolution='f', llcrnrlon= -74.2, llcrnrlat= 40.5,urcrnrlon= -73.6, urcrnrlat=40.9)
for unit in mean_ENTRIESn_df.values:
    xpt, ypt = m(unit[3], unit[2])
    m.plot(xpt, ypt, 'r.', ms=unit[1]/ 2500000, alpha=1/unit[1] + 0.7)
m.drawcoastlines()
m.bluemarble()
plt.title("NYC subway stations ENTRIES")
plt.savefig("NYC_subway_stations_ENTRIES")



