import numpy as np 
import matplotlib.pyplot as plt
import math 
import random
import time

obst_prob = 0.6
node_list = []
path = []

class Node():
    def __init__(self, x, y,isObst):
        self.x = x
        self.y = y
        self.isObst = isObst
        self.distance = np.Inf
        self.hueristic = np.Inf
        self.parent = None


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

def plot_state(point_list, color_int='blue'):
    x_list = [p.x for p in point_list]
    y_list = [p.y for p in point_list]
    plt.scatter(x_list, y_list, color=color_int)


def _startA_star(node_list, path, goal):
    time1 = time.time()
    node_list = [node for node in node_list if node.isObst == False]
    while len(node_list) != 0:
        node_list = sorted(node_list, key=lambda node: node.hueristic)
        current = node_list[0]
        #print(current.x,current.y)
        adjacent_nodes = [node for node in node_list if int(np.sqrt((node.x - current.x)**2 + (node.y - current.y)**2)) == 1]
        for adjacent_node in adjacent_nodes:
            if adjacent_node.isObst == True:
                adjacent_nodes.remove(adjacent_node)
        node_list.remove(current)
        #print(adjacent_nodes)
        #print('1')
        if current.x == goal.x and current.y == goal.y:
            print("Reached Goal")
            break
        else:
            for node in adjacent_nodes:
                #print('inside for loop')
                if node.distance > current.distance + np.sqrt((current.x - node.x)**2 + (current.y - node.y)**2):
                    node.distance = current.distance + np.sqrt((current.x - node.x)**2 + (current.y - node.y)**2)
                    node.hueristic = node.distance + np.sqrt((goal.x - node.x)**2 + (goal.y - node.y)**2)
                    node.parent = current
                    #print('inside first if')
                    if node not in path:
                        path.append(node)
                        #print('node appended')
            #print('end of for loop')
    time2 = time.time()
    print(time2 - time1)

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
                    

goal = Node(47, 23, False)
make_nodes(50, 50)
start = Node(0, 0, False)
start.distance = 0
start.hueristic = start.distance + np.sqrt((start.x - goal.x)**2 + (start.y - goal.y)**2)
node_list.insert(0, start)
plot_state(node_list)
plot_state([node for node in node_list if node.isObst == True], color_int='black')
path.append(start)
_startA_star(node_list, path, goal)
path_planned = get_path(path, goal)
plt.plot([p[0] for p in path_planned], [p[1] for p in path_planned], color = 'red')
plt.show()





    