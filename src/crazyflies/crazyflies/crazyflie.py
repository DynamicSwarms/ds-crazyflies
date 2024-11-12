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


from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


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

        if type == CrazyflieType.WEBOTS:
            self.create_webots_crazyflie(id, initial_position)

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

    def create_webots_crazyflie(self, cf_id, initial_position):
        callback_group = MutuallyExclusiveCallbackGroup()
        webots_creation = self.node.create_client(
            WebotsCrazyflie,
            "/crazyflie_webots_gateway/add_crazyflie",
            callback_group=callback_group,
        )
        if not webots_creation.wait_for_service(1.0):
            raise CrazyflieInitializationError(
                "Initialization of crazyflie failed, webots_gateway not available!"
            )

        creation_request = WebotsCrazyflie.Request()
        creation_request.id = cf_id
        (
            creation_request.initial_position.x,
            creation_request.initial_position.y,
            creation_request.initial_position.z,
        ) = initial_position
        creation_request.type.data = "default"

        future = webots_creation.call_async(creation_request)

        rclpy.spin_until_future_complete(self.node, future)
        response: WebotsCrazyflie.Response = future.result()

        if not response.success:
            raise CrazyflieInitializationError(
                "Initialization of crazyflie failed, webots_gateway responded with false!"
            )

    def close_webots_crazyflie(self):
        callback_group = MutuallyExclusiveCallbackGroup()
        webots_close = self.node.create_client(
            WebotsCrazyflie,
            "/crazyflie_webots_gateway/remove_crazyflie",
            callback_group=callback_group,
        )
        if not webots_close.wait_for_service(1.0):
            raise CrazyflieInitializationError(
                "Closing of crazyflie failed, webots_gateway not available!"
            )

        close_request = WebotsCrazyflie.Request()
        close_request.id = self.id

        future = webots_close.call_async(close_request)

        rclpy.spin_until_future_complete(self.node, future)
        response: WebotsCrazyflie.Response = future.result()

        if not response.success:
            raise CrazyflieInitializationError(
                "Closing of crazyflie failed, webots_gateway responded with false!"
            )


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
