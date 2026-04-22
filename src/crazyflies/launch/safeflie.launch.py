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
    arg_tracked = LaunchConfiguration("tracked")

    cf_id = int(arg_id.perform(context))
    cf_type = CrazyflieType[arg_type.perform(context)].value
    cf_channel = int(arg_channel.perform(context))
    cf_tracked = arg_tracked.perform(context).lower() == "true"
    cf_initial_position = [
        float(x) for x in arg_initial_position.perform(context).strip("[]").split(",")
    ]

    safeflie = Node(
        package="crazyflies",
        executable="safeflie",
        name=f"safeflie{cf_id}",
        parameters=[
            {
                "id": cf_id,
                "type": cf_type,
                "channel": cf_channel,
                "tracked": cf_tracked,
                "initial_position": cf_initial_position,
            }
        ],
    )

    yield safeflie


def generate_launch_description():

    cf_id_launch_arg = DeclareLaunchArgument(
        "id", default_value="231", description="The ID of the crazyflie."  # E7 in hex
    )

    cf_type_launch_arg = DeclareLaunchArgument(
        name="type",
        default_value=CrazyflieType.HARDWARE.name,
        description=f"Wheter it should connect to a real, simulated or webots crazyflie.",
        choices=[
            CrazyflieType.HARDWARE.name,
            CrazyflieType.SIMULATION.name,
            CrazyflieType.WEBOTS.name,
        ],
    )

    cf_channel_launch_arg = DeclareLaunchArgument(
        "channel",
        default_value="80",
        description="The channel the crazyflie is on. Ignored if Webots.",
    )

    cf_tracked_launch_arg = DeclareLaunchArgument(
        name="tracked",
        default_value="false",
        description="Whether to use motion capture for tracking the crazyflie.",
        choices=["true", "false"],
    )
    cf_initial_position_launch_arg = DeclareLaunchArgument(
        name="initial_position",
        default_value="[0.0,0.0,0.0]",
        description="The initial position we expect the crazyflie to be at launch (Only relevant if tracked, or simulation).",
    )

    return LaunchDescription(
        [
            cf_id_launch_arg,
            cf_channel_launch_arg,
            cf_type_launch_arg,
            cf_tracked_launch_arg,
            cf_initial_position_launch_arg,
            OpaqueFunction(function=create_safeflie),
        ]
    )
