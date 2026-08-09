# Dynamic Swarms Crazyflies

A ROS2 stack for the [Crazyflie](https://www.bitcraze.io/) Nanoquadcopter.

This software stack was designed and testet with [ROS2Lyrical](https://docs.ros.org/en/lyrical/index.html) on Ubuntu 26.04.

The documentation can be found here: https://dynamicswarms.github.io/ds-crazyflies/

> [!WARNING]
> This software is currently under development. Breaking changes will happen.

## Crazyflies

The crazyflies package allows the user to interchangeably use real hardware or a simulation.
There are two implementations. You can either use a [Crazyflie](/src/crazyflies/crazyflies/crazyflie.py) or a [Safeflie](/src/crazyflies/crazyflies/safeflie.py). The Safeflie is a tuned down version of the crazyflie providing a topic "/cf_ID_/send_target" which allows to control the crazyflie without knowledge about the controller of the real hardware. 

## Usage

The [framework.launch.py](/src/crazyflies/launch/framework.launch.py) can be configured to use appropriate tracking hardware if real crazyflies are used.
When launching this launch file the _backend_ argument should be provided specifying if the simulation backend or the hardware backend shall be used.

Afterwards you can either implement your own node and either use or inherit from the Crazyflie or Safeflie class.

## Implementations

There are currently 2 backends which are integrated into this software stack.
[Crazyflie Hardware](https://github.com/DynamicSwarms/crazyflie_hardware)
[Crazyflie Simulation](https://github.com/DynamicSwarms/crazyflie_simulation)

### SITL

With the hardware backend it is also possible to use a SITL crazyflie. 
Checkout [this](https://github.com/DynamicSwarms/crazyflie_sitl) repository for more information. 
(The crazyflie sitl can even be used with the official crazyflie-client-python)


## Installation
We use vcs for subrepository management. 
However there is a convenience script, for choosing different implemententations to be installed. 

The get started quickly: 

```
git clone https://github.com/DynamicSwarms/ds-crazyflies.git
cd ds-crazyflies
./setup.sh simulation
source opt/ros/lyrical/setup.bash
colcon build
```

