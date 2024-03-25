cmake_minimum_required(VERSION 3.0.2)
project(carla_player_publisher)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  rospy
  carla_player_publisher_msg
)

catkin_package(
  # INCLUDE_DIRS 
  # LIBRARIES carla_player_publisher
  CATKIN_DEPENDS geometry_msgs rospy carla_player_publisher_msg
)

include_directories(
  include
   ${catkin_INCLUDE_DIRS}
)


catkin_install_python(PROGRAMS
  src/carla_player_publisher.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
