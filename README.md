# DTUSDC's Software Stack
![ROS CI](https://github.com/DTUSDC/ros/workflows/ROS%20CI/badge.svg?branch=master)

Welcome to the DTUSDC IGVC software repo!

This document will give you a brief description of the repo's layout and an overview of the repo.

## Folder Structure

 * **simulation**
    *Package to launch the simulation along with a test maze world and URDF*
 * **navigation**
    *Collection of nodes that form our navigation stack*
 * **encoder**
    *Nodes that form the arduino encoders.*
 * **perception**
    *Nodes and scripts that contain the perception pipeline.*
    
## Prerequisites

1. Download the `ros/navstack` packages

   ```bash
   sudo apt-get ros-melodic-navigation
   ```

2. Download and install `gmapping`:
   ```bash
   sudo apt-get install ros-melodic-slam-gmapping
   ```
   
    
## Building Code
 
1. Clone the repository into the src directory of a catkin workspace:
    ```bash
    git clone https://github.com/dtusdc/ros --recursive
    ```

2. Run `catkin build` in the workspace to build all the packages:
    ```bash
    catkin build
    ```
    

## Running Gazebo

**Load up Rviz/Gazebo:**

The following command will load the simulation along with the robot mesh:
```bash
roslaunch simulation simulation.launch
```

**Load up Navigation:**

The following command will load the navigation stack:
```bash
roslaunch navigation navigation.launch
```


## Maintainers
- Ayaan Zaidi
- Tanmay Jain
- Krushnal Patel
