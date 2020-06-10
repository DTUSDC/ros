# DTUSDC ROS NAVIGATION
Welcome to DTUSDC's Navigation 


This document will give you a brief description about the navigation capabilities of our Bot

The main algorithm we are using in SLAM-GMAPPING for simultaneous localisation and mapping 
Move-Base node is the main compoment of ROSNavigation stack 
Local,Global Costmap and Move Base are configured with the parameters

## Navigation is done with help of ROS Navigation Stack

### Folder Structure

* **launch**
   *This folder contains all our launch files from launching gmapping and move base node*
* **param**
   *This folder contains the YAML files for configuring our navigation stack*
  

## Running Navigation
**Load up Rviz/Gazebo:**

The following command will load the simulation along with the robot mesh:
```bash
roslaunch simulation simulation.launch
```
**Launch the navstack**
```bash
roslaunch navigation navigation.launch
```
## Giving the Goal

In Rviz click the `2d nav Goal` to give bot a new location
