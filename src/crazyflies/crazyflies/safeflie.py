import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rcl_interfaces.msg import ParameterDescriptor

from std_msgs.msg import Empty, Float32
from crazyflies_interfaces.msg import SendTarget

from crazyflies.crazyflie import Crazyflie, CrazyflieType
from crazyflies.safe.safe_commander import SafeCommander


from typing import List
import signal
from enum import Enum, auto


class SafeflieState(Enum):
    IDLE = auto()
    TAKEOFF = auto()
    LAND = auto()
    TARGET = auto()

class Safeflie(Crazyflie):
    """
    A safe wrapper around the Crazyflie class which ensures that commands are safe to execute on real harware.
    """

    def __init__(
        self,
        node: Node,
        id: int,
        channel: int,
        initialPosition: List[float],
        type: CrazyflieType,
        tracked: bool = False
    ):
        super().__init__(node, id, channel, initialPosition, type, tracked)
        node.get_logger().info(f"Safeflie with ID {id} successfully initialized.")
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
            msg_type=Float32,
            topic=prefix + "/takeoff_to",
            callback=self._takeoff_to_callback,
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

        node.create_subscription(
            msg_type=Float32,
            topic=prefix + "/land_to",
            callback=self._land_to_callback,
            qos_profile=qos_profile,
            callback_group=callback_group,
        )   

        update_rate = 10.0  # Hz
        dt = 1 / update_rate

        self.commander = SafeCommander(
            dt=dt, max_step_distance_xy=3, max_step_distance_z=1, clipping_box=None
        )

        cmd_position_timer = self.node.create_timer(
            dt, self.__send_target, callback_group=callback_group
        )

        # self._sleep(0.3)  # Wait for crazyflie to be ready
        # block = self.create_log_block(["range.zrange"], "range", self.loginfo)
        # self._sleep(0.3)
        # block.start_log_block(20)  # 5 Hz

    def __send_target(self):
        if self.state is not SafeflieState.TARGET:
            return
        position = self.get_position()
        if position is not None and self.target is not None:
            safe_target = self.commander.safe_cmd_position(position, self.target)
            self.cmd_position(safe_target, 0.0)

    def _send_target_callback(self, msg: SendTarget) -> None:
        x, y, z = msg.target.x, msg.target.y, msg.target.z
        self.target = [x, y, z]

   

    def _takeoff_to_callback(self, msg: Float32) -> None:
        self.__takeoff(msg.data)

    def _takeoff_callback(self, msg: Empty) -> None:
        TAKEOFF_HEIGHT = 1.0
        self.__takeoff(TAKEOFF_HEIGHT)
  
    def _land_to_callback(self, msg: Float32) -> None:
        self.__land(msg.data)

    def _land_callback(self, msg: Empty) -> None:
        LAND_HEIGHT = 0.0
        self.__land(height=LAND_HEIGHT)

    def _sleep(self, duration: float) -> None:
        """Sleeps for the provided duration in seconds."""
        start = self.__time()
        end = start + duration
        while self.__time() < end:
            rclpy.spin_once(self.node, timeout_sec=0)

    def __time(self) -> "Time":
        """Return current time in seconds."""
        return self.node.get_clock().now().nanoseconds / 1e9

    def __takeoff(self, height: float) -> None:
        if self.state != SafeflieState.IDLE:
            self.node.get_logger().info("Cannot takeoff, not in IDLE state.")
            return

        position = self.get_position()
        if position is not None:
            self.target = position
            self.target[2] = height
            self.state = SafeflieState.TAKEOFF
            self.takeoff(target_height=height, duration_seconds=4.0)
            self._sleep(4.0)
            self.state = SafeflieState.TARGET
        else:
            raise Exception("Crazyflie doesnt have position. Cannot takeoff.")

    def __land(self, height: float) -> None:
        if self.state != SafeflieState.TARGET:
            self.node.get_logger().info("Cannot land, not in TARGET state.")
            return
        self.state = SafeflieState.LAND
        self.notify_setpoints_stop(200)
        self._sleep(0.01)  # Make sure the notify_setpoints_stop is sent before landing
        self.land(target_height=height, duration_seconds=4.0)
        self._sleep(duration=4.0)
        self.state = SafeflieState.IDLE

SHUTDOWN = False


def safe_shutdown(signum, frame):
    global SHUTDOWN
    SHUTDOWN = True


def main():
    rclpy.init()
    node = Node("safeflie")
    parameter_descriptor = ParameterDescriptor(dynamic_typing=True, read_only=True)
    cf_id: int = node.declare_parameter("id", descriptor=parameter_descriptor).get_parameter_value().integer_value
    cf_type: CrazyflieType = CrazyflieType(node.declare_parameter("type", descriptor=parameter_descriptor).get_parameter_value().integer_value)
    cf_channel: int = node.declare_parameter("channel", descriptor=parameter_descriptor).get_parameter_value().integer_value
    cf_tracked: bool = node.declare_parameter("tracked", descriptor=parameter_descriptor).get_parameter_value().bool_value
    cf_initial_position: List[float] = node.declare_parameter("initial_position", descriptor=parameter_descriptor).get_parameter_value().double_array_value

    safeflie = Safeflie(node, cf_id, cf_channel, cf_initial_position, cf_type, cf_tracked)

    signal.signal(signal.SIGINT, safe_shutdown)
    while rclpy.ok() and not SHUTDOWN:
        rclpy.spin_once(node)

    safeflie.close_crazyflie()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
