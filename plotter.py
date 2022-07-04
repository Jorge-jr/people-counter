import matplotlib.dates
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import numpy as np


def time_series_filler(timestamp, series):

    tm = timestamp - np.timedelta64(1, 's')
    if timestamp == np.datetime64('2022-06-26 21:15:17'):
        return 8
    elif tm in series.keys():
        return series[tm]
    else:
        return time_series_filler(tm, series)


time_series = np.arange(np.datetime64('2022-06-26 21:15:17'), np.datetime64('2022-06-26 21:26:00'), np.timedelta64(1, 's'))

with open('snaps.txt') as snaps:
    lines = snaps.readlines()
    # print(len(lines))
    sniffer_series = {np.datetime64('2022-06-26 ' + entry[1]): entry[4][:-1] for entry in [x.split(' ') for x in lines if 'Time' in x]}


ground_true = {np.datetime64('2022-06-26 21:15:17'): 8, np.datetime64('2022-06-26 21:16:30'): 7,
               np.datetime64('2022-06-26 21:17:45'): 5, np.datetime64('2022-06-26 21:18:33'): 4,
               np.datetime64('2022-06-26 21:19:09'): 1, np.datetime64('2022-06-26 21:20:50'): 3,
               np.datetime64('2022-06-26 21:21:30'): 4, np.datetime64('2022-06-26 21:22:22'): 6,
               np.datetime64('2022-06-26 21:23:10'): 7, np.datetime64('2022-06-26 21:23:40'): 5,
               np.datetime64('2022-06-26 21:24:40'): 8}


brief_sniffer_series = {}

for entry in time_series:
    brief_sniffer_series[entry] = time_series_filler(entry, sniffer_series)
    if entry not in ground_true.keys():
        ground_true[entry] = time_series_filler(entry, ground_true)

for val in sniffer_series.keys():
    print(str(sniffer_series[val]) + '-' + str(ground_true[val]))

print(len(time_series), len(ground_true), len(brief_sniffer_series))

'''
fig, ax = plt.subplots()

ax.plot(brief_sniffer_series.values(), label="sniffer")
ax.plot(ground_true.values(), label="ground true")



ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))  # to get a tick every minute
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

ax.legend()

plt.show()
'''