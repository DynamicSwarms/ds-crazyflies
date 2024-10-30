import rclpy
from rclpy.node import Node
from typing import List
from enum import Enum

from crazyflies.crazyflies.high_level_commander_interface import HighLevelCommanderInterface

class CrazyflieType(Enum):
    HARDWARE = 1
    WEBOTS =   2 

class Crazyflie(Node, HighLevelCommanderInterface):
    """
    Represents a crazyflie. 

    Allows user to interchangeably use different crazyflie implementations (currently Webots or Real Hardware)
    """
    def __init__(self, id: int, initialPosition: List[float], type: CrazyflieType) -> None:
        name = "cf{}_instance".format(id)
        super(Node, self).__init__(name)

        self.id = id
        prefix = "/cf{}".format(id)


        HighLevelCommanderInterface.__init__(self, prefix)
        
    





