#ifndef COMBINEDPLOTTING_H
#define COMBINEDPLOTTING_H

#include <iostream>
#include <boost/geometry.hpp>
#include <boost/geometry/geometries/point_xy.hpp>
#include <boost/geometry/geometries/polygon.hpp>
#include <boost/geometry/geometries/linestring.hpp>
#include <boost/geometry/geometries/adapted/boost_tuple.hpp>
#include <boost/geometry/geometries/adapted/c_array.hpp>
#include <vector>

#include "matplotlibcpp.h"

namespace plt = matplotlibcpp;
using namespace boost::geometry;
typedef model::polygon<model::d2::point_xy<float>> Polygon;
typedef model::d2::point_xy<float> Point;
typedef model::linestring<Point> LineString;

std::vector<float> x_array;
std::vector<float> y_array;

/*Function to plot a boost::geometry::model::d2::point_xy*/
void plot_point(Point& point, const std::string& color){
    std::vector<float> x_s;
    std::vector<float> y_s;
    float x = get<0>(point);
    float y = get<1>(point);

    x_s.push_back(x);
    y_s.push_back(y);
    plt::scatter(x_s, y_s, 2.0, {{"c", color}});
}

/*helper function to get points out from the LineString*/
void get_point(Point& point){
    x_array.push_back(get<0>(point));
    y_array.push_back(get<1>(point));
}

/*Function to plot a LineString*/
void plot_linestring(LineString* line){
    // due to lack of a simpler solution, the points are getting stored in a vector everytime this function is called.
    // it is being made sure that, the point_array is clear before taking in the next points
    x_array.clear();
    y_array.clear();
    for_each_point(*line, get_point);
    std::vector<float> x_s;
    std::vector<float> y_S;
    plt::plot(x_array, y_array, {{"color", "green"}});
}

/*Function to plot BoxObstacle*/
void plot_box_obstacle(float x, float y, float width, float height){
    std::vector<float> x_s;
    std::vector<float> y_s;

    x_s = {x, x, x+width, x+width};
    y_s = {y, y+height, y+height, y};

    plt::fill(x_s, y_s, {{"c" , "black"}});
}

#endif