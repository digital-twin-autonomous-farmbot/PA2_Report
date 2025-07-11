from geometry_msgs.msg import Twist
from serial_motor_demo_msgs.msg import MotorCommand
import rclpy
from rclpy.node import Node

class CmdVelToMotorCommandNode(Node):
    def __init__(self):
        super().__init__('cmd_vel_to_motor_command')

        # Subscriber for /cmd_vel
        self.cmd_vel_subscriber = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10)

        # Publisher for /motor_command
        self.motor_command_publisher = self.create_publisher(
            MotorCommand,
            '/motor_command',
            10)

        self.get_logger().info("Node started: Relaying /cmd_vel to /motor_command")

    def cmd_vel_callback(self, twist_msg):
        # create MotorCommand message
        motor_command = MotorCommand()

        # convert Twist (linear.x, angular.z) to MotorCommand
        motor_command.is_pwm = True  # PWM-Modus activate
        motor_command.mot_1_req_rad_sec = twist_msg.linear.x * 255  
        motor_command.mot_2_req_rad_sec = twist_msg.angular.z * 255

        # Publish message
        self.motor_command_publisher.publish(motor_command)

        self.get_logger().info(f"Relayed: linear.x={twist_msg.linear.x}, angular.z={twist_msg.angular.z}")

def main(args=None):
    rclpy.init(args=args)
    node = CmdVelToMotorCommandNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
