import os
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="collision_avoidance_examples",  # Change this to your actual package name
                executable="collision_avoidance_test",
                name="collision_avoidance_node",
                output="screen",
            ),
            Node(
                package="collision_avoidance",  # Change this to your actual package name
                executable="collision_avoidance_node",
                name="collision_avoidance_node",
                output="screen",
            ),
            Node(package="rviz2", executable="rviz2", name="rviz2", output="screen"),
        ]
    )
