.. _implementation:


Different Implementations
=========================

There are two implementations available in the `crazyflie_hardware` repository. They can be selected with a launch argument in `crazyflie_hardware_gateway.launch.py <https://github.com/DynamicSwarms/crazyflie_hardware/blob/master/src/crazyflie_hardware_gateway/launch/crazyflie_hardware_gateway.launch.py>`_.


1. **C++**: The cpp implementation is more scalable and up to date implementation. Using this is the default and is recommended. 
   
2. **Python**: This version was implemented before the C++ version and has more features, such as the :doc:`Logging</logging>` interface. Also more crtp messages are implemented. The issue with the python version is, that rclpy nodes have very poor performance and have very high cpu load. Therefore using this implementation limits the number of crazyflies that can be used in a swarm (~10).

In the future the python implementation will be removed and the C++ implementation should be improved to not have these limitations.