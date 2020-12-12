import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString, Polygon
from sklearn.neighbors import KDTree
from descartes import PolygonPatch

PLOT_POINTS = False

class Node:
    def __init__(self, x, y):
        self.x, self.y = x, y
class Obstacle:
    def __init__(self, obj, type_):
        self.obj = obj
        self.patch = PolygonPatch(obj, fc="b",alpha=0.75)
        self.type = type_

    def plot_obstacle(self, ax):
        ax.add_patch(self.patch)

    def check_collision(self, point):
        if point.within(self.obj):
            return True
        else: 
            return False
    
    def __str__(self):
        print(f"Box at : {self.obj.exterior.coords.xy}") if self.type == "box" else print(f"Circle at : {self.obj.centroid.x}, {self.obj.centroid.y}")
    def __repr__(self):
        return "Box : {}\n".format(self.obj.exterior.coords.xy) if self.type=="box" else "Circle : {:1f}, {:1f}\n".format(self.obj.centroid.x, self.obj.centroid.y)

class GridWorld:
    """Basic World that consisits of Grid
    Args:
        X : Maximum Width of the World
        Y : Maximum length of the World
        obstacle_level (0 to 1) : level of obstacles
        obst_type : list of strings. Supported "circles" and "boxes"
    """
    def __init__(self, X=10, Y=10, obstacle_level=0.9, obst_type=["circles", "boxes"], start = [0, 0], goal = [10, 10]):
        self.X = X
        self.Y = Y
        self.obstacle_level = obstacle_level
        self.obst_type = obst_type
        self.start = start
        self.goal = goal
        # List of all the nodes and obstacles
        self.nodes = []
        self.obstacles = []
        # Make the obstacles
        self.make_obstacles()
        # Method to make the nodes
        #self.make_nodes()

        # Plotting information
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_xlim([-2.5, int(self.X) + 2.5])
        self.ax.set_ylim([-2.5, int(self.Y) + 2.5])

    def __len__(self):
        return len(self.nodes)

    def __str__(self):
        return f"``Grid World``\nDimensions : {self.X}, {self.Y}\nObstacle level : {self.obstacle_level}\nObstacle Types : {self.obst_type}"

    def make_obstacles(self):
        X = [i for i in range(0, self.X - 1) if i not in [self.start[0], self.goal[0]]]
        Y = [i for i in range(0, self.Y - 1) if i not in [self.start[1], self.goal[1]]]
        
        for i in range(0, int(self.obstacle_level * self.X * self.Y)):
            #randomly select a corner in X, Y
            x, y = np.random.choice(X), np.random.choice(Y)

            # choose between a square and a rectangle
            obst_type = np.random.choice(self.obst_type)

            if obst_type == "boxes":
                height, width = np.random.uniform(1, 3), np.random.uniform(1, 3)
                self.obstacles.append(Obstacle(Polygon([(x, y), (x, y+height), (x+width, y+height), (x+width, y)]), "box"))
            else:
                self.obstacles.append(Obstacle(Point(x, y).buffer(np.random.uniform(0.5, 1.5)), "circle"))

    def plot_obstacles(self):
        for obst in self.obstacles:
            obst.plot_obstacle(self.ax)
        if PLOT_POINTS:
            self.plot_points()
        plt.show()
    
    def plot_points(self):
        for x in range(-2, self.X + 2):
            for y in range(-2, self.Y + 2):
                plt.scatter(x, y, color='red', alpha=0.5)
    
    # Functions for checking collisions
    def check_collision_of_point(self, point):
        for obst in self.obstacles:
            if obst.check_collision(point) == True:
                return True
        # else:
        return False

    def check_collision_of_path(self, path):
        for obst in self.obstacles:
            if LineString(path).intersects(obst):
                return True
        # else
        return False

    def obtain_nearest_n(self, point, n):
        # use KDTree to store all the nodes
        # and query the nearest n neighbours
        pass
    def obtain_nearest_in_r(self, point, r):
        # use KDTree to store all the nodes
        # and query the nearest neighbours in r radius
        pass
    
    def make_nodes(self):
        # make all the nodes and store them in a KDTree

if __name__ == "__main__":
    world = GridWorld(obstacle_level=0.1)
    world.plot_obstacles()