# CORE_SPARTON
Package implementing support for Sparton IMU(SPARTON AHRS 8-P).

#### Currently supported devices/interfaces
* AHRS8 over NMEA

#### Usage
1. Drop into a catkin source folder (such as ~/catkin-ws/src/)
2. Run catkin_make inside the folder above the catkin source folder (~/catkin-ws)
3. Source the setup.bash in the devel folder (source ~/catkin-ws/devel/setup.bash)
4. Run the launch file with roslaunch (roslaunch core_sparton AHRS-8.launch)

The launch file is located in the core_sparton/launch folder and shows how to launch the node with roslaunch. It also shows where to set the serial port and baud rate. The core_sparton/udev folder contains a file with a udev rule that ensures AHRS-8 devices will always appear at /dev/sparton/ahrs8, useful for systems with lots of other USB serial ports.

The node publishes a sensor_msgs/Imu message to the "imu/data" topic.
