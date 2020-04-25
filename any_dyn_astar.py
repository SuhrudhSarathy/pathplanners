
import numpy as np 
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString, Polygon
import random as rn 

# Constants
obst_prob = 0.75

class Node():

    '''
        Each node can be represented using this class

        Args:
            1. x-coordinate of centre of the grid cell
            2. y-coordinate of centre of the grid cell
            3. is_obst (bool) denotes if the node is in an obstacle
                default = False (set True to treat it as an obstacle)

        Assumptions:
            1. Grid size = 1
    ''' 

    def __init__(self, x, y, is_obst = False):
        self.x = x
        self.y = y
        self.is_obst = is_obst
        if self.is_obst == True:
            self.coords = [(self.x + 0.5, self.y + 0.5), (self.x + 0.5, self.y - 0.5), (self.x - 0.5, self.y - 0.5), (self.x - 0.5, self.y + 0.5)]
            self.polygon = Polygon(self.coords)
        
        # Parameters used in ADA-star algorithm
        self.g_value = np.Infinity
        self.rhs_value = None
        self.succesors = []
        self.succesor = None
        self.predecessor = None
        self.keys = []

        
    def _plot_node_(self):
        if self.is_obst == True:
            plt.fill([p[0] for p in self.coords], [p[1] for p in self.coords], color='black', alpha = 0.7)
        else:
            plt.scatter(self.x, self.y, color='red', alpha=0.25, s=5)

class Map():

    '''
        This class contains all the information regarding the environment
        Information stored:
        ``````````````````
            1. Start Position
            2. Goal Position
            3. Nodes
            4. Obstacale Data
            5. Path
    '''
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.nodes = []
        self.obstacles = []
        self.path = []

    def init_map(self):
        X = np.arange(start=0.5, stop = 10.5, step=1)
        Y = np.arange(start=0.5, stop = 10.5, step=1)

        for x in X:
            for y in Y:
                if (x == self.goal.x and y == self.goal.y) or (x == self.goal.x and y == self.goal.y):
                    continue 
                else:
                    prob = rn.random()
                    if prob > obst_prob:
                        self.obstacles.append(Node(x, y, True))
                    else:
                        self.nodes.append(Node(x, y))

    def plot_map(self):
        for node in self.nodes:
            node._plot_node_()
        for obst in self.obstacles:
            obst._plot_node_()
        plt.scatter([self.start.x, self.goal.x], [self.start.y, self.goal.y], color='green')


class Dstar():
    '''
        Implementation of  D star Lite algorithm
    '''
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.OPEN = []
        self.CLOSED = []
        self.INCONS = []

    def cost(self, state1, state2):
        '''
            Cost function used is Euclidean Distance
        '''
        cost = np.linalg.norm(np.array((state1.x, state1.y)) - np.array((state2.x, state2.y)))
        
        return cost
    
    def g_value(self, state):
        '''
            g_value is the cost of the present state to goal state
        '''
        g_value = self.cost(state, self.goal)

        return g_value

    def rhs_value(self, state):
        '''
            One-Step-LookAheadCost
        '''    
        if state.x == self.goal.x and state.y == self.goal.y:
            rhs = 0
        else:
            for successor in state.succesors:
                successor.rhs_value = self.cost(state, successor) + successor.g_value
            state.successors = state.successors.sorted(state.succesors, key=lambda successor: successor.rhs_value)
            rhs = state.succesors.rhs_value
            state.successor = state.succesors[0]
        
        return rhs
    
    def hueristic(self, state):
        '''
            Use manhattan distance as Hueristic
        '''
        hueristic = abs(state.x - self.goal.x) + abs(state.y - self.goal.y)

        return hueristic

    def keys(self, s):
        s.keys = [min(self.g_value(s), self.rhs_value(s)+self.hueristic(s)),
                        min(self.g_value(s), self.rhs_value(s))]



if __name__ == '__main__':
    start = Node(0.5, 0.5)
    goal = Node(7.5, 9.5)

    map = Map(start, goal)
    map.init_map()
    map.plot_map()
    plt.show()

        

