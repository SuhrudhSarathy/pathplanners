import random
import matplotlib.pyplot as plt 
from shapely.geometry import LineString, Polygon, Point
import numpy as np 
from sklearn.neighbors import KDTree

def get_n_neighbors(node_list, n, point):
    X = [[p.x, p.y] for p in node_list]
    X = np.array(X)
    tree = KDTree(X, leaf_size=2)
    ind, dist = tree.query(np.array([[point.x, point.y]]), k=n)
    print(ind)
    n_neighbors = [node_list[i] for i in ind]
    return n_neighbors

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

def plot_obstacle(obstacle):
    point_list = obstacle.exterior.coords
    x_list = [p[0] for p in point_list]
    y_list = [p[1] for p in point_list]
    plt.fill(x_list, y_list, color='black')
    

class Node():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.connections = []
        self.distance = np.Inf
        self.hueristic = np.Inf
        self.parent = None


def generate_nodes(nodes): 
    while nodes > 0 :
        x = random.random() * 10
        y = random.random() * 10
        point = Point(x, y)
        for obstacle in obstacles():
            if obstacle.contains(point):
                collision = True
                break
            else:
                collision = False
        if collision == True:
            continue
        else:
            node_list.append(Node(x, y))
            nodes -= 1

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

def make_roadmap(node_list, obstacle_list):
    for node in node_list:
        node_list2 = [node2 for node2 in node_list if node2 != node]        
        for node2 in node_list2:
           if collisionCheck(node, node2, obstacle_list) == False:
               node.connections.append(node2)
               
def plot_roadmaps(node_list, obstacle_list):
    for node in node_list:
        for node2 in node.connections:
            plt.plot([node.x, node2.x], [node.y, node2.y], color = 'red')   


    
def connect_node(node_list, node, obstacle_list):
    for node2 in node_list:
        if collisionCheck(node, node2, obstacle_list) == False:
            node2.connections.append(node)
            node.connections.append(node2)
    node_list.append(node)
        
def astar(node_list, start, goal):
    while len(node_list) != 0:
        node_list = sorted(node_list, key=lambda node: node.hueristic)
        current = node_list[0]
        node_list.remove(current)
        adjacent_nodes = current.connections
        for node in adjacent_nodes:
            if current.x == goal.x and current.y == goal.y:
                #print(current.x, current.y ,current.parent)
                print("Reached Goal")
                break
            else:
                if node.distance > current.distance + np.sqrt((node.x - current.x)**2 + (node.y - current.y)**2):
                    node.distance = current.distance + np.sqrt((node.x - current.x)**2 + (node.y - current.y)**2)
                    node.hueristic = node.distance + np.sqrt((node.x - goal.x)**2 + (node.y - goal.y)**2)
                    node.parent = current
                    #print((current.x, current.y), (goal.x, goal.y))
                    if node not in path:
                        path.append(node)
def get_path(path, goal):
    goal = [node for node in path if node.x == goal.x and node.y == goal.y]
    goal = goal[0]
    #go back from goal
    path_planned = []
    path_planned.append((goal.x, goal.y))
    current = goal
    while current.parent != None:
        path_planned.append((current.parent.x, current.parent.y))
        current = current.parent
    return path_planned

if __name__ == '__main__':
    start = Node(0, 0)
    goal = Node(10, 10)
    start.distance = 0
    start.hueristic = start.distance + np.sqrt((start.x - goal.x)**2 + (start.y - goal.y)**2)    
    path = []
    obstacle_list = obstacles()
    for obstacle in obstacle_list:
        plot_obstacle(obstacle)
    nodes = 60
    node_list = []
    generate_nodes(nodes)
    make_roadmap(node_list, obstacle_list)
    connect_node(node_list, start, obstacle_list)
    #print([(p.x, p.y, p.distance, p.hueristic, p.connections) for p in node_list if (p.x == start.x ) and (p.y == start.y)])
    connect_node(node_list, goal, obstacle_list)
    astar(node_list, start, goal)
    path_planned = get_path(path, goal)
    #print([((p.x , p.y), (p.parent.x, p.parent.y)) for p in path])
    #print(path_planned)
    plt.scatter([p.x for p in node_list], [p.y for p in node_list])
    plt.scatter([start.x, goal.x], [start.y, goal.y], color='green')
    plot_roadmaps(node_list, obstacle_list)    
    plt.plot([p[0] for p in path_planned], [p[1] for p in path_planned], color = 'yellow')
    plt.show()


    





    
        
