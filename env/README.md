# Environments 
An implementation of environments for simulating the action of path planning algorithms in 2-D
Presently consists of a world with fixed grids, which can be used for grid-based path planning algorithms like A-star and Dijkstra's etc.

## GridWorld
Basic implementation of a grid based world. Use `GridWorld.py` for python implementation and use `GridWorld.hpp` as a header only alternative with the same API.
### Features
1. Uses Shapely for collision checking.
2. Stores the nodes in a KDTree data structure for faster and efficient search.
3. Contains functions for plotting the world.

### API
The methods of the GridWorld class can be broadly divided into four categories.
#### 1. Making the Environment
- `make_obstacles`  :   Makes the obstacles based on parameter `obstacle_level`. Supports `Box` type and `Circle` type obstacles.
- `make_nodes`  :   Makes the nodes for the given map size and stores them in a KDTree.

#### 2. Collision Checking
- `check_collision_of_point`    :   Checks if the given point is within any obstacle.
- `check_collision_of_path` :   Checks if the given path is in collision with the obstacles in the world.

#### 3. Nearest Neighbour Queries
- `obtain_nearest_n`    :   Obtains the `n` nearest neighbours using the KDTree DataStructure.
- `obtain_nearest_in_r` :   Obtains the nearest neighbours within the given radius `r`.

#### 4. Plotting Functions
- `plot_obstacles`  :   Plots obstacles in the world.
- `plot_points`     :   Plots points(nodes).
- `plot_start_and_goal` :   Plots the start and goal of the world.
- `plot_path`       :   Plots a given path.
- `plot_world`      : Plots the whole world. Also plots the path if given.

### Requirements
#### 1. Python
The python version requires the follwing modules
1. Numpy
2. MatPlotlib
3. Descartes
4. Scikit Learn
5. Shapely

#### 2. C++
The C++ version(as of now, is limited, without any visualisation and nearest neigbour search) uses Boost Geometry for all the geometry related applications.

## Continous World
Basic implementation of a world without grids.
### Features
1. Uses Shapely for collision checking.
2. Contains functions for plotting the world.

### API
The methods of the ContinousWorld class can be broadly divided into three categories.
#### 1. Making the Environment
- `make_obstacles`  :   Makes the obstacles based on parameter `obstacle_level`. Supports `Box` type and `Circle` type obstacles.

#### 2. Collision Checking
- `check_collision_of_point`    :   Checks if the given point is within any obstacle.
- `check_collision_of_path` :   Checks if the given path is in collision with the obstacles in the world.

#### 3. Plotting Functions
- `plot_obstacles`  :   Plots obstacles in the world.
- `plot_start_and_goal` :   Plots the start and goal of the world
- `plot_path`       :   Plots a given path
- `plot_world`      : Plots the whole world. Also plots the path if given.