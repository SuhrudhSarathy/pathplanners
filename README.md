# Pathplanners
A general implementation of some path planning algorithms for learning and reference purposes
## Contents
This repository contains environments for simulation, planners and some utility functions and classes.
1. `env`    :   Contains simulations environements
2. `scripts`:   Contains Planners
3. `utils`  :   Contains some Utility functions and files.
## Instructions
### Planners written in Python
Planners can be run using the standard way.
```
python planner.py
```
or
```
python3 planner.py
```
can be used based on Python interpreter.
### Planners written in C++
#### Compiling using GCC
Any planner can be compiled using the GCC compiler. How ever since the `matplotlibcpp.h` file is being used for plotting functionality, additional flags are required.
```
g++ -o planner planner.cpp -std=c++11 -I/usr/include/python2.7 -lpython2.7 
```
Refer to the original Matplotlibcpp [repository](https://github.com/lava/matplotlib-cpp) for debugging purposes.

#### Note:
The `utils` directory contains `matplotlibcpp.h` which is a wrapper over the [MatplotLib](https://matplotlib.org) package. Head over to this [repository](https://github.com/lava/matplotlib-cpp) for full information.
