import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray


class MergeArraysNode(Node):
    def __init__(self):
        super().__init__('merge_arrays_node')

        # Subscribers
        self.subscribe_to_input_1 = self.create_subscription(
            Int32MultiArray,
            '/input/array1',
            self.array_1_callback,
            10
        )

        self.subscribe_to_input_2 = self.create_subscription(
            Int32MultiArray,
            '/input/array2',
            self.array_2_callback,
            10
        )

        # Publisher
        self.publisher = self.create_publisher(Int32MultiArray, '/output/array', 10)

        # For storing input arrays
        self.array_1 = []
        self.array_2 = []

    # Receive from /input/array1
    def array_1_callback(self, received_message: Int32MultiArray):
        self.array_1 = list(received_message.data)
        self.publish_merged()

    # Receive from /input/array2
    def array_2_callback(self, received_message: Int32MultiArray):
        self.array_2 = list(received_message.data)
        self.publish_merged()

    # Output merged and sorted array to /output
    def publish_merged(self):
        if self.array_1 and self.array_2:
            output_message = Int32MultiArray()
            output_message.data = sorted(self.array_1 + self.array_2)
            self.publisher.publish(output_message)


def main(args=None):
    rclpy.init(args=args)
    node = MergeArraysNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
