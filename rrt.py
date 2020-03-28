import matplotlib.pyplot as plt 
import numpy as np 
from shapely.geometry import Point, LineString, Polygon
import random
from sklearn.neighbors import KDTree

## make a KD Tree to store path



def plot_obstacle(obstacle):
    point_list = obstacle.exterior.coords
    x_list = [p[0] for p in point_list]
    y_list = [p[1] for p in point_list]
    plt.fill(x_list, y_list, color='black')

class Rectangle():
    def __init__(self, center):
        self.x, self.y = center[0], center[1]
        self.polygon = Polygon([(self.x + 0.25, self.y + 0.25), (self.x - 0.25, self.y + 0.25), (self.x - 0.25, self.y - 0.25), (self.x + 0.25, self.y - 0.25)])

def generate_random_map(number):
    obstacle_list = []
    for i in range(number):
        rectangle = Rectangle((random.random()*10, random.random()*10))
        obstacle_list.append(rectangle.polygon)
    for obstacle in obstacle_list:
        plot_obstacle(obstacle)
    return obstacle_list

def obstacles():
    poly1 = Polygon([(2, 10), (7, 10), (7, 1), (6, 1), (6, 6), (4, 6), (4, 9), (2, 9)])
    poly2 = Polygon([(4, 0), (4, 5), (5, 5), (5, 0)])
    poly3 = Polygon([(8, 2), (8, 7), (10, 7), (10, 2)])
    '''cirlce1 = Point(8, 3).buffer(1)
    circle2 = Point(2, 7).buffer(1.5)
    poly4 = Polygon([(11, 10), (11, 13), (12, 13.75), (13, 12)])
    circle3 = Point(10, 1).buffer(0.75)
    circle4 = Point(11, 1.2).buffer(0.86)
    circle5 = Point(5, 15).buffer(1)
    circle6 = Point(4, 10).buffer(1)
    circle7 = Point(5, 10.7).buffer(1)'''
    obstacle_list = [poly1, poly2, poly3]
    return obstacle_list



def collisionCheck(point1, point2, obstacle_list):
    line = LineString([(point1.x, point1.y), (point2.x, point2.y)])
    intersection = 0
    for obstacle in obstacle_list:
        if line.intersects(obstacle):
            intersection += 1
        else:
            pass
    if intersection == 0:
        collision = False
    else:
        collision = True
    return collision

def distance(point1, point2):
    distance = np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    return distance

def new_vector(point1, point2, threshold):
    vector = Node((point2.x - point1.x), (point2.y - point1.x))
    vector.x, vector.y = vector.x/np.sqrt((vector.x**2 + vector.y**2)), vector.y/np.sqrt((vector.x**2 + vector.y**2))
    vector.x, vector.y = point1.x + vector.x * threshold, point1.y + vector.y * threshold
    return vector
class Node():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.distance = 0
class RRT():
    def __init__(self, start, goal, threshold, obstacle_list, max_iter):
        self.start = start
        self.goal = goal
        self.threshold = threshold
        self.nodes = []
        self.is_reached = False
        self.max_iter = max_iter
        self.goal_sample_rate = 0.1

    def _start_tree(self):
        self.nodes.append(self.start)
        while self.max_iter > 0:
            new_node = self.generate_random_node()
            #print((new_node.x, new_node.y))
            for node in self.nodes:
                node.distance = distance(node, new_node)
            self.nodes = sorted(self.nodes, key=lambda node: node.distance)
            nearby_node = self.nodes[0]
            for node in self.nodes:
                node.distance = 0 
            if distance(nearby_node, new_node) <= self.threshold:
                if collisionCheck(nearby_node, new_node, obstacle_list) == False:
                    new_node.parent = nearby_node
                    self.nodes.append(new_node)
                else : 
                    pass
            else:
                new_node = new_vector(nearby_node, new_node, self.threshold)
                if collisionCheck(new_node, nearby_node, obstacle_list) == False:
                    new_node.parent = nearby_node
                    self.nodes.append(new_node)
                else :
                    pass
            if new_node.x == self.goal.x and new_node.y == self.goal.y:
                self.is_reached == True
                print(self.max_iter)
                print('Reached')
                break
            self.max_iter -= 1
            #print((new_node.x, new_node.y))
    def plot_points(self):
        plt.scatter([p.x for p in self.nodes], [p.y for p in self.nodes], color='red')
        for node in self.nodes :
            plt.plot([node.x, node.parent.x], [node.y, node.parent.y], color = 'green')
        plt.scatter([self.start.x, self.goal.x], [self.start.y, self.goal.y], color='yellow')

    def generate_random_node(self):
        if np.random.random_sample() > self.goal_sample_rate:
            new_node = Node(random.random() * 10, random.random()*10)
        else:
            new_node = self.goal
        return new_node
if __name__ == '__main__': 
    obstacle_list = generate_random_map(100)
    '''obstacle_list = obstacles()
    for obstacle in obstacle_list:
        plot_obstacle(obstacle)'''
    start = Node(0, 0)
    start.parent = start
    rrt = RRT(start, Node(10,10), 0.9, obstacle_list, 1000)
    rrt._start_tree()
    rrt.plot_points()
    plt.show()
    

