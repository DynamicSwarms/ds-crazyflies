import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

from .crazyflie_types import CrazyflieType

from crazyflie_webots_gateway_interfaces.srv import WebotsCrazyflie
from crazyflie_hardware_gateway_interfaces.srv import (
    AddCrazyflie as AddHardwareCrazyflie,
    RemoveCrazyflie as RemoveHardwareCrazyflie,
)

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
    add_service_type: Type
    remove_service_type: Type
    is_success: Callable[[Any], bool]
    request_msg: Callable[[Any], str]


class GatewayEndpoint:
    webots_gateway = gateway(
        name="crazyflie_webots_gateway",
        add="add_crazyflie",
        remove="remove_crazyflie",
        add_service_type=WebotsCrazyflie,
        remove_service_type=WebotsCrazyflie,
        is_success=lambda response: response.success,
        request_msg=lambda response: "See gateway for more information!",
    )
    hardware_gateway = gateway(
        name="crazyflie_hardware_gateway",
        add="add_crazyflie",
        remove="remove_crazyflie",
        add_service_type=AddHardwareCrazyflie,
        remove_service_type=RemoveHardwareCrazyflie,
        is_success=lambda response: response.success,
        request_msg=lambda response: response.msg,
    )

    def __init__(
        self,
        node: Node,
        cf_id: int,
        cf_channel: int,
        initial_position: List[float],
        crazyflie_type: CrazyflieType,
    ):
        self.node: Node = node

        self.add_request = None
        self.remove_request = None
        self.gateway = None
        if crazyflie_type == CrazyflieType.WEBOTS:
            self.add_request = self.__create_webots_request(cf_id, initial_position)
            self.remove_request = self.__create_webots_request(cf_id, initial_position)
            self.gateway = self.webots_gateway
        elif crazyflie_type == CrazyflieType.HARDWARE:
            self.add_request = self.__create_hardware_add_request(
                cf_id, cf_channel, initial_position
            )
            self.remove_request = self.__create_hardware_remove_request(
                cf_id, cf_channel
            )
            self.gateway = self.hardware_gateway

        if (
            self.add_request is None
            or self.remove_request is None
            or self.gateway is None
        ):
            raise CrazyflieGatewayError(
                "Opening connection failed. No gateway available for {}".format(
                    crazyflie_type.name
                )
            )

    def open(self):
        self.__query_gateway(GatewayQueryType.CREATE, self.add_request)

    def close(self):
        self.__query_gateway(GatewayQueryType.CLOSE, self.remove_request)

    def __query_gateway(self, query_type: GatewayQueryType, request):
        query_name = (
            self.gateway.add
            if query_type is GatewayQueryType.CREATE
            else self.gateway.remove
        )
        service_type = (
            self.gateway.add_service_type
            if query_type is GatewayQueryType.CREATE
            else self.gateway.remove_service_type
        )

        client = self.node.create_client(
            service_type,
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

        max_timeout: int = 15
        for _ in range(max_timeout):  # Wait 10 seconds at most
            rclpy.spin_until_future_complete(
                self.node, future, timeout_sec=1.0
            )  # Wait until crazyflie configuration is done
            response = future.result()
            if response is None:
                if not client.wait_for_service(0.1):
                    raise CrazyflieGatewayError(
                        "Tried {}, failed! {} was available but died during processing!".format(
                            query_name,
                            self.gateway.name,
                        )
                    )
                else:
                    continue
            elif not self.gateway.is_success(response):
                raise CrazyflieGatewayError(
                    "{} call to {} responded with False! {}.".format(
                        query_name,
                        self.gateway.name,
                        self.gateway.request_msg(response),
                    )
                )
            else:
                return  # Succesfully executed the query to gateway.

        raise CrazyflieGatewayError(
            f"Gateway call failed due to a timeout in service call! Failed after {max_timeout} seconds."
        )

    def __create_webots_request(self, cf_id: int, initial_position: List[float]):
        request = WebotsCrazyflie.Request()
        request.id = cf_id
        return request

    def __create_hardware_add_request(
        self, cf_id: int, channel: int, initial_position: List[float]
    ) -> AddHardwareCrazyflie.Request:
        request = AddHardwareCrazyflie.Request()
        request.id = cf_id
        request.channel = channel
        (
            request.initial_position.x,
            request.initial_position.y,
            request.initial_position.z,
        ) = initial_position
        request.type = "tracked"
        return request

    def __create_hardware_remove_request(
        self, cf_id: int, channel: int
    ) -> RemoveHardwareCrazyflie.Request:
        request = RemoveHardwareCrazyflie.Request()
        request.id = cf_id
        request.channel = channel
        return request
