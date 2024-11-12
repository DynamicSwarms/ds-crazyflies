source /opt/ros/humble/setup.bash

ROOT=$PWD



cd src/dependencies/crazyflie_hardware/src/crazyflie_interfaces
touch COLCON_IGNORE
CRAZYFLIE_INTERFACES=$PWD
cd $ROOT

cd src/dependencies/crazyflie_hardware/src/crazyflie_interfaces_python
touch COLCON_IGNORE
CRAZYFLIE_INTERFACES_PYTHON=$PWD
cd $ROOT

colcon build


cd $CRAZYFLIE_INTERFACES
rm COLCON_IGNORE
cd $CRAZYFLIE_INTERFACES_PYTHON
rm COLCON_IGNORE

cd $ROOT