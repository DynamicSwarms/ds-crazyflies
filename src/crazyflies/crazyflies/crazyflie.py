import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from typing import List
from enum import Enum

from crazyflie_webots_gateway_interfaces.srv import WebotsCrazyflie
from crazyflie_hardware_gateway_interfaces.srv import Crazyflie as HardwareCrazyflie

from crazyflie_interfaces_python.client import (
    ConsoleClient,
    EmergencyClient,
    GenericCommanderClient,
    HighLevelCommanderClient,
    LoggingClient,
    RPYTCommanderClient,
)


class CrazyflieType(Enum):
    HARDWARE = 1
    WEBOTS = 2


class CrazyflieInitializationError(Exception):
    pass


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
        self, node: Node, id: int, initialPosition: List[float], type: CrazyflieType
    ):
        self.id = id
        prefix = "/cf{}".format(id)

        loginfo = lambda msg: node.get_logger().info(str(msg))
        ConsoleClient.__init__(self, node, prefix, loginfo)
        EmergencyClient.__init__(self, node, prefix)
        GenericCommanderClient.__init__(self, node, prefix)
        HighLevelCommanderClient.__init__(self, node, prefix)
        LoggingClient.__init__(self, node, prefix)
        RPYTCommanderClient.__init__(self, node, prefix)

        callback_group = MutuallyExclusiveCallbackGroup()

        if type == CrazyflieType.WEBOTS:
            webots_creation = node.create_client(
                WebotsCrazyflie,
                "/crazyflie_webots_gateway/add_crazyflie",
                callback_group=callback_group,
            )
            if not webots_creation.wait_for_service(1.0):
                raise CrazyflieInitializationError(
                    "Initialization of crazyflie failed, webots_gateway not available!"
                )

            creation_request = WebotsCrazyflie.Request()
            creation_request.id = id
            (
                creation_request.initial_position.x,
                creation_request.initial_position.y,
                creation_request.initial_position.z,
            ) = initialPosition
            creation_request.type = "default"

            response: WebotsCrazyflie.Response = webots_creation.call(creation_request)

            if not response.success:
                raise CrazyflieInitializationError(
                    "Initialization of crazyflie failed, webots_gateway responded with false!"
                )

        # self.create_timer(1, self.pub_position)
        # block = self.create_log_block(["range.zrange"], "range", loginfo)
        # block.start_log_block(200)

    # def pub_position(self) -> None:
    # self.cmd_position([1.0, 2.0, 0.0], 1.00)


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
