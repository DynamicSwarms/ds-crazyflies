# Dynamic Swarms Crazyflies

A ROS2 stack for the [Crazyflie](https://www.bitcraze.io/) Nanoquadcopter.

This software stack was designed and testet with [ROS2Humble](https://docs.ros.org/en/humble/index.html) on Ubuntu 22.04 as well as Ubuntu 20.04.

> [!WARNING]
> This software is currently under development. Breaking changes will happen.

## Crazyflies

The crazyflies package allows the user to interchangeably use real hardware or a simulation based on [Webots](https://cyberbotics.com/).
There are two implementations. You can either use a [Crazyflie](/src/crazyflies/crazyflies/crazyflie.py) or a [Safeflie](/src/crazyflies/crazyflies/crazyflie.py). The Safeflie is a tuned down version of the crazyflie providing a topic "/cf_ID_/send_target" which allows to control the crazyflie without knowledge about the controller of the real hardware. 

Further documentation can be generated with the docs.

## Usage

The [launch.py](/src/crazyflies/launch/launch.py) can be configured to use appropriate tracking hardware if real crazyflies are used.
When launching this launch file the _backend_ argument should be provided specifying if the webots backend or the hardware backend shall be used.

Afterwards you can either implement your own node and either use or inherit from the Crazyflie or Safeflie class.
Examples will be provided soon.

## Implementations

There are currently 2 backends which are integrated into this software stack.
[Crazyflie Hardware](https://github.com/DynamicSwarms/crazyflie_hardware)
[Crazyflie Webots](https://github.com/DynamicSwarms/crazyflie_webots)


## Installation
Because both the hardware implementation as well as the webots implementation depend on the same packages the [build script](/build.sh) has to be used instead of _colcon build_. 