import rclpy
from rclpy.node import Node


from visualization_msgs.msg import MarkerArray, Marker
from geometry_msgs.msg import PoseArray, PoseStamped

from builtin_interfaces.msg import Duration

from crazyflie_interfaces_python.positions import CfPositionBuffer, CfPositionListener


class PositionVisualization(Node):
    def __init__(self):
        super().__init__("position_visualization")

        self.marker_pub = self.create_publisher(
            msg_type=MarkerArray, topic="cf_positions_marker", qos_profile=10
        )
        self.pose_array_pub = self.create_publisher(
            msg_type=PoseArray, topic="cf_positions_poses", qos_profile=10
        )

        decay_time = 1.0
        self.buffer = CfPositionBuffer(self, decay_time=decay_time)
        self.listener = CfPositionListener(self.buffer, self)

        self.create_timer(1.0 / 10.0, self.visualize_positions)

    def visualize_positions(self):
        positions = self.buffer.get_all_positions()

        msg_pose_array = PoseArray()
        msg_marker_array = MarkerArray()

        msg_pose_array.header.stamp = self.get_clock().now().to_msg()
        msg_pose_array.header.frame_id = "world"

        pose_stamped: PoseStamped
        for pose_stamped in positions:
            msg_pose_array.poses.append(pose_stamped.pose)

            marker = Marker()
            marker.header = msg_pose_array.header
            marker.type = Marker.TEXT_VIEW_FACING
            marker.lifetime = Duration(sec=1)
            marker.ns = pose_stamped.header.frame_id
            marker.scale.z = 0.1
            marker.text = pose_stamped.header.frame_id
            marker.pose = pose_stamped.pose
            color = (1.0, 1.0, 1.0, 1.0)
            (
                marker.color.r,
                marker.color.g,
                marker.color.b,
                marker.color.a,
            ) = color

            msg_marker_array.markers.append(marker)

        self.marker_pub.publish(msg_marker_array)
        self.pose_array_pub.publish(msg_pose_array)


def main():
    rclpy.init()
    vis_node = PositionVisualization()
    rclpy.spin(vis_node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
