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

.. tabs::

   .. tab:: Full Build

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

         .. note:: 
            Avoid installing Webots via snap as this causes issues with the ROS2 integration.
         
      #. Now cd into the `ds-crazyflies` folder and source your ROS installation.

         .. code-block:: bash

            cd ds-crazyflies
            source /opt/ros/humble/setup.bash    
            export WEBOTS_HOME=/usr/local/webots

      #. Build the software stack

         .. code-block:: bash
         
            sh build.sh ALL

   .. tab:: Hardware Only

      #. `cd` into the `ds-crazyflies` folder and source your ROS installation.

         .. code-block:: bash

            cd ds-crazyflies
            source /opt/ros/humble/setup.bash    

      #. Build the software stack 

         .. code-block:: bash
         
            sh build.sh HARDWARE_ONLY   
   
   .. tab:: Webots Only

         Currently not supported

.. note:: 
   Because of the dependency structure, ``colcon build`` can not be executed directly. 
   If you only want to build the ``crazyflies`` package, use: 
   
   .. code-block::
      
      colcon build --packages-select crazyflies

The webots world is not included in this repository. It needs to be downloaded separately:

   #. Download the `crazywebotsworld` repository:

      .. code-block:: bash

         git clone https://github.com/DynamicSwarms/crazywebotsworld.git

   #. Open webots with the world:

      .. code-block:: bash

         webots crazywebotsworld/worlds/crazyflie.wbt


Next up follow the :doc:`Getting Started </getting_started>` guide.