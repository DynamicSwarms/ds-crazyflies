# syntax=docker/dockerfile:1

# ROS distribution to use
ARG ROS_DISTRO=humble

FROM osrf/ros:${ROS_DISTRO}-desktop-full AS base
ENV ROS_DISTRO=${ROS_DISTRO}
SHELL ["/bin/bash", "-c"]

RUN apt-get update || true && \
    apt-get install -y --no-install-recommends ntpdate && \
    ntpdate ntp.ubuntu.com

# Install some basic packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip gdb dos2unix wget

RUN apt install mesa-utils -y 

# Install ros dependencies
RUN apt-get install -y ros-humble-tf-transformations ros-humble-ros2-control
# Install webots
RUN mkdir -p /etc/apt/keyrings
WORKDIR /etc/apt/keyrings
RUN wget -q https://cyberbotics.com/Cyberbotics.asc

RUN echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/Cyberbotics.asc] https://cyberbotics.com/debian binary-amd64/" | sudo tee /etc/apt/sources.list.d/Cyberbotics.list
RUN apt update

RUN apt install webots -y

ENV WEBOTS_HOME=/usr/local/webots

RUN mkdir -p /ds && chmod 777 /ds
RUN useradd -ms /bin/bash devuser && \
    echo "devuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER devuser

RUN git config --global --add safe.directory /ds/ds-crazyflies

# Install ds-crazyflies
WORKDIR /ds
COPY --chown=devuser ./src /ds/ds-crazyflies/src
COPY --chown=devuser build.sh /ds/ds-crazyflies/

WORKDIR /ds/ds-crazyflies
RUN source /opt/ros/${ROS_DISTRO}/setup.bash &&\
    dos2unix build.sh &&\
    bash build.sh

# Install webotsworld
WORKDIR /ds
RUN git clone https://github.com/DynamicSwarms/crazywebotsworld.git
   
  
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc \
    && echo "source /ds/ds-crazyflies/install/setup.bash" >> ~/.bashrc