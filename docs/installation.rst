.. _installation:

Installation
############

This project has been developed and tested for ROS2 Humble on following system configurations. 
It is recommended to also use a similar configuration.

====== =======
Ubuntu ROS
------ -------
20.04  Humble
22.04  Humble
====== =======
   
Step by Step Instructions
=========================

#. If you have not already done so install `ROS 2 Humble <https://docs.ros.org/en/humble/index.html>`_ on your system.

#. These dependencies are required:

   .. code-block:: bash

      sudo apt-get install ros-humble-tf-transformations ros-humble-ros2-control

#. Clone the `ds-crazyflies <https://github.com/DynamicSwarms/ds-crazyflies>`_ (this) repository 

   .. code-block:: bash

      git clone https://github.com/DynamicSwarms/ds-crazyflies.git

#. Before building this repository the submodules need to be initialized

   .. code-block:: bash

      git submodule update --init --recursive

#. Source your ROS installation

   .. code-block:: bash
      
      source /opt/ros/humble/setup.bash

#. Install colcon

   .. code-block:: bash
      
      sudo apt install python3-colcon-common-extensions

#. Build the software stack 

   .. code-block:: bash
      
      sh build.sh

.. note:: 
   Because of the dependency structure, ``colcon build`` can not be executed directly. 
   If you only want to build the ``crazyflies`` package, use: 
   
   .. code-block::
      
      colcon build --packages-select crazyflies

Webots Simulation
*****************

If you want to use the Webots simulation you will also need to:

#. Install the Webots Simulator (**Webots 2023b is required**)

   Either

      from: https://cyberbotics.com/ select `Older Versions` and download Webots 2023b.
   
   or 

   .. code-block:: bash

      wget -q https://github.com/cyberbotics/webots/releases/download/R2023b/webots-R2023b-x86-64.tar.bz2 
      tar -xjf webots-R2023b-x86-64.tar.bz2 
      mv webots /usr/local/webots 
      ln -s /usr/local/webots/webots /usr/local/bin/webots 
      rm webots-R2023b-x86-64.tar.bz2


#. Also the `ros-humble-webots-ros2` package needs to be installed:    

   Build the webots_ros2 package from source into a directory of your choice. When building (`sh build.sh`) this package then also needs to be sourced.

   .. code-block:: bash

      git clone -b 2023.1.2 --recurse-submodules https://github.com/cyberbotics/webots_ros2.git
      source /opt/ros/humble/setup.bash
      colcon build 



   .. note::
      The apt package is currently broken (doesn't check for version). In the future the following might suffice:


      .. code-block:: bash

         sudo apt-get install ros-humble-webots-ros2

#. Download the `crazywebotsworld` repository:

   .. code-block:: bash

      git clone https://github.com/DynamicSwarms/crazywebotsworld.git

#. Build the controllers inside the world: 

   #. Open the world found at ``crazywebotsworld/worlds/crazyflie.wbt``.
   #. `Right click` on the Crazyflie in the scene tree and select ``Edit Controller``.
   #. Press the gear icon in the editor to build the controllers.
   #. Repeat steps 2 and 3 for the `Wand`.

Next up follow the :doc:`Getting Started </getting_started>` guide.