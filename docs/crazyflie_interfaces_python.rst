.. _crazyflie_interfaces_python:

Crazyflie Interfaces Python - Package 
=====================================

The package provides Server and Client classes which can be implemented. 
For coding your own application logic these client classes can be used, which automatically create the appropriate publishers.
If you want to implement your own backend the Server classes can be used to setup the appropriate subscribers.

E.g. the  ``Crazyflies`` implementation uses the ``client`` and maps python calls to ROS 2 topics.

.. note:: 
    For systems where performance is critical (e.g. swarms with many crazyflies), it is recommended to implement your own Client class which only implements the functionality you need. T
    This reduces the number of ROS Topic connections and therefore increases performance.



.. include:: crazyflie_interfaces_python_client.rst

