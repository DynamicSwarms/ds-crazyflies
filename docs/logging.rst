.. _logging:

Logging
#######

.. toctree:: 
    :maxdepth: 1

The Crazyflie's logging feature allows data to be streamed from the Crazyflie to a PC.
By defining so called ``Log Blocks``, the user can define which variables should be logged.
A ``Log Block`` consists of several variables.
A list of `Logging groups and variables <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/logs/>`_ is available on the bitcraze website. 
Depending on your firmware version some variables might not be available. 

Depending on your used :doc:`Implementation </implementation>` the logging framework is implemented differently. 


CPP (Hardware) Implementation
******************

For the cpp-crazyflie it is currently not possible to start and end ``LogBlock`` during runtime.
Checkout `/dependencies/crazyflie_hardware/src/crazyflie_hardware_cpp/src/crtp_driver/logging.cpp` to see how the state logging is implemented.

The cpp implementation automatically logs one log block to the topic ``/cfID/state`` consisting of the following variables:

    - `pm.vbat <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/logs/#pmvbat>`_
    - `pm.chargeCurrent <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/logs/#pmchargecurrent>`_
    - `pm.state <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/logs/#pmstate>`_
    - `sys.canfly <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/logs/#syscanfly>`_
    - `sys.isFlying <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/logs/#sysisflying>`_
    - `sys.isTumbled <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/logs/#sysistumbled>`_

If the crazyflie is also set to default (no external tracking) there will be an additional log block. This block will not be published as a GenericLogBlock topic but insted on the global `/cf_positions` topic. 


Webots Implementation
**********************

The logging framework is implemented as a ROS2 topic interface:

.. When using hardware crazyflies with the python implementation, the first time you connect a crazyflie to this library, a folder called ``home/.crazyflies`` will be created. In this folder you will find the downloaded table of contents (the variables that are actually available).

When using the webots simulation, a limited subset of logging variables is available. 
Calling the ``cfID/get_logging_toc_info`` topic will print all available logging variables to the console. (You should avoid calling this on a hardware Crazyflie).

.. code-block:: bash
    
    ros2 topic pub /cf0/get_logging_toc_info std_msgs/msg/Empty --once


Creating a Log Block
====================

When a Crazyflie is connected, a ROS topic called ``cfID/create_log_block`` is available (where ID is the id of the Crazyflie).
The msg definition is as follows and can be found `here <https://github.com/DynamicSwarms/crazyflie_interfaces/blob/master/msg/LogBlock.msg>`_:

.. code-block:: 
    :caption: LogBlock.msg

    string[] variables
    string name

In variables you can add multiple log variables, e.g. ``pm.vbat``. The name can be choosen freely.
In the following we assume that we have chosen ``pm_log`` as the name.

.. code-block:: bash

    ros2 topic pub /cf0/create_log_block crazyflie_interfaces/msg/LogBlock "variables: ['pm.vbat'] 
    name: 'pm_log'" --once

After sending this, 3 new topics will be created: 

*  ``cfID/log/pm_log/start``
*  ``cfID/log/pm_log/stop``
*  ``cfID/log/pm_log/data``

.. note:: There is a maximum of 28 bytes available for each log block. Ensure that you do not have too many variables in your block.

Starting a LogBlock
===================

The ``start`` topic starts the log block on the crazyflie with a defined logging periode. The type of the topic is encoded using a `std_msgs/Int16 <https://docs.ros.org/en/humble/p/std_msgs/interfaces/msg/Int16.html>`_. 

.. note:: The unit is [10ms]. A frequency of 1 Hz is obtained by setting this to 100.

.. code-block:: bash

    ros2 topic pub /cf0/log/pm_log/start std_msgs/msg/Int16 "data: 100" --once

Receiving Data
==============

When the log block is started, the data streamed by the crazyflie is posted to the ``data`` topic as `GenericLogBlock <https://github.com/DynamicSwarms/crazyflie_interfaces/blob/master/msg/GenericLogData.msg>`_ messages: 

.. code-block:: 
    :caption: GenericLogBlock.msg

    float64[] values

The values are sorted as described when the log block was created.

.. code-block:: bash

    ros2 topic echo /cf0/log/pm_log/data

Stopping a Log Block
====================

A log block can be stopped by sending an `Empty <https://docs.ros.org/en/humble/p/std_msgs/interfaces/msg/Empty.html>`_ message to the provided topic.

.. code-block:: bash

    ros2 topic pub /cf0/log/pm_log/stop std_msgs/msg/Empty --once

.. note::
    
    When creating and starting log block with code it is important to add a delay between creating the log block and starting it.
    This is because the appropriate topics need to be created first.