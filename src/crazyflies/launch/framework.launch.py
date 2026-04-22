import os

from launch import LaunchDescription, LaunchContext

from ament_index_python.packages import get_package_share_directory

from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import LaunchConfigurationNotEquals, LaunchConfigurationEquals
from launch_ros.actions import Node

from launch.actions import GroupAction


def webots_launch():
    webots_gateway = Node(
        package="crazyflie_webots_gateway",
        executable="gateway",
        name="crazyflie_webots_gateway",
        output="screen",
        parameters=[
            {
                "webots_port": 1234,
                "webots_use_tcp": False,
                "webots_tcp_ip": "127.0.0.1",
            }
        ],
    )

    wand = Node(
        package="crazyflie_webots",
        executable="wand",
        name="Wand1",
        parameters=[
            {
                "id": 1,
                "webots_port": 1234,
                "webots_use_tcp": False,
                "webots_tcp_ip": "127.0.0.1",
            }
        ],
        output="screen",
    )

    return [webots_gateway, wand]


def tracking_launch():
    motion_capture = Node(
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
        package="object_tracker",
        executable="tracker",
        name="tracker",
        parameters=[config],
    )

    return [motion_capture, object_tracker]


def hardware_launch():
    tracked_arg = DeclareLaunchArgument(
        "tracked",
        default_value="false",
        description="Whether to use motion capture for tracking the crazyflies. Make sure to set up the motion capture system accordingly (modify IP in this launch file).",
    )

    hardware_gateway = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                get_package_share_directory("crazyflie_hardware_bringup"),
                "/launch/hardware.launch.py",
            ]
        )
    )

    tracking = GroupAction(
        condition=LaunchConfigurationNotEquals("tracked", "false"),
        actions=tracking_launch(),
    )

    return [hardware_gateway, tracked_arg, tracking]


def simulation_launch():
    simulation_gateway = Node(
        package="crazyflie_simulation_gateway",
        executable="gateway",
        name="crazyflie_simulation_gateway",
        output="screen",
    )

    return [simulation_gateway]


def generate_launch_description():
    hardware_bringup_dir = get_package_share_directory("crazyflie_hardware_bringup")

    backend_arg = DeclareLaunchArgument(
        "backend",
        default_value="sim",
        description="Select used backend, choose  'hardware', 'sim', 'webots'.",
    )

    # In Jazzy we can use Substitions with Equals and Or
    # Then we can also start combinations.

    hardware = GroupAction(
        condition=LaunchConfigurationEquals("backend", "hardware"),
        actions=hardware_launch(),
    )

    simulation = GroupAction(
        condition=LaunchConfigurationEquals("backend", "sim"),
        actions=simulation_launch(),
    )

    webots = GroupAction(
        condition=LaunchConfigurationEquals("backend", "webots"),
        actions=webots_launch(),
    )

    position_visualization = Node(
        package="crazyflies",
        executable="position_visualization",
        name="position_visualization",
    )

    return LaunchDescription(
        [
            backend_arg,
            hardware,
            simulation,
            # webots,
            position_visualization,
        ]
    )
