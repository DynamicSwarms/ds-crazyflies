import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

from .crazyflie_types import CrazyflieType

from crazyflie_webots_gateway_interfaces.srv import WebotsCrazyflie
from crazyflie_hardware_gateway_interfaces.srv import Crazyflie as HardwareCrazyflie

from enum import Enum, auto

from typing import List, Type, Callable, Any
from dataclasses import dataclass


class CrazyflieGatewayError(Exception):
    pass


class GatewayQueryType(Enum):
    CREATE = auto()
    CLOSE = auto()


@dataclass
class gateway:
    name: str
    add: str
    remove: str
    service_type: Type
    is_success: Callable[[Any], bool]


class GatewayEndpoint:
    webots_gateway = gateway(
        name="crazyflie_webots_gateway",
        add="add_crazyflie",
        remove="remove_crazyflie",
        service_type=WebotsCrazyflie,
        is_success=lambda response: response.success,
    )
    hardware_gateway = gateway(
        name="crazyflie_hardware_gateway",
        add="add_crazyflie",
        remove="remove_crazyflie",
        service_type=HardwareCrazyflie,
        is_success=lambda response: response.success,
    )

    def __init__(
        self,
        node: Node,
        crazyflie_type: CrazyflieType,
        cf_id: float,
        initial_position: List[float],
    ):
        self.node: Node = node
        channel = 100

        self.request = None
        self.gateway = None
        if crazyflie_type == CrazyflieType.WEBOTS:
            self.request = self.__create_webots_request(cf_id, initial_position)
            self.gateway = self.webots_gateway
        elif crazyflie_type == CrazyflieType.HARDWARE:
            self.request = self.__create_hardware_request(
                cf_id, channel, initial_position
            )
            self.gateway = self.hardware_gateway

        if self.request is None or self.gateway is None:
            raise CrazyflieGatewayError(
                "Opening connection failed. No gateway available for {}".format(
                    crazyflie_type.name
                )
            )

    def open(self):
        self.__query_gateway(GatewayQueryType.CREATE, self.request)

    def close(self):
        self.__query_gateway(GatewayQueryType.CLOSE, self.request)

    def __query_gateway(self, query_type: GatewayQueryType, request):
        query_name = (
            self.gateway.add
            if query_type is GatewayQueryType.CREATE
            else self.gateway.remove
        )

        client = self.node.create_client(
            self.gateway.service_type,
            "/{}/{}".format(
                self.gateway.name,
                query_name,
            ),
            callback_group=MutuallyExclusiveCallbackGroup(),
        )
        if not client.wait_for_service(1.0):
            raise CrazyflieGatewayError(
                "{} failed, {} not available!".format(
                    query_name,
                    self.gateway.name,
                )
            )

        future = client.call_async(request)
        rclpy.spin_until_future_complete(self.node, future, timeout_sec=1.0)
        response = future.result()
        try:
            if not self.gateway.is_success(response):
                raise CrazyflieGatewayError(
                    "{} call to {} responded with false!".format(
                        query_name,
                        self.gateway.name,
                    )
                )
        except:
            raise CrazyflieGatewayError(
                "Gateway call failed due to a timeout in service call!"
            )

    def __create_webots_request(self, cf_id: int, initial_position: List[float]):
        request = WebotsCrazyflie.Request()
        request.id = cf_id
        (
            request.initial_position.x,
            request.initial_position.y,
            request.initial_position.z,
        ) = initial_position
        request.type.data = "default"
        return request

    def __create_hardware_request(
        self, cf_id: int, channel: int, initial_position: List[float]
    ):
        request = HardwareCrazyflie.Request()
        request.id = cf_id
        request.channel = channel
        (
            request.initial_position.x,
            request.initial_position.y,
            request.initial_position.z,
        ) = initial_position
        request.type.data = "default"
        return request
