import random as rn
import numpy as np
from numpy.random import choice as np_choice
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

class AntColony(object):

    def __init__(self, dist_mat, gp, xy_coords, latitudes, longitudes, n_ants, n_best, n_iterations, rho, alpha=1, beta=1):

        self.dist_mat  = dist_mat
        self.pheromone = np.ones(self.dist_mat.shape) / len(dist_mat)
        self.all_inds = range(len(dist_mat))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.rho = rho
        self.alpha = alpha
        self.beta = beta
        self.xy_coords = xy_coords
        self.latitudes = latitudes
        self.longitudes = longitudes
        self.gp = gp

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):

            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])




            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            self.pheromone = self.pheromone * self.rho
            node_list = self.extract_nodes(all_time_shortest_path)
            print("iteration: {}".format(i))
            print (node_list)
            self.draw_path(node_list, self.latitudes, self.longitudes)


        return all_time_shortest_path

    def draw_path(self, path, latitudes, longitudes):

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

        for name, xpt, ypt in zip(self.gp, x, y):
            plt.annotate(name, xy=(xpt,ypt), xytext=(5,5), textcoords='offset points', fontsize = 8)

        n_loc = len(path)
        for i in range(n_loc-2):
            init_loc = path[i]
            end_loc = path[i+1]
            m.drawgreatcircle(longitudes[init_loc], latitudes[init_loc], longitudes[end_loc], latitudes[end_loc], linewidth=2, color='b')


        # Add a title and show the map
        plt.title('Formula 1 GP Tour')
        plt.ion()

        plt.pause(0.015)

        plt.clf()




    def spread_pheronome(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.dist_mat[move]

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.dist_mat[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))

        return all_paths

    def extract_nodes(self, path):
        node_list = [p[0] for p in path[0] ]
        journey = path[0]
        first_tour = journey[0]
        first_city = first_tour[0]
        node_list.append(first_city)
        dist = path[-1]
        node_list.append(dist)

        return node_list


    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.dist_mat) - 1):
            move = self.pick_move(self.pheromone[prev], self.dist_mat[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start)) # going back to where we started
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)

        norm_row = row / row.sum()
        move = np_choice(self.all_inds, 1, p=norm_row)[0]
        return move
