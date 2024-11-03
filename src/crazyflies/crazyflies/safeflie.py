import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from crazyflies.crazyflie import Crazyflie, CrazyflieType

from typing import List

from crazyflies_interfaces.msg import SendTarget


class Safeflie(Crazyflie):
    def __init__(
        self, node: Node, id: int, initialPosition: List[float], type: CrazyflieType
    ):
        super().__init__(node, id, initialPosition, type)

        prefix = "/cf{}".format(id)
        qos_profile = 10
        callback_group = MutuallyExclusiveCallbackGroup()

        node.create_subscription(
            SendTarget,
            prefix + "/send_target",
            self._send_target_callback,
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

    def _send_target_callback(self, msg: SendTarget) -> None:
        if self.id != msg.cf_id:
            return

        x, y, z = msg.target.x, msg.target.y, msg.target.z
        self.cmd_position([x, y, z], 0.0)


def main():
    rclpy.init()
    name = "safeflie"
    node = Node(name)
    try:
        Safeflie(node, 0, [0.0, 0.0, 0.0], CrazyflieType.WEBOTS)
        rclpy.spin(node)
    except Exception as e:
        node.get_logger().info(f"Error: {e}")
        rclpy.shutdown()


if __name__ == "__main__":
    main()
