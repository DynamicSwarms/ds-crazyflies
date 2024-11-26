import os

from launch import LaunchDescription, LaunchContext

from ament_index_python.packages import get_package_share_directory

from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import LaunchConfigurationEquals
from launch_ros.actions import Node


from webots_ros2_driver.webots_launcher import WebotsLauncher


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

    motion_caputre = Node(
        condition=LaunchConfigurationEquals("backend", "hardware"),
        package="ros_motioncapture",
        executable="motioncapture_node",
        name="node",
        output="screen",
        parameters=[
            {
                "type": "vicon",
                "hostname": "172.20.37.251",
                "add_labeled_markers_to_pointcloud": True,
            }
        ],
    )

    config = os.path.join(
        get_package_share_directory("object_tracker"), "launch", "tracker_config.yaml"
    )

    object_tracker = Node(
        condition=LaunchConfigurationEquals("backend", "hardware"),
        package="object_tracker",
        # namespace='object_tracker',
        executable="tracker",
        name="tracker",
        parameters=[config],
    )

    wb = WebotsLauncher(
        # world="/home/winni/dynamic_swarms/crazywebotsworld/worlds/crazyflie.wbt",
        world="/home/winni/crazyflie.wbt"
    )

    return LaunchDescription(
        [
            wb,
            backend_arg,
            webots_gateway,
            hardware_gateway,
            motion_caputre,
            object_tracker,
        ]
    )
