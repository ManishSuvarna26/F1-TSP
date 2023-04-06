import re
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import random
from math import sqrt
from math import factorial
import numpy as np
from aco import AntColony

with open('Cities.txt', 'r') as f:
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

latitudes = np.array([float(re.findall(r'-?\d+\.\d+', lat)[0]) * (-1 if re.findall(r'[A-Za-z]+', lat)[0] == 'S' else 1) for lat in latitudes])
longitudes = np.array([float(re.findall(r'-?\d+\.\d+', long)[0]) * (-1 if re.findall(r'[A-Za-z]+', long)[0] == 'W' else 1) for long in longitudes])

print(latitudes)
print(longitudes)
print(gp)

xy = 2

n_gp = len(gp)

print(n_gp)

latitudes_rs = latitudes.reshape(n_gp,1)
longitudes_rs = longitudes.reshape(n_gp,1)
xy_coords = np.zeros((n_gp,2))

for i in range(n_gp):
    xy_coords[i, 0] = latitudes_rs[i]
    xy_coords[i, 1] = longitudes_rs[i]

print(xy_coords)

def distance_matrix(coords):
    num_cities = len(coords)
    dist_mat = np.array([[0.0] * num_cities for i in range(num_cities)])
    for i in range(num_cities):
        for j in range(i+1, num_cities):
            x1, y1 = coords[i]
            x2, y2 = coords[j]
            dist = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            dist_mat[i][j] = dist
            dist_mat[j][i] = dist
    return dist_mat

def draw_best_path(path, latitudes, longitudes):

    fig = plt.figure(figsize=(10,8))
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
    m.plot(x, y, 'ro', markersize=5)

    for name, xpt, ypt in zip(gp, x, y):
        plt.annotate(name, xy=(xpt,ypt), xytext=(5,5), textcoords='offset points', fontsize = 8)

    n_loc = len(path)
    for i in range(n_loc-2):
        init_loc = path[i]
        end_loc = path[i+1]
        m.drawgreatcircle(longitudes[init_loc], latitudes[init_loc], longitudes[end_loc], latitudes[end_loc], linewidth=2, color='b')



    plt.title('Ants have spoken! This is the best way to tour an F1 GP!')
    plt.pause(100)

dist_mat = distance_matrix(xy_coords)
np.fill_diagonal(dist_mat, np.inf)

print(dist_mat)


ant_colony = AntColony(dist_mat, gp, xy_coords, latitudes, longitudes, 1, 1, 100, 0.95, alpha=1, beta=1)
shortest_path = ant_colony.run()
print ("shorted_path: {}".format(shortest_path))
shortest_node_list = ant_colony.extract_nodes(shortest_path)
draw_best_path(shortest_node_list, latitudes, longitudes)
print("Done!")
