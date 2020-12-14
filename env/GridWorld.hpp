#ifndef GRIDWORLD_H
#define GRIDWORLD_H


#include <iostream>
#include <boost/geometry.hpp>
#include <boost/geometry/geometries/point_xy.hpp>
#include <boost/geometry/geometries/polygon.hpp>
#include <boost/geometry/geometries/linestring.hpp>
#include <boost/geometry/geometries/adapted/boost_tuple.hpp>
#include <boost/geometry/geometries/adapted/c_array.hpp>
#include <vector>
#include <random>
#include "../utils/combinedplotting.hpp"

#define BOX 1
#define CIRCLE 2
#define PLOT_POINTS 1
#define PLOT_START_AND_GOAL 0
#define PLOT_OBSTACLES 1

BOOST_GEOMETRY_REGISTER_C_ARRAY_CS(cs::cartesian)
BOOST_GEOMETRY_REGISTER_BOOST_TUPLE_CS(cs::cartesian)

using namespace boost::geometry;
typedef model::polygon<model::d2::point_xy<float>> Polygon;
typedef model::d2::point_xy<float> Point;
typedef model::linestring<Point> LineString;

std::random_device rnd;
std::mt19937 gen(rnd());
std::uniform_real_distribution<float> dis(1.0, 2.5);

namespace gridworld{

class BoxObstacle{
    private:
        Polygon obj;
        float x = 0;
        float y = 0;
        float width = 1;
        float height = 1;
        int type = BOX;
    public:
        BoxObstacle(float x_end, float y_end, float width_, float height_, int type_) : x(x_end), y(y_end), width(width_), height(height_), type(type_)
        {
            construct_polygon();
        }
        void construct_polygon(){
            // make the actual polygon
            float points[][2] = {{x, y}, {x, y+height}, {x+width, y+height}, {x+width, y}};
            append(obj, points);
        }
        void get_params_of_polygon(float &x, float &y, float &width, float &height){
            // return the coordinates of the polygon
            x = this->x;
            y = this->y;
            width = this->width;
            height = this->height;
        }
        // void plot polygon
        bool check_point_within_polygon(Point& point){
            boost::tuple<float, float> p = boost::make_tuple(point.x(), point.y());
            return within(p, obj);
        }
        bool check_line_intersects_polygon(LineString& line){
            return intersects(line, obj);
        }
        bool check_line_touches_polygon(LineString& line){
            return touches(line, obj);
        }
};

class GridWorld{
    public:
        GridWorld(float X_ = 10, float Y_ = 10, float obstacle_level_ = 0.1, float start_x = 0, float start_y = 0, float goal_x = 10, float goal_y = 10){

            // set the constants
            X = X_;
            Y = Y_;
            obstacle_level = obstacle_level;

            // set the start and goal coordinates
            start.x(start_x);
            start.y(start_y);
            goal.x(goal_x);
            goal.y(goal_y);

            make_obstacles();
            make_nodes();
        }

        // Making Functions
        void make_obstacles(){
            std::vector<float> x_s, y_s;

            // make a list of X and Y that doesnot include start_x and start_y
            for(int i = 0; i < X - 1; i++){
                if(i != get<0>(start) && i != get<0>(goal)){
                    x_s.push_back(i);
                }
            }
            for(int i = 0; i < Y-1; i++){
                if(i !=get<1>(start) && i!=get<1>(goal)){
                    y_s.push_back(i);
                }
            }

            // Randomly select the base coordinates from the above nodes
            for(int i = 0; i < int(obstacle_level * X * Y); i++){
                // randomly select a number to access the element in the array
                int x_index = rand() % x_s.size();
                int y_index = rand() % y_s.size();

                obstacles.push_back(BoxObstacle(x_s[x_index], y_s[y_index], dis(gen), dis(gen), BOX));
            }
        }

        void make_nodes(){
            // Due to a lack of better option the nodes are stored in a vector
            for(int i = -2; i < X + 2; i++){
                for(int j = -2; j < Y + 2; j++){
                    nodes.push_back(Point(i, j));
                }
            }
        }

        // Functions for checking collisions
        bool check_collision_of_point(Point& point){
            for(auto obst: obstacles){
                if(obst.check_point_within_polygon(point)){
                    return true;
                }
            }
            // else
            return false;
        }

        bool check_collision_of_path(LineString& path){
            for(auto obst: obstacles){
                if(obst.check_line_intersects_polygon(path) || obst.check_line_touches_polygon(path)){
                    return true;
                }
            }
            //else
            return false;
        }
        void get_status(){
            std::cout << "```GridWorld```" << std::endl;
            std::cout << "X: " << X << "Y: " << Y << std::endl;
            std::cout << "No. of Nodes: " << nodes.size() << std::endl;
            std::cout << "No. of Obstacles: " << obstacles.size() << std::endl;
        }

        // Plotting functions
        void plot_obstacles(){
            for(auto obst: obstacles){
                float x, y, width, height;
                obst.get_params_of_polygon(x, y, width, height);
                plot_box_obstacle(x, y, width, height);
            }
        }

        void plot_points(){
            for(auto node: nodes){
                plot_point(node, "red");
            }
        }

        void plot_start_and_goal(){
            plot_point(start, "green");
            plot_point(goal, "green");
        }

        void plot_path(LineString* path){
            plot_linestring(path);
        }

        void plot_world(LineString* path = NULL){
            // if path is not a null pointer
            if(path){
                plot_path(path);
            }
            if(PLOT_POINTS){
                plot_points();
            }
            if(PLOT_START_AND_GOAL){
                plot_start_and_goal();
            }
            if(PLOT_OBSTACLES){
                plot_obstacles();
            }
        }
        
    private:
        float X = 10;
        float Y = 10;
        float obstacle_level = 0.1;
        // int obst_type {not yet implemented}
        std::vector<Point> nodes;
        std::vector<BoxObstacle> obstacles;
        Point start, goal;
};
} // namespace gridworld
#endif