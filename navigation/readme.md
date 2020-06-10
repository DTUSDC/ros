# DTUSDC ROS NAVIGATION

Welcome to DTUSDC's Navigation

This document will give you a brief description about the navigation capabilities of our Bot


move_base node is the main compoment of `ros/navstack`

[Navstack RosWiki](http://wiki.ros.org/move_base?distro=noetic)

The main algorithm we are using is `gmapping` for simultaneous localisation and mapping

[Gmapping RosWiki](http://wiki.ros.org/gmapping)

Local,Global Costmap and Move Base are configured with the parameters

[2D Costmap RosWiki](http://wiki.ros.org/costmap_2d?distro=noetic)

Global planner and Local planner are used for pathplanning

[Global Planner RosWiki](http://wiki.ros.org/global_planner?distro=noetic)

[Local Planner RosWiki](http://wiki.ros.org/base_local_planner?distro=noetic)

## Navigation is done with help of ROS Navigation Stack

### Folder Structure

- **launch**
  _This folder contains all our launch files from launching gmapping and move base node_
- **param**
  _This folder contains the YAML files for configuring our navigation stack_

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
