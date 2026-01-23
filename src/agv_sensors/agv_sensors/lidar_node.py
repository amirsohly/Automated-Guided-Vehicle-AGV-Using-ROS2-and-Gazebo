import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math

class LidarNode(Node):
    def __init__(self):
        super().__init__('lidar_node')
        self.publisher_ = self.create_publisher(LaserScan, 'scan', 10)
        self.timer = self.create_timer(0.5, self.publish_scan)

    def publish_scan(self):
        scan = LaserScan()
        scan.header.frame_id = 'laser_link'
        scan.angle_min = -math.pi / 2
        scan.angle_max = math.pi / 2
        scan.angle_increment = math.pi / 180
        scan.range_min = 0.2
        scan.range_max = 5.0
        scan.ranges = [2.0] * int((scan.angle_max - scan.angle_min) / scan.angle_increment)
        self.publisher_.publish(scan)

def main(args=None):
    rclpy.init(args=args)
    node = LidarNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

