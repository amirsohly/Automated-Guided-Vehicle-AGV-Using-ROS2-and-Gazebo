import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random

class AGVMonitor(Node):
    def __init__(self):
        super().__init__('agv_monitor_node')
        self.publisher_ = self.create_publisher(String, 'agv_status', 10)
        self.timer = self.create_timer(2.0, self.timer_callback)

    def timer_callback(self):
        battery = random.randint(20, 100)
        msg = String()
        msg.data = f'AGV_ID: 001 | Battery: {battery}% | Status: Moving'
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = AGVMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
