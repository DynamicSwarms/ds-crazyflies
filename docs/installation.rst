.. _installation:

Installation
==============

.. toctree::
   :maxdepth: 100

This project has been developed and tested for ROS Humble on following system configurations. 
It is recommended to also use a similar configuration.

====== =======
Ubuntu ROS
------ -------
20.04  Humble
22.04  Humble
====== =======

   


#. If you have not already done so install `ROS 2 Humble <https://docs.ros.org/en/humble/index.html>`_ on your system.

#. If you plan to use the webots installations

   .. code-block:: bash

      sudo apt-get install ros-humble-webots-ros2

#. These dependencies are required:

   .. code-block:: bash

      sudo apt-get install ros-humble-tf-transformations

#. Clone the `ds-crazyflies <https://github.com/DynamicSwarms/ds-crazyflies>`_ repository 

   .. code-block:: bash

      git clone https://github.com/DynamicSwarms/ds-crazyflies.git

#. Before building this repository the submodules need to be initialized

   .. code-block:: bash

      git submodule update --init --recursive

#. Source your ROS installation

   .. code-block:: bash
      
      source /opt/ros/humble/install/setup.bash

#. Build the software stack 

   .. code-block:: bash
      
      sh build.sh

.. note:: Because of the dependency structure, ``colcon build`` can not be executed directly. If you only want to build the ``crazyflies`` package, use: ``colcon build --packages-select crazyflies``

Webots Simulation
__________________

If you want to use the Webots simulation you will also need to:

#. Install the Webots Simulator as described here: https://cyberbotics.com/

#. Download the `crazywebotsworld` repository:

   .. code-block:: bash

      git clone https://github.com/DynamicSwarms/crazywebotsworld.git

#. Build the controllers inside the world: 

   #. Open the world found at ``crazywebotsworld/worlds/crazyflie.wbt``.
   #. `Right click` on the Crazyflie in the scene tree and select ``Edit Controller``.
   #. Press the gear icon in the editor to build the controllers.
   #. Repeat steps 2 and 3 for the `Wand`.

Visit the :doc:`Getting Started </getting_started>` page to start tinkering.
