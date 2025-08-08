.. _api:

API-Documentation
#################

.. toctree::
   :maxdepth: 1

In the `Usage <usage>`_ section, we showed how to use takeoff, land and go_to messages from the command line.  
Of course you can also write your own node which sends commands to the crazyflie by setting up publishers for the appropriate topics manually. The :doc:`crazyflie interfaces package </crazyflie_interfaces_python>` however provides python classes which can be used to avoid having to setup these publishers manually.


.. include:: crazyflies.rst

.. include:: crazyflie_interfaces_python.rst
