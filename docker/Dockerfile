# syntax=docker/dockerfile:1

# ROS distribution to use
ARG ROS_DISTRO=humble

FROM osrf/ros:${ROS_DISTRO}-desktop-full AS base
ENV ROS_DISTRO=${ROS_DISTRO}
SHELL ["/bin/bash", "-c"]

# Install basic packages and the Qt XCB runtime dependency used by RQT
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxcb-cursor0 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install ros dependencies
RUN apt-get install -y ros-lyrical-tf-transformations 

# Install ds-crazyflies
WORKDIR /ds
COPY --chown=devuser ./setup.sh /ds/ds-crazyflies/setup.sh
COPY --chown=devuser ./repos /ds/ds-crazyflies/repos
COPY --chown=devuser ./src /ds/ds-crazyflies/src

WORKDIR /ds/ds-crazyflies
RUN ./setup.sh simulation
RUN source /opt/ros/${ROS_DISTRO}/setup.bash &&\
    colcon build

  
RUN echo "source /opt/ros/lyrical/setup.bash" >> ~/.bashrc \
    && echo "source /ds/ds-crazyflies/install/setup.bash" >> ~/.bashrc
