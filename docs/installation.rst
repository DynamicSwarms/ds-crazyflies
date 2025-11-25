.. _installation:

Installation
############

This project has been developed and tested for ROS2 Humble on following system configurations. 
It is recommended to also use a similar configuration.

====== =======
Ubuntu ROS
------ -------
22.04  Humble
====== =======
   
Step by Step Instructions
=========================

#. If you have not already done so install `ROS 2 Humble <https://docs.ros.org/en/humble/index.html>`_ on your system.

#. These dependencies are required:

   .. code-block:: bash

      sudo apt-get install ros-humble-tf-transformations ros-humble-ros2-control ros-humble-vision-msgs
      sudo apt install python3-colcon-common-extensions


#. Clone the `ds-crazyflies <https://github.com/DynamicSwarms/ds-crazyflies>`_ (this) repository 

   .. code-block:: bash

      git clone --recurse https://github.com/DynamicSwarms/ds-crazyflies.git

#. Now cd into the `ds-crazyflies` folder and: Source your ROS installation and the webots package

   .. code-block:: bash

      cd ds-crazyflies
      source /opt/ros/humble/setup.bash    

#. Build the software stack 

   There are 3 options to build the project:
   You can select between a full build, build for only the webots simulation or build for real hardware only.
   Set mode to one of the following options: ``ALL``, ``WEBOTS``, ``HARDWARE``.
      
   .. code-block:: bash
      
      sh build.sh ALL

.. warning:: 

   If the webots packages are build webots needs to be installed first (see below).
   Also the ``WEBOTS_HOME`` environment variable needs to be set before building.

   .. code-block:: bash
      
      export WEBOTS_HOME=/usr/local/webots

.. note:: 
   Because of the dependency structure, ``colcon build`` can not be executed directly. 
   If you only want to build the ``crazyflies`` package, use: 
   
   .. code-block::
      
      colcon build --packages-select crazyflies

Webots Simulation
*****************

If you want to use the Webots simulation you will also need to:

#. Install the Webots Simulator (We are currently supporting Webots2025a): 

   For this you can follow the instructions from Cyberbotics: https://cyberbotics.com/doc/guide/installation-procedure#installing-the-debian-package-with-the-advanced-packaging-tool-apt

   .. code-block:: bash

      sudo mkdir -p /etc/apt/keyrings
      cd /etc/apt/keyrings
      sudo wget -q https://cyberbotics.com/Cyberbotics.asc

   .. code-block::   bash

      echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/Cyberbotics.asc] https://cyberbotics.com/debian binary-amd64/" | sudo tee /etc/apt/sources.list.d/Cyberbotics.list
      sudo apt update

   .. code-block::   bash

      sudo apt install webots
   
#. Download the `crazywebotsworld` repository:

   .. code-block:: bash

      git clone https://github.com/DynamicSwarms/crazywebotsworld.git

#. Open webots with the world:

   .. code-block:: bash

      webots crazywebotsworld/worlds/crazyflie.wbt

.. note:: 
   Avoid installing Webots via snap as this causes issues with the ROS2 integration.

Next up follow the :doc:`Getting Started </getting_started>` guide.