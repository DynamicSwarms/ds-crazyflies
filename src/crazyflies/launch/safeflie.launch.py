from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration

from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

crazyflies_package = get_package_share_directory("crazyflies")
import sys

sys.path.append(crazyflies_package)
from crazyflies.crazyflie_types import CrazyflieType


def create_safeflie(context):
    arg_id = LaunchConfiguration("id")
    arg_channel = LaunchConfiguration("channel")
    arg_initial_position = LaunchConfiguration("initial_position")
    arg_type = LaunchConfiguration("type")

    cf_id = int(arg_id.perform(context))
    cf_channel = int(arg_channel.perform(context))
    cf_initial_position = [
        float(x) for x in arg_initial_position.perform(context).strip("[]").split(",")
    ]
    cf_type = int(arg_type.perform(context))

    safeflie = Node(
        package="crazyflies",
        executable="safeflie",
        name=f"safeflie{cf_id}",
        parameters=[
            {
                "id": cf_id,
                "channel": cf_channel,
                "initial_position": cf_initial_position,
                "type": cf_type,
            }
        ],
    )

    yield safeflie


def generate_launch_description():

    cf_id_launch_arg = DeclareLaunchArgument(
        "id", default_value="231", description="The ID of the crazyflie."  # E7 in hex
    )

    cf_channel_lauch_arg = DeclareLaunchArgument(
        "channel",
        default_value="100",
        description="The channel the crazyflie is on. Ignored if Webots.",
    )

    cf_initial_position_launch_arg = DeclareLaunchArgument(
        name="initial_position",
        default_value="[0.0,0.0,0.0]",
        description="The initial posiition we expect the crazyflie to be at launch.",
    )

    cf_type_launch_arg = DeclareLaunchArgument(
        name="type",
        default_value=f"{CrazyflieType.WEBOTS.value}",
        description=f"Wheter it should spawn as a simulated crazyflie or a real one. Hardware: {CrazyflieType.HARDWARE.value}, Webots: {CrazyflieType.WEBOTS.value}",
    )

    return LaunchDescription(
        [
            cf_id_launch_arg,
            cf_channel_lauch_arg,
            cf_initial_position_launch_arg,
            cf_type_launch_arg,
            OpaqueFunction(function=create_safeflie),
        ]
    )
