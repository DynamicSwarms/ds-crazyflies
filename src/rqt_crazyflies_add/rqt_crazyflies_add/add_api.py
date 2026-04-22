from rclpy.node import Node
from rclpy.qos import qos_profile_services_default

from crazyflie_interfaces.srv import AddCrazyflie, RemoveCrazyflie
from geometry_msgs.msg import Pose


class AddApi:

    def __init__(self, node: Node):
        self._node = node

        service_qos = qos_profile_services_default
        service_qos.depth = 100  # The add all button should not have a limit

        self._add_hardware_client = self._node.create_client(
            AddCrazyflie,
            "crazyflie_hardware_gateway/add_crazyflie",
            qos_profile=service_qos,
        )
        self._remove_hardware_client = self._node.create_client(
            RemoveCrazyflie,
            "crazyflie_hardware_gateway/remove_crazyflie",
            qos_profile=service_qos,
        )

        self._add_simulation_client = self._node.create_client(
            AddCrazyflie,
            "crazyflie_simulation_gateway/add_crazyflie",
            qos_profile=service_qos,
        )
        self._remove_simulation_client = self._node.create_client(
            RemoveCrazyflie,
            "crazyflie_simulation_gateway/remove_crazyflie",
            qos_profile=service_qos,
        )

        self._add_webots_client = self._node.create_client(
            AddCrazyflie,
            "crazyflie_webots_gateway/add_crazyflie",
            qos_profile=service_qos,
        )
        self._remove_webots_client = self._node.create_client(
            RemoveCrazyflie,
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

        request = AddCrazyflie.Request()
        uri = f"radio://0/{channel}/2M/E7E7E7E7{id:02X}"

        request.uri = uri
        request.type = type
        initial_pose = Pose()
        if initial_position:
            initial_pose.position.x = initial_position[0]
            initial_pose.position.y = initial_position[1]
            initial_pose.position.z = initial_position[2]
        request.initial_pose = initial_pose

        self._add_hardware_client.call_async(request)

    def remove_hardware_crazyflie(self, id: int, channel: int):
        request = RemoveCrazyflie.Request()
        request.uri = f"radio://0/{channel}/2M/E7E7E7E7{id:02X}"

        self._remove_hardware_client.call_async(request)

    def add_webots_crazyflie(self, id: int):
        request = AddCrazyflie.Request()
        request.uri = f"webots://{id}"

        self._add_webots_client.call_async(request)

    def remove_webots_crazyflie(self, id: int):
        request = RemoveCrazyflie.Request()
        request.uri = f"webots://{id}"

        self._remove_webots_client.call_async(request)

    def add_simulation_crazyflie(
        self, id: int, initial_position: list[float] | None = None
    ):
        request = AddCrazyflie.Request()
        request.uri = f"sim://{id}"
        initial_pose = Pose()
        if initial_position:
            initial_pose.position.x = initial_position[0]
            initial_pose.position.y = initial_position[1]
            initial_pose.position.z = initial_position[2]
        request.initial_pose = initial_pose

        self._add_simulation_client.call_async(request)

    def remove_simulation_crazyflie(self, id: int):
        request = RemoveCrazyflie.Request()
        request.uri = f"sim://{id}"

        self._remove_simulation_client.call_async(request)
