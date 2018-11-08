import ephem
import numpy as np
import matplotlib.pylab as plt, matplotlib.dates as mdates
import datetime as dt
"""
Calculates sunrise and sunset data for a calendar year and displays them in a nice plot

Disclaimer: This script is for educational purposes only.
            Please do not fetch huge amounts of data from public web servers unnecessarily!
            Instead, use local files if possible.
"""

# Let's make a function that gets all the sunrise and sunset times for a place and a year:
def sunrisetimes(value, year=2018):
  obs=ephem.Observer()
  if len(value)==5:
    obs.elevation=value[4]
  obs.lon,obs.lat=('%f'%(value[0]+value[1]/60),'%f'%(value[2]+value[3]/60))
  srise=[]
  sset=[]
  dates=mdates.drange(dt.datetime(year,1,1,12),dt.datetime(year+1,1,1,12),dt.timedelta(1))
  for single_date in dates:
    obs.date=mdates.num2date(single_date)
    srise.append(obs.previous_rising(ephem.Sun())%1+dates[0])
    sset.append(obs.next_setting(ephem.Sun())%1+dates[1])
  return dates,srise, sset

year=2018

# Dictionary. Key is the place name label, value is a 5-tuple containing
# - Longitude West in Degrees and Minutes, then
# - Latitude North in Degrees and Minutes and then
# - elevation above sea level in m (optional
places={"Greenwich": (0, 0, 51, 29), "Zurich": (8, 33, 47, 22, 408)}

# Create a nice plot for both series:
ax=plt.subplot(111)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
ax.yaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.yaxis.set_major_locator(mdates.HourLocator(interval=2))

# Loop through the places and the colors:
for idx,(key, value) in enumerate(places.items()):
  # Call the sunrisetimes function:
  dates,sunrise, sunset=sunrisetimes(value)

  # Plot the returned data as line plots:
  ax.plot(dates, sunrise, label=key, color='C%d'%(idx%10))
  ax.plot(dates, sunset, color='C%d'%(idx%10))

  # Puts a fill between the sunrise and sunset line plots:
  ax.fill_between(dates, sunrise, sunset, facecolor='C%d'%(idx%10), alpha=0.2, interpolate=True)

# Tweak plot title and axis labels:
plt.title('Sunlight hours %d'%year)
plt.xticks(np.linspace(dates[0],dates[-1],10))
plt.xlabel('date')

# # activate if y axis should range from 0h to 24h
# plt.ylim([dates[0]+0.5,dates[1]+0.5])
plt.ylabel('time')

plt.legend()
plt.tight_layout()
# plt.savefig('final2.png', dpi=90)
plt.show()
