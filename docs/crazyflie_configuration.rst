.. _crazyflie_configuration:

.. toctree::
   :maxdepth: 100

Crazyflie Configuration
========================

.. note::
    If you are not using real hardware crazyflies (webots simulation) you do not need to configure anything in software.
    For most basic hardware setups the default configuration is also sufficient.

For the hardware there are two `.yaml` files which are used to configure the Crazyflie. The default files are automatically loaded if no changes are made and should be sufficient for most use cases. If you need parameters to be set at startup or have a specific motion_capture setup you can create your own `.yaml` files and load them instead.

Both files are arguments of the `crazyflie_hardware_gateway.launch.py <https://github.com/DynamicSwarms/crazyflie_hardware/blob/master/src/crazyflie_hardware_gateway/launch/crazyflie_hardware_gateway.launch.py>`_ launch file. You can therefore pass the parameter ``crazyflie_types_yaml`` or ``crazyflie_configuration_yaml`` (`see <https://github.com/DynamicSwarms/crazyflie_hardware/blob/master/src/crazyflie_hardware_gateway/launch/crazyflie_hardware_gateway.launch.py>`_). 
Follow this tutorial to learn about ros2 launch arguments: `Using Substitutions <https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Using-Substitutions.html>`_.

When launching with the `framework.launch.py <https://github.com/DynamicSwarms/ds-crazyflies/blob/master/src/crazyflies/launch/framework.launch.py>`_ both arguments are passed through and can be used just like with the gateway. 

Crazyflie types (crazyflieTypes.yaml)
-------------------------------------

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


Crazyflie config (crazyflie_config.yaml)
-----------------------------------------

With the ``crazyflie_config.yaml`` you can define the default parameters which are loaded onto the crazyflie when it is connected.
As in :doc:`Parameters<parameters>` you can visit `Crazyflie Parameters <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/params/>`_ to find available parameters.
The most important setting here is the estimator and stabilizer used and in case you are using external tracking the input can be configured.

#. stabilizer.estimator: 1: complementary, 2: ekf
#. stabilizer.controller: 1: pid, 2: mellinger
#. locSrc.extPosStdDev: 1e-3: The standard deviation of the external position source, e.g. vicon/optitrack.

In the `default file <https://github.com/DynamicSwarms/crazyflie_hardware/blob/master/src/crazyflie_hardware/launch/crazyflie_config.yaml>`_ this is set to complementary estimator and mellinger controller. 



    
    
    