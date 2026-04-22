import os

from launch import LaunchDescription, LaunchContext

from ament_index_python.packages import get_package_share_directory

from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import LaunchConfigurationNotEquals, LaunchConfigurationEquals
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

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


def sitl_launch():
    sitl_crazyflie = Node(
        package="crazyflie_sitl",
        executable="crazyflie_sitl",
        parameters=[
            {
                "id": 231,
                "initial_position": [0.0, 0.0, 0.0],
            }
        ],
        output="screen",
    )
    return [sitl_crazyflie]


def hardware_launch():
    sitl_arg = DeclareLaunchArgument(
        "sitl",
        default_value="false",
        description="Whether to start the crazyflie sitl. "
        "This is useful for testing without hardware. "
        "backend must be set to hardware for this to work. "
        "(Dont activate tracking if using SITL.)",
    )

    tracked_arg = DeclareLaunchArgument(
        "tracked",
        default_value="false",
        description="Whether to use motion capture for tracking the crazyflies."
        "Only available if backend is set to hardware. "
        "Make sure to set up the motion capture system accordingly (modify IP in this launch file).",
    )

    hardware_gateway = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                get_package_share_directory("crazyflie_hardware_bringup"),
                "/launch/hardware.launch.py",
            ]
        ),
        launch_arguments={
            "sitl_udp_radio": LaunchConfiguration("sitl"),
        }.items(),
    )

    tracking = GroupAction(
        condition=LaunchConfigurationNotEquals("tracked", "false"),
        actions=tracking_launch(),
    )

    sitl = GroupAction(
        condition=LaunchConfigurationEquals("sitl", "true"),
        actions=sitl_launch(),
    )

    return [tracked_arg, sitl_arg, hardware_gateway, tracking, sitl]


def simulation_launch():
    simulation_gateway = Node(
        package="crazyflie_simulation_gateway",
        executable="gateway",
        name="crazyflie_simulation_gateway",
        output="screen",
    )

    return [simulation_gateway]


def generate_launch_description():
    backend_arg = DeclareLaunchArgument(
        "backend",
        default_value="sim",
        description="Select a crazyflie implementation to use.",
        choices=["hardware", "sim", "webots"],
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
            webots,
            position_visualization,
        ]
    )
