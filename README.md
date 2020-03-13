# DTUSDC's Software Stack

Welcome to the DTUSDC IGVC software repo!

This document will give you a brief description of the repo's layout and an overview of the repo.

## Folder Structure

 * **description**
    *URDF files for our robot *
 * **gazebo**
    *Package to launch the simulation along with a test maze world*
 * **navigation**
    *Collection of nodes that form our navigation stack*
 * **encoder**
    *Nodes that form the arduino encoders.*
 * **perception_pipeline**
    *Nodes and scripts that contain the perception pipeline.*
 * **cv_camera, usb_cam and vision_opencv**
    *Dependant packages.*
    
## Building Code
 
1. Clone the repository into the src directory of a catkin workspace:
    ```bash
    git clone https://github.com/dtusdc/ros --recursive
    ```

2. Run `catkin_make` in the workspace to build all the packages:
    ```bash
    catkin_make
    ```

## Running Gazebo

**Load up Rviz/Gazebo:**

The following command will load the simulation along with the robot mesh:
```
roslaunch description rviz.launch
```

**Load up Navigation:**

The following command will load the navigation stack:
```
roslaunch navigation navigation.launch
```