# DTUSDC ROS NAVIGATION
Welcome to DTUSDC's Navigation 


This document will give you a brief description about the navigation capabilities of our Bot



## Navigation is done with help of ROS Navigation Stack

### Folder Structure

* **launch**
   *This folder contains all our launch files from launching gmapping and move base node*
* **param**
   *This folder contains the YAML files for configuring our navigation stack*
  
## Prerequisites
1. Download the NavStack packages
    ```bash
    sudo apt-get ros-melodic-navigation
    ```
    
2. Download the Gmapping package
    ```bash
    sudo apt-get install ros-melodic-slam-gmapping
    ```
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
