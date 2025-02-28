.. _getting_started:

.. toctree:: 
    :maxdepth: 100


Getting started
===================


Familiarise yourself with the :doc:`Crazyflie and Safeflie  </crazyflies>` classes (the *crazyflies* package).

#. If you want to use the simulation start Webots first, select the provided world (see :doc:`Installation </installation>`).


#. Launch the framework with:

    .. code-block:: bash

        ros2 launch crazyflies framework.launch.py backend:=webots

    Select `hardware`, `webots`, or `both` as your backend. 

#. You can start your first Safeflie with: 

    .. code-block:: bash

        ros2 launch crazyflies safeflie.launch.py id:=0 channel:=100 initial_position:=[0.0,0.0,0.0] type:=2

    * **id**: The id of the crazyflie.
    * **channel**: The channel of the crazyflie, if a real crazyflie is used.
    * **initial_position**: The crazyflies initial position, if a real crazyflie is used.
    * **type**: 1 if you want to connect a hardware crazyflie. 2 if you want to connect a webots crazyflie.


Start implementing your application logic with the :doc:`Crazyflie and Safeflie </crazyflies>` classes.


Setting up Motion Capture
-------------------------

In the file `framework.launch.py <https://github.com/DynamicSwarms/ds-crazyflies/blob/master/src/crazyflies/launch/framework.launch.py>`_ you can configure the motion_capture system you are using.
You can refer to this file: `motion_capture.cpp <https://github.com/DynamicSwarms/libmotioncapture/blob/main/src/motioncapture.cpp>`_ for your specific motion capture system.

Marker Configuration and Dynamics Configuration
________________________________________________
In the  `framework.launch.py <https://github.com/DynamicSwarms/ds-crazyflies/blob/master/src/crazyflies/launch/framework.launch.py>`_ you can also pass your own version of `Tracker Configuration <https://github.com/DynamicSwarms/ros-objecttracker/blob/master/object_tracker/launch/tracker_config.yaml>`_.
This allows you can define the marker arrangement you placed on your crazyfle.

There you can also define the dynamics configuration used by the tracker. 

.. note:: Creating a Crazyflie/Safeflie will automatically set it up to be tracked by a motion capture system, but this is subject to change. If you instantiate a Crazyflie using the gateway (see :doc:`Architecture </architecture>`), then you may provide a type field.



Crazyflie types
---------------

When launching the `Crazyflie Hardware Gateway` (`framework.launch.py <https://github.com/DynamicSwarms/ds-crazyflies/blob/master/src/crazyflies/launch/framework.launch.py>`_)
you can also pass the parameter ``crazyflie_types_yaml`` (`see <https://github.com/DynamicSwarms/crazyflie_hardware/blob/master/src/crazyflie_hardware_gateway/launch/crazyflie_hardware_gateway.launch.py>`_).

With the ``crazyflie_types_yaml`` you can define the configuration with which a crazyflie is launched. 
The `default file <https://github.com/DynamicSwarms/crazyflie_hardware/blob/master/src/crazyflie_hardware_gateway/launch/crazyflieTypes.yaml>`_ used describes two types of Crazyflies. 
One `tracked` and another `untracked`. This type can be used when calling ``gateway/add_crazyflie``.

    .. code-block:: 

        crazyflieTypes:
        tracked: 
            sendExternalPosition: true
            sendExternalPose: false
            maxInitialDeviation: 0.4
            markerConfigurationIndex: 4
            dynamicsConfigurationIndex: 0

    * **sendExternalPosition**: Use external tracking such as vicon/optitrack
    * **sendExternalPose**: Sends not only the position but also the pose to the crazyflie (untested)
    * **maxInitialDeviation**: Currently not fully implemented. If the crazyflie is added to the tracking service and there is no point close, returns false (being ingored)
    * **markerConfigurationIndex**: The marker configuration index as described above
    * **dynamicsConfigurationIndex**: The dynamicsConfigurationIndex as described above
