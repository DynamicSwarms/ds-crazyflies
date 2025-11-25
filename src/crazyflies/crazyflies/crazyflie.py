import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup


from crazyflie_interfaces_python.client import (
    ConsoleClient,
    EmergencyClient,
    GenericCommanderClient,
    HighLevelCommanderClient,
    LoggingClient,
    RPYTCommanderClient,
)


from crazyflie_interfaces.msg import PoseStampedArray
import time

from .crazyflie_types import CrazyflieType
from .gateway_endpoint import GatewayEndpoint

from typing import List


class Crazyflie(
    ConsoleClient,
    EmergencyClient,
    GenericCommanderClient,
    HighLevelCommanderClient,
    LoggingClient,
    RPYTCommanderClient,
):
    """
    Represents a crazyflie.

    Allows user to interchangeably use different crazyflie implementations (currently Webots or Real Hardware)
    """

    def __init__(
        self,
        node: Node,
        id: int,
        channel: int,
        initial_position: List[float],
        type: CrazyflieType,
    ):
        self.id = id
        self.tf_name = "cf{}".format(id)
        self.node = node

        self.position = initial_position

        prefix = "/cf{}".format(id)
        self.loginfo = lambda msg: node.get_logger().info(str(msg))
        ConsoleClient.__init__(self, node, prefix, self.loginfo)
        EmergencyClient.__init__(self, node, prefix)
        GenericCommanderClient.__init__(self, node, prefix)
        HighLevelCommanderClient.__init__(self, node, prefix)
        LoggingClient.__init__(self, node, prefix)
        RPYTCommanderClient.__init__(self, node, prefix)

        self.gateway_endpoint = GatewayEndpoint(
            node, id, channel, initial_position, type
        )
        self.gateway_endpoint.open()

        self.cf_listener = node.create_subscription(
            PoseStampedArray,
            "/cf_positions",
            self.position_callback,
            10,
        )

    def get_position(self) -> List[float]:
        return self.position

    def position_callback(self, msg: PoseStampedArray):
        for pose in msg.poses:
            if pose.header.frame_id == self.tf_name:
                self.position = [
                    pose.pose.position.x,
                    pose.pose.position.y,
                    pose.pose.position.z,
                ]
                break

    def close_crazyflie(self):
        self.gateway_endpoint.close()


def main():
    rclpy.init()
    cf_id = 0
    name = "cf{}_instance".format(cf_id)
    node = Node(name)
    cf = Crazyflie(node, cf_id, [0.0, 0.0, 0.0], CrazyflieType.WEBOTS)
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
