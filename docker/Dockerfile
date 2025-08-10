# syntax=docker/dockerfile:1

# ROS distribution to use
ARG ROS_DISTRO=humble

FROM osrf/ros:${ROS_DISTRO}-desktop-full AS base
ENV ROS_DISTRO=${ROS_DISTRO}
SHELL ["/bin/bash", "-c"]

# Install some basic packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip gdb dos2unix wget
# Install ros dependencies
RUN apt-get install -y ros-humble-tf-transformations ros-humble-ros2-control

# Install webots
RUN wget -q https://github.com/cyberbotics/webots/releases/download/R2023b/webots-R2023b-x86-64.tar.bz2 \
 && tar -xjf webots-R2023b-x86-64.tar.bz2 \
 && mv webots /usr/local/webots \
 && ln -s /usr/local/webots/webots /usr/local/bin/webots \
 && rm webots-R2023b-x86-64.tar.bz2
ENV WEBOTS_HOME=/usr/local/webots

RUN mkdir -p /ds && chmod 777 /ds
RUN useradd -ms /bin/bash devuser && \
    echo "devuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER devuser

RUN git config --global --add safe.directory /ds/ds-crazyflies

# Install webots ros
WORKDIR /ds
RUN git clone -b 2023.1.2 --recurse-submodules https://github.com/cyberbotics/webots_ros2.git
WORKDIR /ds/webots_ros2
RUN source /opt/ros/humble/setup.bash &&\
    colcon build 

# Install ds-crazyflies
WORKDIR /ds
COPY --chown=devuser . ./ds-crazyflies
WORKDIR /ds/ds-crazyflies
RUN source /opt/ros/${ROS_DISTRO}/setup.bash &&\
    source /ds/webots_ros2/install/setup.bash &&\
    git submodule update --init --recursive &&\
    dos2unix build.sh &&\
    bash build.sh

# Install webotsworld
WORKDIR /ds
RUN git clone https://github.com/DynamicSwarms/crazywebotsworld.git
    

# Make controllers
WORKDIR /ds/crazywebotsworld/controllers/crazyflie_controller 
RUN make
WORKDIR /ds/crazywebotsworld/controllers/wand_ctrl_controller
RUN make

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc \
    && echo "source /ds/ds-crazyflies/install/setup.bash" >> ~/.bashrc