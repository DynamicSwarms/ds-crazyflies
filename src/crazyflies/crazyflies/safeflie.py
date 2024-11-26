import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from crazyflies.crazyflie import Crazyflie, CrazyflieType

from std_msgs.msg import Empty

from crazyflies_interfaces.msg import SendTarget
from crazyflies.safe.safe_commander import SafeCommander

from typing import List
import signal
from enum import Enum, auto


class SafeflieState(Enum):
    IDLE = auto()
    TAKEOFF = auto()
    LAND = auto()
    TARGET = auto()


from builtin_interfaces.msg import Duration


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
        self.state: SafeflieState = SafeflieState.IDLE

        prefix = "/safeflie{}".format(id)
        qos_profile = 10
        callback_group = MutuallyExclusiveCallbackGroup()

        self.target: List[float] = None

        node.create_subscription(
            SendTarget,
            prefix + "/send_target",
            self._send_target_callback,
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

        node.create_subscription(
            msg_type=Empty,
            topic=prefix + "/takeoff",
            callback=self._takeoff_callback,
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

        node.create_subscription(
            msg_type=Empty,
            topic=prefix + "/land",
            callback=self._land_callback,
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
        if position is not None and self.target is not None:
            safe_target = self.commander.safe_cmd_position(position, self.target)
            self.cmd_position(safe_target, 0.0)

    def _send_target_callback(self, msg: SendTarget) -> None:
        x, y, z = msg.target.x, msg.target.y, msg.target.z
        self.target = [x, y, z]

    def _takeoff_callback(self, msg: Empty) -> None:
        TAKEOFF_HEIGHT = 1.0

        position = self.get_position()
        if position is not None:
            self.target = position
            self.target[2] = TAKEOFF_HEIGHT

            self.takeoff(target_height=TAKEOFF_HEIGHT, duration_seconds=4.0)
            self.state = SafeflieState.TARGET
        else:
            raise Exception("Crazyflie doesnt have position. Cannot takeoff.")

    def _land_callback(self, msg: Empty) -> None:
        LAND_HEIGHT = 0.0
        self.land(target_height=LAND_HEIGHT, duration_seconds=4.0)
        self.state = SafeflieState.IDLE


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
