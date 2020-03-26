import numpy as np 
from sklearn.neighbors import KDTree
import random
import matplotlib.pyplot as plt 

point = [6.54345, 7.65456]
n = 25
point_list = [[random.random()*n, random.random()*n] for i in range(n)]
X = np.array(point_list )
tree = KDTree(X,leaf_size=4)
dist, ind = tree.query(np.array([point]), k=6)
x_list = [point_list[i][0] for i in range(len(X))]
y_list = [point_list[i][1] for i in range(len(X))]
nearest_neighbors = [X[i] for i in ind][0]
x_nn = [nearest_neighbors[i][0] for i in range(len(nearest_neighbors))]
y_nn = [nearest_neighbors[i][1] for i in range(len(nearest_neighbors))]
plt.scatter(point[0], point[1], color='green')
plt.scatter(x_list, y_list, color='black')
plt.scatter(x_nn, y_nn, color='red')
plt.show()

