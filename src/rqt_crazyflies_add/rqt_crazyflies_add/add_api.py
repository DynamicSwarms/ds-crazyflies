from rclpy.node import Node
from rclpy.qos import qos_profile_services_default

from crazyflie_hardware_gateway_interfaces.srv import (
    AddCrazyflie as AddHardwareCrazyflie,
    RemoveCrazyflie as RemoveHardwareCrazyflie,
)
from crazyflie_webots_gateway_interfaces.srv import WebotsCrazyflie
from geometry_msgs.msg import Point


class AddApi:

    def __init__(self, node: Node):
        self._node = node

        service_qos = qos_profile_services_default
        service_qos.depth = 100  # The add all button should not have a limit

        self._add_hardware_client = self._node.create_client(
            AddHardwareCrazyflie,
            "crazyflie_hardware_gateway/add_crazyflie",
            qos_profile=service_qos,
        )
        self._remove_hardware_client = self._node.create_client(
            RemoveHardwareCrazyflie,
            "crazyflie_hardware_gateway/remove_crazyflie",
            qos_profile=service_qos,
        )
        self._add_webots_client = self._node.create_client(
            WebotsCrazyflie,
            "crazyflie_webots_gateway/add_crazyflie",
            qos_profile=service_qos,
        )
        self._remove_webots_client = self._node.create_client(
            WebotsCrazyflie,
            "crazyflie_webots_gateway/remove_crazyflie",
            qos_profile=service_qos,
        )

    def add_hardware_crazyflie(
        self,
        id: int,
        channel: int,
        type: str,
        initial_position: list[float] | None = None,
    ):

        request = AddHardwareCrazyflie.Request()
        request.id = id
        request.channel = channel
        request.type = type
        request.initial_position = (
            Point(x=initial_position[0], y=initial_position[1], z=initial_position[2])
            if initial_position
            else Point()
        )

        self._add_hardware_client.call_async(request)

    def remove_hardware_crazyflie(self, id: int):
        request = RemoveHardwareCrazyflie.Request()
        request.id = id

        self._remove_hardware_client.call_async(request)

    def add_webots_crazyflie(self, id: int):
        request = WebotsCrazyflie.Request()
        request.id = id

        self._add_webots_client.call_async(request)

    def remove_webots_crazyflie(self, id: int):
        request = WebotsCrazyflie.Request()
        request.id = id

        self._remove_webots_client.call_async(request)
