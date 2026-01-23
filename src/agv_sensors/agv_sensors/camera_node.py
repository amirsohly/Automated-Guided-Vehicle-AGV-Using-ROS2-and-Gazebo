import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np

class FakeCamera(Node):
    def __init__(self):
        super().__init__('fake_camera')
        self.pub = self.create_publisher(Image, '/camera/image', 10)
        self.timer = self.create_timer(0.1, self.publish_image)

    def publish_image(self):
        img = Image()
        img.header.frame_id = 'camera_link'
        img.height = 240
        img.width = 320
        img.encoding = 'rgb8'
        img.data = (np.zeros((240,320,3), dtype=np.uint8)).tobytes()
        self.pub.publish(img)

def main():
    rclpy.init()
    node = FakeCamera()
    rclpy.spin(node)
