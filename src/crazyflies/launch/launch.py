from launch import LaunchDescription, LaunchContext

from ament_index_python.packages import get_package_share_directory

from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import LaunchConfigurationEquals


def generate_launch_description():
    package_dir = get_package_share_directory("crazyflies")

    webots_dir = get_package_share_directory("crazyflie_webots_gateway")
    hardware_dir = get_package_share_directory("crazyflie_hardware_gateway")

    backend_arg = DeclareLaunchArgument(
        "backend",
        default_value="webots",
        description="Select used backend, currently only 'webots' or 'hardware' supported.",
    )

    webots_gateway = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([webots_dir, "/launch/gateway.launch.py"]),
        condition=LaunchConfigurationEquals("backend", "webots"),
    )

    hardware_gateway = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [hardware_dir, "/launch/crazyflie_hardware_gateway.launch.py"]
        ),
        condition=LaunchConfigurationEquals("backend", "hardware"),
    )

    return LaunchDescription([backend_arg, webots_gateway, hardware_gateway])
