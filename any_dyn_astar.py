
import numpy as np 
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString, Polygon
import random as rn 
from functools import cmp_to_key

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
        self.g = np.Infinity
        self.rhs = None
        self.succesors = []
        self.predecessors = []
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


class ADAstar():
    '''
        Implementation of  Anytime Dynamic A-star
    '''
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.epsilon = 2.5
        self.OPEN = []
        self.CLOSED = []
        self.INCONS = []

    def cost(self, state1, state2):
        '''
            Cost function used is Euclidean Distance
        '''
        cost = np.linalg.norm(np.array((state1.x, state1.y)) - np.array((state2.x, state2.y)))
        
        return cost
    
    def g(self, state):
        '''
            g is the cost of the present state to goal state
        '''
        g = self.cost(state, self.goal)

        return g

    def rhs(self, state):
        '''
            One-Step-LookAheadCost
        '''    
        if state.x == self.goal.x and state.y == self.goal.y:
            rhs = 0
        else:
            s_dash = sorted(state.successors, key=lambda successor: self.cost(state, successor) + successor.g)[0]
            rhs = self.cost(state, s_dash) + s_dash.g
        return rhs
    
    def hueristic(self, state1, state2):
        '''
            Use manhattan distance as Hueristic
        '''
        hueristic = abs(state1.x - state2.x) + abs(state1.y - state2.y)

        return hueristic

    def keys(self, s):
        '''
            Returns key(s) function as mentioned in the algorithm
        '''

        if self.g(s) > self.rhs(s):
            keys = [self.rhs(s) + self.epsilon * self.hueristic(self.start, s), self.rhs(s)]
        else:
            keys = [self.g(s) + self.hueristic(self.start, s), self.g(s)]

        return keys

    def compare_keys(self, s1, s2):
        '''
            Comparision function for 
        '''

        if s1.keys[0] < s2.keys[0] or (s1.keys[0] == s2.keys[0] and s1.keys[1] < s2.keys[1]):
            return 1
        elif s1.keys[0] == s2.keys[0] and s1.keys[1] == s2.keys[1]:
            return 0
        else :
            return -1

    def sort_open_based_on_keys(self):

        # change this based on version of python
        # refer to https://stackoverflow.com/questions/5213033/sort-a-list-of-lists-with-a-custom-compare-function/46320068#46320068

        self.OPEN = sorted(self.OPEN, key = cmp_to_key(lambda state1, state2: self.compare_keys(state1, state2)))

    def update_state(self, s):
        s.rhs = self.rhs(s)
        if s in self.OPEN :
            self.OPEN.remove(s)
        if s.g != s.rhs:
            if s not in self.CLOSED:
                s.keys = self.keys(s)
                self.OPEN.append(s)
            else:
                self.INCONS.append(s)

    def cip(self):
        '''
            cip == Compare or Improve Path
        '''
        self.sort_open_based_on_keys()
        while self.compare_keys(self.OPEN[0], self.start) == 1 or self.start.rhs != self.start.g:
            self.sort_open_based_on_keys()
            s = self.OPEN[0]
            self.OPEN.remove(s)
            if s.g > s.rhs:
                s.g = s.rhs
                self.CLOSED.append(s)
                for s_dash in s.predecessors:
                    self.update_state(s_dash)
            else:
                s.g = np.Infinity
                s.predecessors.append(s)
                for s_dash in s.predecessors:
                    self.update_state(s_dash)




if __name__ == '__main__':
    start = Node(0.5, 0.5)
    goal = Node(7.5, 9.5)

    map = Map(start, goal)
    map.init_map()
    map.plot_map()
    plt.show()

        

