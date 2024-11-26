import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from crazyflies.crazyflie import Crazyflie, CrazyflieType

from crazyflies_interfaces.msg import SendTarget

from crazyflies.safe.safe_commander import SafeCommander

from typing import List
import signal


class Safeflie(Crazyflie):
    def __init__(
        self,
        node: Node,
        id: int,
        channel: int,
        initialPosition: List[float],
        type: CrazyflieType,
    ):
        super().__init__(node, id, channel, initialPosition, type)

        prefix = "/safeflie{}".format(id)
        qos_profile = 10
        callback_group = MutuallyExclusiveCallbackGroup()

        self.target: List[float] = initialPosition

        node.create_subscription(
            SendTarget,
            prefix + "/send_target",
            self._send_target_callback,
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

        update_rate = 10.0  # Hz
        dt = 1 / update_rate

        self.commander = SafeCommander(
            dt=dt, max_step_distance_xy=3, max_step_distance_z=1, clipping_box=None
        )

        cmd_position_timer = self.node.create_timer(dt, self.__send_target)

    def __send_target(self):
        position = self.get_position()
        if position is not None:
            safe_target = self.commander.safe_cmd_position(position, self.target)
            self.cmd_position(safe_target, 0.0)

    def _send_target_callback(self, msg: SendTarget) -> None:
        x, y, z = msg.target.x, msg.target.y, msg.target.z
        self.target = [x, y, z]


SHUTDOWN = False


def safe_shutdown(signum, frame):
    global SHUTDOWN
    SHUTDOWN = True


def main():
    rclpy.init()
    node = Node("safeflie", automatically_declare_parameters_from_overrides=True)
    cf_id: int = node.get_parameter("id").get_parameter_value().integer_value
    cf_channel: int = node.get_parameter("channel").get_parameter_value().integer_value
    cf_initial_position: List[float] = (
        node.get_parameter("initial_position").get_parameter_value().double_array_value
    )
    cf_type: CrazyflieType = CrazyflieType(
        node.get_parameter("type").get_parameter_value().integer_value
    )

    safeflie = Safeflie(node, cf_id, cf_channel, cf_initial_position, cf_type)

    signal.signal(signal.SIGINT, safe_shutdown)
    while rclpy.ok() and not SHUTDOWN:
        rclpy.spin_once(node)

    safeflie.close_crazyflie()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
