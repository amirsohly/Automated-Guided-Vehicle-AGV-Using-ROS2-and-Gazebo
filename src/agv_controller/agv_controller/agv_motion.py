import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from tf2_ros import TransformBroadcaster
import math
import time

class AGVMotion(Node):
    def __init__(self):
        super().__init__('agv_motion')

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

        self.br = TransformBroadcaster(self)

        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0

        self.cmd = Twist()
        self.last_time = time.time()

        self.timer = self.create_timer(0.05, self.update)
        self.get_logger().info("AGV motion node started")

    def cmd_callback(self, msg):
        self.cmd = msg

    def update(self):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        v = self.cmd.linear.x
        w = self.cmd.angular.z

        self.x += v * math.cos(self.yaw) * dt
        self.y += v * math.sin(self.yaw) * dt
        self.yaw += w * dt

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'map'
        t.child_frame_id = 'base_link'

        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0

        t.transform.rotation.z = math.sin(self.yaw / 2.0)
        t.transform.rotation.w = math.cos(self.yaw / 2.0)

        self.br.sendTransform(t)

def main():
    rclpy.init()
    node = AGVMotion()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
