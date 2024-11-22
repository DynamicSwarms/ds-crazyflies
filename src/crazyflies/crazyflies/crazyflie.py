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


from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

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
        self, node: Node, id: int, initial_position: List[float], type: CrazyflieType
    ):
        self.id = id
        self.tf_name = "cf{}".format(id)
        self.node = node

        prefix = "/cf{}".format(id)
        loginfo = lambda msg: node.get_logger().info(str(msg))
        ConsoleClient.__init__(self, node, prefix, loginfo)
        EmergencyClient.__init__(self, node, prefix)
        GenericCommanderClient.__init__(self, node, prefix)
        HighLevelCommanderClient.__init__(self, node, prefix)
        LoggingClient.__init__(self, node, prefix)
        RPYTCommanderClient.__init__(self, node, prefix)

        self.gateway_endpoint = GatewayEndpoint(node, type, id, initial_position)
        self.gateway_endpoint.open()

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self.node)

        # self.create_timer(1, self.pub_position)
        # block = self.create_log_block(["range.zrange"], "range", loginfo)
        # block.start_log_block(200)

    def get_position(self) -> List[float]:
        try:
            t = self.tf_buffer.lookup_transform(
                "world", self.tf_name, rclpy.time.Time()
            )
            return [
                t.transform.translation.x,
                t.transform.translation.y,
                t.transform.translation.z,
            ]
        except Exception as ex:
            return None

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
