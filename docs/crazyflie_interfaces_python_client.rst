.. _crazyflie_interfaces_python_client:

``Crazyflie Interfaces Python Clients`` 
---------------------------------------

These clients are used to translate the ros2 topics to python functionality.
They represent an access point to the different components of the crazyflie interface.
The modules represent the different `CRTP ports <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/functional-areas/crtp/>`_
of the Crazyflie CRTP protocol. 

All classes are instantiated with a Node (:class:`rclpy.node.Node`) and a Prefix (:class:`str`). 
The modules will each create a :class:`rclpy.callback_group` to which they add publishers and subscriptions. 
The user is repsonsible for spinning the node. 
The Prefix is needed in order to map to the correct Crazyflie namespace. In most cases this is just ``/cfXX``, where XX is the id.

* :ref:`Console <console-client>`
* :ref:`Emergency <emergency-client>`
* :ref:`Generic Commander <generic-commander-client>`
* :ref:`High Level Commander <high-level-commander-client>`
* :ref:`Logging <logging-client>`
* :ref:`RPYT Commander <rpyt_commander-client>`


.. _console-client:

Console
_______

Whenever a console message is sent from the Crazyflie, it is published on the ``cfID/console`` topic.
The Console Client subscribes to this topic and calls a user provided callback function with the message content.

.. automodule:: crazyflie_interfaces_python.client.console
    :members:
    :undoc-members:


.. _emergency-client:

Emergency
_________

Unused and not implemented yet.

.. automodule:: crazyflie_interfaces_python.client.emergency
    :members:
    :undoc-members:


.. _generic-commander-client:

Generic Commander
_________________

This is the entry point to the Crazyflie's low level commander. 
The commands are sent directly to Crazyflie's controller. 
Sending position setpoints to far away points will crash the Crazyflie.
Also, be sure to call :meth:`notify_setpoints_stop <crazyflie_interfaces_python.client.generic_commander.GenericCommanderClient.notify_setpoints_stop>`
before sending high level commands again. 

.. warning::
    In the current implementations only `cmd_position` is implemented.
    Open a github issue if you need more low level commands imeplemented.


.. automodule:: crazyflie_interfaces_python.client.generic_commander
    :members:
    :undoc-members:

.. _high-level-commander-client:

High Level Commander
____________________

.. automodule:: crazyflie_interfaces_python.client.high_level_commander
    :members:
    :undoc-members:

.. _logging-client:

Logging
_______

Checkout :doc:`Logging </logging>` for more information about the logging framework.

.. automodule:: crazyflie_interfaces_python.client.logging
    :members:
    :undoc-members:

.. automodule:: crazyflie_interfaces_python.client.logblock
    :members:
    :undoc-members:

.. _rpyt_commander-client:

RPYT Commander
_______________

.. automodule:: crazyflie_interfaces_python.client.rpyt_commander
    :members:
    :undoc-members:
