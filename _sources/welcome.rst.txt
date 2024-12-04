.. _welcome:

Welcome to DynamicSwarms Crazyflies
===================================

.. toctree::
    :maxdepth: 100

The Dynamic Swarms Crazyflie project is a fully ROS2 based software stack, which allows you to control mulitple `Crazyflies <https://www.bitcraze.io/>`_ simultaniously.
The project was heavily inspired by the `Crazyswarm <https://crazyswarm.readthedocs.io/en/latest/>`_ and `Crazyswarm 2 <https://imrclab.github.io/crazyswarm2/>`_ project.
It provides the ability to add and remove Crazyflies safely during the runtime of the system. It is fully ROS2 based and allows you to access the radio communication directly.

In our development of a Crazyflie-Swarm-Middleware with up to 50 Crazyflies, which are charged with the QI-Charging deck we modified the `Crazyswarm <https://crazyswarm.readthedocs.io/en/latest/>`_
heavily in order to fullfill our needs. A key feature we needed was the ability to add and remove crazyflies during runtime. 

Because ROS Noetic has reached it's end of life and a transition to ROS 2 was imminent for us, we needed to decide if we wanted to integrate our changes into Crazyswarm2 or develop our own software stack with the knowledge we had gained. 
The Crazyswarm2 implementation did not come with improvements regarding our specific need and we therefor decide to develop this project.

This package also provides a `Webots <https://cyberbotics.com/>`_ simulation interface such that simulated crazyflies and real hardware crazyflies can be interchangeably used.

The following was created with our modified version of Crazswarm.

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; margin-bottom: 20pt; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/YTd9pCpeYuU" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>

What is different to `Crazyswarm 2 <https://imrclab.github.io/crazyswarm2/>`_?
---------------------------------------------------------------------------------

The crazyswarm2 projected especially the cpp implementation is implemented as one monolithic ROS Node.
This makes it hard to change and adapt the library to specific needs. 
A major difference is that crazyflie functionality (e.g. ``takeoff``) is not implemented as services but as topics.
This allows user code to be fully independent of the implementation, especially if a crazyflie fails this does not result in deadlock situations.
Especially if you do not know your swarm configuration at start-up the Crazyswarm(2) implementation is not suitable.

When should I use this library instead of `Crazyswarm 2 <https://imrclab.github.io/crazyswarm2/>`_?
----------------------------------------------------------------------------------------------------

* You want to add or remove Crazyflies during runtime?
* You want to change your configuration like logging variable during runtime?
* You want to be able to have low-level access directly to the CRTP-Protocoll with ROS?