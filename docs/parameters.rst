.. _parameters:

Parameters
===========

.. toctree:: 
    :maxdepth: 1

The crazyflie's  parameters are directly mapped and connected to the corresponding ROS2 parameters.

Get a list of all parameters by writing:

.. code-block:: bash

    ros2 param list /cf0

in the terminal.
What each parameter does can be found on the `official bitcraze documentation <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/params/>`_.

.. note:: The parameters are not initialized when a crazyflie is connected, as this would require to poll hundrets of parameters. Therefore ``ros2 param get ..`` will not work until a parameter is set.
    To find out the default value of the parameter use the crazyflie client or investigate the source code. 


For setting parameters you can use the following command:

.. code-block:: bash

    ros2 param set /cf0 <parameter_name> <value>

this will not only set the node's parameter but also update the parameter on the crazyflie.
