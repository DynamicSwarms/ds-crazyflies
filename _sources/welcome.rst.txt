.. _welcome:

Welcome to DynamicSwarms Crazyflies
###################################

.. toctree::
    :maxdepth: 2

The Dynamic Swarms Crazyflie project is a fully ROS2 based software stack that allows you to control multiple `Crazyflies <https://www.bitcraze.io/>`_ simultaneously.
The project was heavily inspired by the `Crazyswarm <https://crazyswarm.readthedocs.io/en/latest/>`_ and `Crazyswarm 2 <https://imrclab.github.io/crazyswarm2/>`_ projects.
It provides the ability to safely add and remove Crazyflies while the system is running. It is completely ROS2 based and therefore allows you to access the radio and other internal mechanisms directly.

In our development of a Crazyflie Swarm Middleware with up to 50 Crazyflies, which are charged with the `QI-Charging Deck <https://www.bitcraze.io/products/qi-1_2-charger-deck/>`_, we modified the `Crazyswarm <https://crazyswarm.readthedocs.io/en/latest/>`_ project heavily to meet our needs. A key feature we needed was the ability to add and remove Crazyflies at runtime.

As ROS Noetic reached it's `end of life <http://wiki.ros.org/Distributions>`_ we wanted to move to ROS 2 and had to decide whether to integrate our changes into `Crazyswarm 2 <https://imrclab.github.io/crazyswarm2/>`_ or use the knowledge gained to develop our own software stack. 
The `Crazyswarm 2 <https://imrclab.github.io/crazyswarm2/>`_ implementation did not come with any improvements regarding our specific needs, so we decided to develop this project.

This package also provides a `Webots <https://cyberbotics.com/>`_ simulation interface so that simulated Crazyflies and real hardware Crazyflies can be used interchangeably.

The following was created using our modified version of `Crazyswarm <https://crazyswarm.readthedocs.io/en/latest/>`_.

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; margin-bottom: 20pt; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/YTd9pCpeYuU" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>

What is the difference to `Crazyswarm 2 <https://imrclab.github.io/crazyswarm2/>`_?
***********************************************************************************

The `Crazyswarm 2 <https://imrclab.github.io/crazyswarm2/>`_ project, specifically the cpp backend, is implemented as a monolithic Ros2 node.
This makes it difficult to modify and adapt the library to specific needs. 
Our implementation has a ros **node for each Crazyflie**, which allows for way better flexibility and scalability.

This seperation into nodes also makes it much easier to **add and remove Crazyflies during runtime**.
Especially if you do not know your swarm configuration at startup, the Crazyswarm(2) implementation is not suitable.

A major difference is that crazyflie functionalities, such as ``takeoff, land, etc``, are not implemented as services but as topics.
This allows user code to be completely independent of the implementation, avoiding deadlocks when a crazyflie fails.

When should I use this library instead of `Crazyswarm 2 <https://imrclab.github.io/crazyswarm2/>`_?
***************************************************************************************************

* Do you want to add or remove Crazyflies during runtime?
* Want to have low-level access to the CRTP protocol directly from ROS?
* Do you want to change your configuration at runtime, such as logging variables :doc:`* </logging>`?
* Want to have a large swarm of 10-50 Crazyflies?
