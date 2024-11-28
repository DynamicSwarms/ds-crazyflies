.. _crazyflie_interfaces_python_client:

.. toctree::

``Crazyflie Interfaces Python Client`` 
--------------------------------------

These clients are used to translate the ros2 topics to python functionality.
They represent an access point to the different components of the crazyflie interface.
The modules represent the different `CRTP Ports <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/functional-areas/crtp/>`_
of the crazyflie crtp protocoll. 

All classes are instantiated with a Node (:class:`rclpy.node.Node`) and a Prefix (:class:`str`). 
The modules will each create a :class:`rclpy.callback_group` in which they add publishers and subscriptions. 
The user is repsonsible for spinning the node. 
The Prefix is needed in order to map to the correct crazylie namespace. In most cases this is only ``/cfXX``, with XX beeing the id.


Console
^^^^^^^

This module does not have functionality at the moment. 
You might be able to receive the crazyflies console with this module in the future.

.. automodule:: crazyflie_interfaces_python.client.console
    :members:
    :undoc-members:

Emergency
^^^^^^^^^

.. automodule:: crazyflie_interfaces_python.client.emergency
    :members:
    :undoc-members:

Generic Commander 
^^^^^^^^^^^^^^^^^

This is the entry point to the low level commander of the crazyflie. 
The commands will get passed directly into the controller of the crazyflie. 
Sending position setpoints to far distant points will crash the crazyflie.
Also ensure to call notify :meth:`notify_setpoints_stop <crazyflie_interfaces_python.client.generic_commander.GenericCommanderClient.notify_setpoints_stop>`,
before sending high level commands again. 

.. automodule:: crazyflie_interfaces_python.client.generic_commander
    :members:
    :undoc-members:

High Level Commander
^^^^^^^^^^^^^^^^^^^^

.. automodule:: crazyflie_interfaces_python.client.high_level_commander
    :members:
    :undoc-members:

Logging
^^^^^^^

.. automodule:: crazyflie_interfaces_python.client.logging
    :members:
    :undoc-members:

RPYT Commander
^^^^^^^^^^^^^^

.. automodule:: crazyflie_interfaces_python.client.rpyt_commander
    :members:
    :undoc-members:
