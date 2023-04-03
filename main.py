import re
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

with open('CIties.txt', 'r') as f:
    city_names = []
    latitudes = []
    longitudes = []
    gp = []

    for line in f:
        parts = line.strip().split(',')
        city_names.append(parts[0])
        latitudes.append(parts[1])

        longitudes.append(parts[2])

    for city in city_names:
        country = city.strip().split('-')
        gp.append(country[0])

latitudes = [float(re.findall(r'-?\d+\.\d+', lat)[0]) * (-1 if re.findall(r'[A-Za-z]+', lat)[0] == 'S' else 1) for lat in latitudes]
longitudes = [float(re.findall(r'-?\d+\.\d+', long)[0]) * (-1 if re.findall(r'[A-Za-z]+', long)[0] == 'W' else 1) for long in longitudes]




print(latitudes)
print(longitudes)
print(gp)
m = Basemap(projection='merc', llcrnrlon=-180, llcrnrlat=-80, urcrnrlon=180, urcrnrlat=80)

# Draw coastlines, countries, and other features on the map
m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='lightgray', lake_color='white')

# Plot the cities on the map
x, y = m(longitudes, latitudes)

x_min, x_max = min(x), max(x)
y_min, y_max = min(y), max(y)

ax = plt.gca()
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

m.plot(x, y, 'ro', markersize=5)

for name, xpt, ypt in zip(gp, x, y):
    plt.annotate(name, xy=(xpt,ypt), xytext=(5,5), textcoords='offset points', fontsize = 8)

# Add a title and show the map
plt.title('Map of Cities')
plt.show()
