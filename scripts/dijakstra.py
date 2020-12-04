import matplotlib.pyplot as plt 
import numpy as np 
import math
import random
import time

obst_prob = 0.60


class Node():
    def __init__(self, x, y, isObstacle):
        self.x = x
        self.y = y
        self.parent = None
        self.distance = np.Inf 
        self.isObstacle = isObstacle

node_list = []
goal = Node(17, 23, False)


def make_nodes(i, j):
    for i in range(0, i+1):
        for j in range(0, j+1):
            if random.random() > obst_prob:
                isObst = True
            else :
                isObst = False
            node = Node(i, j, isObst)
            node_list.append(node)
    node_list.pop(0)
def _start_dijakstra(node_list, path):
    time1 = time.time()
    node_list = [node for node in node_list if node.isObstacle == False]
    while len(node_list) != 0:
        node_list = sorted(node_list, key=lambda x: x.distance)
        current = node_list[0]
        adjacent_nodes = [node for node in node_list if int(np.sqrt((node.x - current.x)**2 + (node.y - current.y)**2)) == 1]
        for adjacent_node in adjacent_nodes:
            if adjacent_node.isObstacle == True:
                adjacent_nodes.remove(adjacent_node)
        node_list.pop(0)
        for node in adjacent_nodes:
            if node.distance > current.distance + np.sqrt((current.x-node.x)**2 + (current.y - node.y)**2):
                node.distance = current.distance + np.sqrt((current.x-node.x)**2 + (current.y - node.y)**2)
                node.parent = current
                if node not in path:
                    path.append(node)
    time2 = time.time()
    print(time2 - time1)
    print('Done')

def get_path(path, goal):
    goal = [node for node in path if node.x == goal.x and node.y == goal.y]
    goal = goal[0]
    print(goal)
    #go back from goal
    path_planned = []
    path_planned.append((goal.x, goal.y))
    current = goal
    while current.parent != None:
        path_planned.append((current.parent.x, current.parent.y))
        current = current.parent
    return path_planned
        


make_nodes(25, 25)
x = [n.x for n in node_list]
y = [n.y for n in node_list]
x_obst = [n.x for n in node_list if n.isObstacle == True]
y_obst = [n.y for n in node_list if n.isObstacle == True]
plt.scatter(x, y)
plt.scatter(x_obst, y_obst, color='black')
plt.show()
start = Node(0, 0, isObstacle = False)
start.distance = 0
node_list.insert(0, start)
path = []
#start dijakstras
path.append(start)
_start_dijakstra(node_list, path)
path = path[1:]
path_planned = get_path(path, goal)
'''for node in path:
    print("Node.x, Node.y",(node.x, node.y))
    print("Node.distance", node.distance)
    print("Node.parent.coord", (node.parent.x, node.parent.y))
    print("----------")'''
x = [n.x for n in node_list]
y = [n.y for n in node_list]
x_obst = [n.x for n in node_list if n.isObstacle == True]
y_obst = [n.y for n in node_list if n.isObstacle == True]
x_path = [n[0] for n in path_planned]
y_path = [n[1] for n in path_planned]
plt.scatter(x, y)
plt.plot(x_path, y_path, color='red')
plt.scatter(x_obst, y_obst, color='black')
plt.scatter(goal.x, goal.y, color = 'green')
plt.show()




