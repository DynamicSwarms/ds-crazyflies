import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker
from collision_avoidance_interfaces.srv import CollisionAvoidance
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.client import Client
import math
import time


class CollisionAvoidanceNode(Node):
    def __init__(self):
        super().__init__("collision_avoidance_test")
        self.publisher_ = self.create_publisher(Marker, "visualization_marker", 10)
        self.timer = self.create_timer(
            0.1, self.update_position0, callback_group=MutuallyExclusiveCallbackGroup()
        )

        self.timer = self.create_timer(
            0.11, self.update_position1, callback_group=MutuallyExclusiveCallbackGroup()
        )

        self.coll_avoidance_client: Client = self.create_client(
            CollisionAvoidance,
            "collision_avoidance",
            callback_group=MutuallyExclusiveCallbackGroup(),
        )

        # Object positions and velocities
        # self.obj1_pos = [0.0, 0.0]
        # self.obj2_pos = [-0.1, 5.0]
        # self.obj1_vel = [0.0, 0.1]
        # self.obj2_vel = [0.0, -0.1]

        # self.obj1_pos = [-3.0, -3.0]  # Bottom-left moving up-right
        # self.obj2_pos = [3.1, 3.0]  # Top-right moving down-left
        # self.obj1_vel = [0.05, 0.05]
        # self.obj2_vel = [-0.05, -0.05]

        self.obj1_pos = [-2.0, 0.0]  # Moving straight along X-axis
        self.obj2_pos = [2.0, 2.0]  # Moving diagonally
        self.obj1_vel = [0.05, 0.0]  # Horizontal movement
        self.obj2_vel = [-0.05, -0.05]  # Diagonal movement

    def update_position0(self):
        self.get_logger().info("Update 1")

        pos = self.obj1_pos
        vel = self.obj1_vel

        target = self.calculate_target(pos, [pos[0] + vel[0], pos[1] + vel[1]], 0)
        self.obj1_pos = [target[0], target[1]]
        # Publish visualization markers
        self.publish_marker(self.obj1_pos, 0)

    def update_position1(self):
        self.get_logger().info("Update 2")
        pos = self.obj2_pos
        vel = self.obj2_vel

        target = self.calculate_target(pos, [pos[0] + vel[0], pos[1] + vel[1]], 1)
        self.get_logger().info(str(target))
        self.obj2_pos = [target[0], target[1]]
        self.publish_marker(self.obj2_pos, 1)

    def calculate_target(
        self, pos: list[float], target: list[float], id: int
    ) -> list[float]:
        req = CollisionAvoidance.Request()
        req.position.x = pos[0]
        req.position.y = pos[1]
        req.target.x = target[0]
        req.target.y = target[1]
        req.id = id

        resp: CollisionAvoidance.Response = self.coll_avoidance_client.call(req)
        return [resp.target.x, resp.target.y]

    def publish_marker(self, position, marker_id):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "objects"
        marker.id = marker_id
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position.x = position[0]
        marker.pose.position.y = position[1]
        marker.pose.position.z = 0.0
        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.2
        marker.color.a = 1.0
        marker.color.r = 1.0 if marker_id == 0 else 0.0
        marker.color.g = 0.0 if marker_id == 0 else 1.0
        marker.color.b = 0.0

        self.publisher_.publish(marker)


def main(args=None):
    rclpy.init(args=args)
    node = CollisionAvoidanceNode()
    rclpy.__executor = MultiThreadedExecutor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
