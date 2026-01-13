FROM osrf/ros:jazzy-desktop-full

RUN apt-get update && apt-get install -y \
    python3-pip \
    nano \
    ros-jazzy-rosbridge-suite \
    ros-jazzy-turtlebot3* \
    && rm -rf /var/lib/apt/lists/*

ENV TURTLEBOT3_MODEL=burger
WORKDIR /home/ubuntu/agv_project

CMD ["/bin/bash"]
