cmake_minimum_required(VERSION 2.8.3)
project(quad_sim)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  geometry_msgs
  visualization_msgs
  nav_msgs
  tf2_ros
  topic_tools
)

catkin_package(
  INCLUDE_DIRS
  LIBRARIES
  CATKIN_DEPENDS roscpp geometry_msgs visualization_msgs nav_msgs tf2_ros topic_tools
  DEPENDS
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

