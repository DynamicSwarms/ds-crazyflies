.. _usage:

Usage
*****

The `crazyflies` package provides a convenient launch file (`framework.launch.py <https://github.com/DynamicSwarms/ds-crazyflies/blob/master/src/crazyflies/launch/framework.launch.py>`_) which allows you to launch with hardware, webots or mixed crazyflies.


#. Sourcing (needs to be done in every new terminal):

    .. code-block:: bash

        source install/setup.bash
        export WEBOTS_HOME=/usr/local/webots
        

#. Launch the framework with:

    .. code-block:: bash

        ros2 launch crazyflies framework.launch.py backend:=webots

    Select `hardware`, `webots`, or `both` as your backend. 

#. When starting with `webots` or `both`. Only the backend for the simulation is started. You need to open Webots seperately and select the provided world (see :doc:`Installation </installation>`). (The Framework will then connect as extern controller to the Webots simulation).

#. Now it is time to connect your first crazyflie: 

    .. code-block:: bash

        ros2 service call /crazyflie_hardware_gateway/add_crazyflie crazyflie_hardware_gateway/srv/AddCrazyflie "id: 0
            channel: 100
            initial_position: [0.0, 0.0, 0.0]
            type: 'default'"

    The result should include a `success: true`.

#. Flight: 

    Takeoff

    .. code-block:: bash

        ros2 topic pub /cf0/takeoff crazyflie_interfaces/msg/Takeoff "group_mask: 0
            height: 0.5
            yaw: 0.0
            use_current_yaw: false
            duration: 2.0" --once

    GoTo

    .. code-block:: bash

        ros2 topic pub /cf0/go_to crazyflie_interfaces/msg/GoTo "group_mask: 0
            relative: true
            linear: false
            goal: [1.0, 0.0, 0.5] # TODO
            yaw: 0.0
            duration: 2.0" --once

    Land
    
    .. code-block:: bash

        ros2 topic pub /cf0/land crazyflie_interfaces/msg/Land "group_mask: 0
            height: 0.0
            yaw: 0.0
            use_current_yaw: false
            duration: 2.0" --once


Crazyflie / Safeflie
--------------------

If you want to start scripting your own application logic, you can use the `crazyflies` package to create a Crazyflie or Safeflie.
Familiarise yourself with the :doc:`Crazyflie and Safeflie  </crazyflies>` classes (the *crazyflies* package).

#. You can start your first Safeflie with: 

    .. code-block:: bash

        ros2 launch crazyflies safeflie.launch.py id:=0 channel:=100 initial_position:=[0.0,0.0,0.0] type:=2

    * **id**: The id of the crazyflie.
    * **channel**: The channel of the crazyflie, if a real crazyflie is used.
    * **initial_position**: The crazyflies initial position, if a real crazyflie is used.
    * **type**: 1 if you want to connect a hardware crazyflie. 2 if you want to connect a webots crazyflie.

The safeflie will automatically use the hardware or webots gateway to add the crazyflie. (no service call add required).


Start implementing your application logic with the :doc:`Crazyflie and Safeflie </crazyflies>` classes.

.. note:: Creating a Crazyflie/Safeflie will automatically set it up to be tracked by a motion capture system, but this is subject to change. If you instantiate a Crazyflie using the gateway (see :doc:`Usage</usage>` /:doc:`Architecture </architecture>`), then you may provide a type field.