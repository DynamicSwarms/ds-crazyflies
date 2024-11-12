import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

from .crazyflie_types import CrazyflieType

from crazyflie_webots_gateway_interfaces.srv import WebotsCrazyflie
from crazyflie_hardware_gateway_interfaces.srv import Crazyflie as HardwareCrazyflie

from enum import Enum, auto


class CrazyflieGatewayError(Exception):
    pass


class GatewayQueryType(Enum):
    CREATE = auto()
    CLOSE = auto()


class GatewayEndpoint:
    gateway_names = {
        CrazyflieType.WEBOTS: "crazyflie_webots_gateway",
        CrazyflieType.HARDWARE: "crazyflie_hardware_gateway",
    }
    query_names = {
        GatewayQueryType.CREATE: "add_crazyflie",
        GatewayQueryType.CLOSE: "remove_crazyflie",
    }

    def __init__(self, node: Node, type: CrazyflieType):
        self.node = node
        self.type = type

    def open(self, cf_id, initial_position):
        self.cf_id = cf_id
        if self.type == CrazyflieType.WEBOTS:
            self.__create_webots_crazyflie(cf_id, initial_position)
        elif self.type == CrazyflieType.HARDWARE:
            pass

    def close(self):
        if self.type == CrazyflieType.WEBOTS:
            self.__close_webots_crazyflie(self.cf_id)
        elif self.type == CrazyflieType.HARDWARE:
            pass

    def __query_gateway(self, query_type: GatewayQueryType, service_type, request):
        client = self.node.create_client(
            service_type,
            "/{}/{}".format(
                self.gateway_names[self.type], self.query_names[query_type]
            ),
            callback_group=MutuallyExclusiveCallbackGroup(),
        )
        if not client.wait_for_service(1.0):
            raise CrazyflieGatewayError(
                "{} failed, {} not available!".format(
                    self.query_names[query_type], self.gateway_names[self.type]
                )
            )

        future = client.call_async(request)
        rclpy.spin_until_future_complete(self.node, future)
        response = future.result()

        if not response.success:
            raise CrazyflieGatewayError(
                "{} call to {} responded with false!".format(
                    self.query_names[query_type], self.gateway_names[self.type]
                )
            )

    #### WEBOTS SPECIFIC METHODS
    def __create_webots_crazyflie(self, cf_id, initial_position):
        creation_request = WebotsCrazyflie.Request()
        creation_request.id = cf_id
        (
            creation_request.initial_position.x,
            creation_request.initial_position.y,
            creation_request.initial_position.z,
        ) = initial_position
        creation_request.type.data = "default"

        self.__query_gateway(GatewayQueryType.CREATE, WebotsCrazyflie, creation_request)

    def __close_webots_crazyflie(self, cf_id):
        close_request = WebotsCrazyflie.Request()
        close_request.id = cf_id
        self.__query_gateway(GatewayQueryType.CLOSE, WebotsCrazyflie, close_request)
