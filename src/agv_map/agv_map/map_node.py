import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid

class StaticMap(Node):
    def __init__(self):
        super().__init__('static_map')
        self.pub = self.create_publisher(OccupancyGrid, '/map', 1)
        self.timer = self.create_timer(1.0, self.publish_map)

    def publish_map(self):
        msg = OccupancyGrid()
        msg.info.resolution = 0.5
        msg.info.width = 20
        msg.info.height = 20
        msg.data = [0] * (20 * 20)
        self.pub.publish(msg)

def main():
    rclpy.init()
    node = StaticMap()
    rclpy.spin(node)
