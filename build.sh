source /opt/ros/$ROS_DISTRO/setup.bash

ROOT=$PWD


# Optional mode argument
MODE=${1:-ALL}  # default is ALL build if no argument provided

cd src/dependencies/crazyflie_hardware/src/crazyflie_interfaces
touch COLCON_IGNORE
CRAZYFLIE_INTERFACES=$PWD
cd $ROOT

cd src/dependencies/crazyflie_hardware/src/crazyflie_interfaces_python
touch COLCON_IGNORE
CRAZYFLIE_INTERFACES_PYTHON=$PWD
cd $ROOT

# Decide which packages to skip based on mode
SKIP_PACKAGES=""
case "$MODE" in
    HARDWARE_ONLY)
        SKIP_PACKAGES="crazyflie_webots crazyflie_webots_examples crazyflie_webots_gateway"
        ;;
    WEBOTS_ONLY)
        SKIP_PACKAGES="crazyflie_hardware crazyflie_hardware_cpp crazyflie_hardware_examples crazyflie_hardware_gateway crazyflie_hardware_gateway_components"
        ;;
    ALL)
        SKIP_PACKAGES=""
        ;;
    *)
        echo "Unknown mode: $MODE"
        echo "Valid modes: HARDWARE_ONLY, WEBOTS_ONLY, ALL"
        exit 1
        ;;
esac

# Build
if [ -z "$SKIP_PACKAGES" ]; then
    colcon build
else
    colcon build --packages-skip $SKIP_PACKAGES
fi


cd $CRAZYFLIE_INTERFACES
rm COLCON_IGNORE
cd $CRAZYFLIE_INTERFACES_PYTHON
rm COLCON_IGNORE

cd $ROOT