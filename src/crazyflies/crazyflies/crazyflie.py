import rclpy
from rclpy.node import Node
from typing import List
from enum import Enum

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


class Crazyflie(
    Node,
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
        self, id: int, initialPosition: List[float], type: CrazyflieType
    ) -> None:
        self.id = id
        prefix = "/cf{}".format(id)
        name = "cf{}_instance".format(id)
        super().__init__(name)

        loginfo = lambda msg: self.get_logger().info(msg)
        ConsoleClient.__init__(self, self, prefix, loginfo)
        EmergencyClient.__init__(self, self, prefix)
        GenericCommanderClient.__init__(self, self, prefix)
        HighLevelCommanderClient.__init__(self, self, prefix)
        LoggingClient.__init__(self, self, prefix)
        RPYTCommanderClient.__init__(self, self, prefix)

        self.create_timer(1, self.pub_position)

    def pub_position(self) -> None:
        self.cmd_position([1.0, 2.0, 0.0], 1.00)


def main():
    rclpy.init()
    cf = Crazyflie(5, [0.0, 0.0, 0.0], CrazyflieType.WEBOTS)
    rclpy.spin(cf)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
