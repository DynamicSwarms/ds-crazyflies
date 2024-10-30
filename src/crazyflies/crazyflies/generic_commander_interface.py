from rclpy.node import Node
from crazyflie_interfaces.msg import (
    NotifySetpointsStop,
    VelocityWorld,
    Hover,
    FullState,
    Position,
)  # (Generic)Commander
from typing import List


class GenericCommanderInterface:

    def __init__(self, node: Node, prefix: str):
        self.notify_setpoints_stop_publisher = node.create_publisher(
            NotifySetpointsStop, prefix + "/notify_setpoints_stop", 10
        )
        self.velocity_world_publisher = node.create_publisher(
            VelocityWorld, prefix + "/cmd_vel", 10
        )
        self.hover_publisher = node.create_publisher(Hover, prefix + "/cmd_hover", 10)
        self.full_state_publisher = node.create_publisher(
            FullState, prefix + "/cmd_full_state", 10
        )
        self.position_publisher = node.create_publisher(
            Position, prefix + "/cmd_position", 10
        )

    def notify_setpoints_stop(
        self, remain_valid_milliseconds: int = 100, group_mask: int = 0
    ) -> None:
        """Sends a notify setpoints command

        Args:
            remain_valid_milliseconds (int, optional): _description_. Defaults to 100.
            group_mask (int, optional): _description_. Defaults to 0.
        """
        pass

    def cmd_velocity_world(self, velocity: List[float], yawrate: float = 0.0) -> None:
        pass

    def cmd_hover(
        self,
        z_distance: float,
        velocity_x: float = 0.0,
        velocity_y: float = 0.0,
        yawrate: float = 0.0,
    ) -> None:
        """Send a hover command

        Args:
            z_distance (float): _description_
            velocity_x (float, optional): _description_. Defaults to 0.0.
            velocity_y (float, optional): _description_. Defaults to 0.0.
            yawrate (float, optional): _description_. Defaults to 0.0.
        """

    def cmd_full_state(
        self,
        position: List[float],
        velocity: List[float],
        acceleration: List[float],
        yaw: float,
        omega: List[float],
    ) -> None:
        """Sends a full-state controller setpoint command

        Args:
            position (List[float]): _description_
            velocity (List[float]): _description_
            acceleration (List[float]): _description_
            yaw (float): _description_
            omega (List[float]): _description_
        """
