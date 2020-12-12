# Environments 
An implementation of environments for simulating the action of path planning algorithms in 2-D
Presently consists of a world with fixed grids, which can be used for grid-based path planning algorithms like A-star and Dijkstra's etc.

## GridWorld
Basic implementation of a grid based world.
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
- `plot_start_and_goal` :   Plots the start and goal of the world
- `plot_path`       :   Plots a given path