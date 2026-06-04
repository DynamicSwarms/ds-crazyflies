import os
import sys
import time
import unittest

import launch
import launch_ros
import launch_testing.actions

from launch.actions import IncludeLaunchDescription
from launch.launch_description import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


from ament_index_python.packages import get_package_share_directory
import rclpy


def generate_test_description():
    simulation_framework = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('crazyflies'), 'launch', 'framework.launch.py')
        ), 
        launch_arguments={'backend': 'SIMULATION'}.items()
    )

    safeflie_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('crazyflies'), 'launch', 'safeflie.launch.py')
        ),
        launch_arguments={
            'id': 231,
            'type': 'SIMULATION',
            'channel': 80,
            'initial_position': [0.0, 0.0, 0.0],
            'tracked': 'false'
        }.items()
    )

    return  LaunchDescription([
        simulation_framework, 
        safeflie_launch])