.. _installation:

Installation
==============

.. toctree::
   :maxdepth: 100

This project was developed and testet for ROS Humble on following system configurations. 
It is recommended to also use a simmilar configuration.

====== =======
Ubuntu ROS
------ -------
20.04  Humble
22.04  Humble
====== =======

   


#. If you have not already done so install `ROS 2 Humble <https://docs.ros.org/en/humble/index.html>`_ on your system.

#. If you plan on using the webots installations

   .. code-block:: bash

      sudo apt-get install ros-humble-webots-ros2

#. These dependencies are necessary:

   .. code-block:: bash

      sudo apt-get install ros-humble-tf-transformations

#. Clone the `ds-crazyflies <https://github.com/DynamicSwarms/ds-crazyflies>`_ repository 

   .. code-block:: bash

      git clone https://github.com/DynamicSwarms/ds-crazyflies.git

#. Before building this repository the submodules need to be initialized

   .. code-block:: bash

      git submodules update --init --recursive

#. Source your ROS installation

   .. code-block:: bash
      
      source /opt/ros/humble/install/setup.bash

#. Build the software stack 

   .. code-block:: bash
      
      sh build.sh

.. note:: Because of the depency structure ``colcon build`` can not be executed directly. If you want to build only ``crazyflies`` package use: ``colcon build --packages-select crazyflies``

Webots Simulation
__________________

If you want to use the Webots Simulation you will also need to:

#. Install the Webots Simulator as described here: https://cyberbotics.com/

#. Download the `crazywebotsworld` repository:

   .. code-block:: bash

      git clone https://github.com/DynamicSwarms/crazywebotsworld.git

#. Build the controllers inside the World: 

   #. Open the world in ``crazywebotsworld/worlds/crazyflie.wbt``
   #. `Right Click` on the Crazyflie in the Scene Tree and select ``Edit Controller``
   #. Press the cog/gear symbol in the Editor to build the controllers
   #. Repeat step 2. and 3. for the `Wand` as well.

Visit the :doc:`Getting Started </getting_started>` page to start tinkering.