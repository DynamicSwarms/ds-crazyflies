.. _installation:

Installation
############

This project has been developed and tested for ROS2 Lyrical on following system configurations. 
It is recommended to also use a similar configuration.

====== =======
Ubuntu ROS
------ -------
26.04  Lyrical
====== =======
   
Step by Step Instructions
=========================

#. If you have not already done so install `ROS 2 Lyrical <https://docs.ros.org/en/lyrical/index.html>`_ on your system.

#. These dependencies are required:

   .. code-block:: bash

      sudo apt-get install ros-lyrical-tf-transformations
      sudo apt install python3-colcon-common-extensions

#. Clone the `ds-crazyflies <https://github.com/DynamicSwarms/ds-crazyflies>`_ (this) repository 

   .. code-block:: bash

      git clone https://github.com/DynamicSwarms/ds-crazyflies.git
      cd ds-crazyflies

#. Configure what you want to build with the setup script.

   .. code-block:: bash

      ./setup.sh [options]

   Available options are:
   
   - ``hardware``: This will allow you to use real crazyflies with a crazyradio and external tracking systems.

   - ``simulation``: A lightweight simulation that can be used for testing.

   
   - ``sitl``: The crazyflie firmware as software in the loop. Requires ``hardware`` to be selected as well.

   .. tabs::

      .. tab:: Recommended Build

         .. code-block:: bash

            ./setup.sh simulation hardware
      

#. Build the workspace with colcon:

   .. code-block:: bash

      source /opt/ros/humble/setup.bash    
      colcon build


End of Life Support for Webots
==========================

Webots support will be removed in the future. 
Probably it currently still works, if you want to, try the following:



.. tabs::

   .. tab:: Build with Webots


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
            
            #. Configure with the ``webots`` option. 

               .. code-block:: bash

                  ./setup.sh webots
                  
            #. Export the webots home variable before building.

               .. code-block:: bash

                  export WEBOTS_HOME=/usr/local/webots



The webots world is not included in this repository. It needs to be downloaded separately:

   #. Download the `crazywebotsworld` repository:

      .. code-block:: bash

         git clone https://github.com/DynamicSwarms/crazywebotsworld.git

   #. Open webots with the world:

      .. code-block:: bash

         webots crazywebotsworld/worlds/crazyflie.wbt


Next up follow the :doc:`Getting Started </getting_started>` guide.