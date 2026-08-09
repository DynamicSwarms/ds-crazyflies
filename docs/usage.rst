.. _usage:

Usage
*****

The `crazyflies` package provides a convenient launch file (`framework.launch.py <https://github.com/DynamicSwarms/ds-crazyflies/blob/master/src/crazyflies/launch/framework.launch.py>`_) which allows you to launch with different configurations such as with real hardware, the simulation, webots or sitl.

We will first show how to use the framework with the simulation, using it with real hardware is very similar and selfexplanatory afterwards.


#. Sourcing (needs to be done in every new terminal):

    .. code-block:: bash

        source install/setup.bash        

#. Launch the framework with:

    .. code-block:: bash

        ros2 launch crazyflies framework.launch.py backend:=simulation


#. Now it is time to connect your first crazyflie. To simplify this process `ds-crazyflies` provides two panels for RQT.
     
    -    For this RQT first needs to discover these plugins, for this run the following command in a new terminal (in the ds-crazyflies folder):

        .. code-block:: bash

            source install/setup.bash
            rqt --force-discover

        .. image:: assets/rqt_plugins.png
            :alt: Alternate text
            :width: 400px
            :height: 300px
            :align: center

        You should now find two new plugins in the RQT plugin list.
        Add both Plugins to your View.

        .. note::
            When inside VSCode ``unset GTK_PATH`` needs to be run before starting RQT, otherwise it will not start.

    - The `Add Plugin` can then be used to connnect the crazyflie. 

        Choose the correct backend and provide the necessary parameters. 
        

        .. image:: assets/add_plugin.png
                    :alt: Alternate text
                    :width: 300px
                    :height: 300px
                    :align: center

    - The connected crazyflies are now listed in the Crazyflie List plugin.

        From here you can monitor the battery voltage and connection status of each crazyflie.
        For the simulated crazyflies most values do not update. 
        When a crazyflie disconnects it will be greyed out.

        .. image:: assets/state_plugin.png
                    :alt: Alternate text
                    :width: 600px
                    :height: 200px
                    :align: center

        The small control button to the left of the PropellerTest button opens a small high level commander interface.

        Here you can send takeoff, goTo and land commands to the crazyflie.
        The position field should also update correctly.


Hardware
========

    When `hardware` is selected it is necessary to set the `radio_channels` argument: 
    If using external tracking (e.g. Vicon, OptiTrack), set `tracked:=true`.

    .. Note::
        Currently OptiTrack compilation is broken. Only Vicon is currently supprted.
    
    .. code-block:: bash

        ros2 launch crazyflies framework.launch.py backend:=hardware radio_channels:=[80] tracked:=false

SITL
____

    To launch in SITL mode there is an extra argument ``sitl`` which needs to be set to true.

    .. code-block:: bash

        ros2 launch crazyflies framework.launch.py backend:=hardware sitl:=true

    This will automaitcally start a SITL crazyflie, which can be added just like a hardware crazyflie.

Webots
======

    Starting with `webots` will **not** automatically open Webots. You need to open Webots seperately and select the provided world (see :doc:`Installation </installation>`). (The Framework will then connect as extern controller to the Webots simulation).

    .. code-block:: bash

        ros2 launch crazyflies framework.launch.py backend:=webots

    Then in the RQT-Panel add a webots crazyflie with id 0.

Usage without RQT
=================

    The RQT-Plugins are just convenient buttons for service calls and topic publications.
    You can also connect a crazyflie by calling the appropriate service directly.

#. For connecting a hardware crazyflie:
    
    .. code-block:: bash

        ros2 service call /crazyflie_hardware_gateway/add_crazyflie crazyflie_interfaces/srv/AddCrazyflie "
            uri: 'radio://0/80/2/E7E7E7E7<ID>'
            initial_position: [0.0, 0.0, 0.0]
            type: 'default'"

    For connecting a simulated crazyflie:

    .. code-block:: bash

        ros2 service call /crazyflie_simulation_gateway/add_crazyflie crazyflie_interfaces/srv/AddCrazyflie "uri: 'sim://0'"

    The result should include a `success=True`.
    
#. When the crazyflie is connected, you can use the high level commander to control the crazyflie: 

    * Takeoff

        .. code-block:: bash

            ros2 service call /cf231/takeoff crazyflie_interfaces/srv/Takeoff "group_mask: 0
                height: 1.0
                yaw: 0.0
                duration:
                    sec: 4
                    nanosec: 0"

    * goTo

        .. code-block:: bash

            ros2 service call /cf231/go_to crazyflie_interfaces/srv/GoTo "group_mask: 0
                relative: false
                goal:
                    x: 0.0
                    y: 1.0
                    z: 1.0
                yaw: 0.0
                duration:
                    sec: 4
                    nanosec: 0" 


    * Land

        .. code-block:: bash

            ros2 service call /cf231/land crazyflie_interfaces/srv/Land "group_mask: 0
                height: 0.0
                yaw: 0.0
                duration:
                    sec: 4
                    nanosec: 0" 


Checkout the :doc:`/safeflie` documentation next as an example of how to use the framework in your own nodes.