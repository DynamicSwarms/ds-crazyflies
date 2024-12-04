.. _logging:

Logging
========

.. toctree:: 
    :maxdepth: 100

The logging feature of the Crazyflie allows to stream data from the crazyflie to the PC. 
By defining so called ``Log Blocks`` the user can define which variables should be logged.
A ``Log Block`` consists of multiple variables.
A List of `Logging groups and variables <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/logs/>`_ is available on the bitcraze website. 
Depending on your firmware version some variables might not be available. 

If you connect a crazyflie with this library for the first time a folder ``home/.crazyflies`` will be created. In this folder you can find the downloaded Table of Contents (The variables which are actually available).

If using the webots simulation a limited subset of logging variables is available. 
By calling the topic ``cfID/get_logging_toc_info`` all available logging variables are printed to the console. (You should avoid calling this to a hardware crazyflie.)


Creating a Log Block
--------------------
When a crazyflie is connected a Ros-Topic will be available called ``cfID/create_log_block`` (ID beeing the id of the crazyflie). 
The msg definition is as follows and can be found `here <https://github.com/DynamicSwarms/crazyflie_interfaces/blob/master/msg/LogBlock.msg>`_:

.. code-block:: 
    :caption: LogBlock.msg

    string[] variables
    string name

In variables you can add mulitple log variables e.g. ``pm.vbat``. The name can be choosen arbitrarily.
In the following we assume we have chosen ``pm_log`` as the name.

After sending this 3 new topics will be created: 

*  ``cfID/log/pm_log/start``
*  ``cfID/log/pm_log/stop``
*  ``cfID/log/pm_log/data``

.. note:: There is a maximum of 28 bytes available for each log block. Make sure not too many variables are inside your Block.

Starting a LogBlock
-------------------

With the ``start`` topic you can start the log block on the crazyflie. The type is of `std_msgs/Int16 <https://docs.ros.org/en/humble/p/std_msgs/interfaces/msg/Int16.html>`_. 
With the data field of the message the logging period of the block will be defined. 

.. note:: The unit is a 10th of a ms. A Frequency of 1 Hz is achieved by setting this to 100.

Receiving Data
------------------

After the log block is started the data streamed from the crazyflie will be published to the ``data`` topic as `GenericLogBlock <https://github.com/DynamicSwarms/crazyflie_interfaces/blob/master/msg/GenericLogData.msg>`_ messages: 

.. code-block:: 
    :caption: GenericLogBlock.msg

    float64[] values

The values are sorted as described when the log block was created.

Stopping a Log Block
--------------------

A log block can be stopped by sending an `Empty <https://docs.ros.org/en/humble/p/std_msgs/interfaces/msg/Empty.html>`_ message to the provided topic.
