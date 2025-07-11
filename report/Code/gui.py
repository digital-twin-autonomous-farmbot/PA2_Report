import rclpy
from rclpy.node import Node
import time
from tkinter import *
import math

from serial_motor_demo_msgs.msg import MotorCommand
from serial_motor_demo_msgs.msg import MotorVels
from serial_motor_demo_msgs.msg import EncoderVals


class MotorGui(Node):

    def __init__(self):
        super().__init__('motor_gui')

        self.publisher = self.create_publisher(MotorCommand, 'motor_command', 10)

        self.speed_sub = self.create_subscription(
            MotorVels,
            'motor_vels',
            self.motor_vel_callback,
            10)

        self.encoder_sub = self.create_subscription(
            EncoderVals,
            'encoder_vals',
            self.encoder_val_callback,
            10)

        self.tk = Tk()
        self.tk.title("Serial Motor GUI")
        root = Frame(self.tk)
        root.pack(fill=BOTH, expand=True)

        Label(root, text="Serial Motor GUI").pack()

        m1_frame = Frame(root)
        m1_frame.pack(fill=X)
        Label(m1_frame, text="Motor 1").pack(side=LEFT)
        self.m1 = Scale(m1_frame, from_=-255, to=255, orient=HORIZONTAL)
        self.m1.pack(side=LEFT, fill=X, expand=True)

        m2_frame = Frame(root)
        m2_frame.pack(fill=X)
        Label(m2_frame, text="Motor 2").pack(side=LEFT)
        self.m2 = Scale(m2_frame, from_=-255, to=255, resolution=1, orient=HORIZONTAL)
        self.m2.pack(side=LEFT, fill=X, expand=True)

        motor_btns_frame = Frame(root)
        motor_btns_frame.pack()
        Button(motor_btns_frame, text='Send Once', command=self.send_motor_once).pack(side=LEFT)
        Button(motor_btns_frame, text='Stop Mot', command=self.stop_motors).pack(side=LEFT)

        enc_frame = Frame(root)
        enc_frame.pack(fill=X)

        self.enc_lbl = Label(enc_frame, text="Encoders: ")
        self.enc_lbl.pack(side=LEFT)
        self.mot_1_enc_lbl = Label(enc_frame, text="XXX")
        self.mot_1_enc_lbl.pack(side=LEFT)
        self.mot_2_enc_lbl = Label(enc_frame, text="XXX")
        self.mot_2_enc_lbl.pack(side=LEFT)

        speed_frame = Frame(root)
        speed_frame.pack(fill=X)

        self.spd_lbl = Label(enc_frame, text="Speed rev/s: ")
        self.spd_lbl.pack(side=LEFT)
        self.mot_1_spd_lbl = Label(enc_frame, text="XXX")
        self.mot_1_spd_lbl.pack(side=LEFT)
        self.mot_2_spd_lbl = Label(enc_frame, text="XXX")
        self.mot_2_spd_lbl.pack(side=LEFT)

    def send_motor_once(self):
        msg = MotorCommand()
        msg.is_pwm = True  # Always in PWM mode now
        msg.mot_1_req_rad_sec = float(self.m1.get())
        msg.mot_2_req_rad_sec = float(self.m2.get())
        self.publisher.publish(msg)

    def stop_motors(self):
        msg = MotorCommand()
        msg.is_pwm = True
        msg.mot_1_req_rad_sec = 0.0
        msg.mot_2_req_rad_sec = 0.0
        self.publisher.publish(msg)

    def motor_vel_callback(self, motor_vels):
        mot_1_spd_rev_sec = motor_vels.mot_1_rad_sec / (2 * math.pi)
        mot_2_spd_rev_sec = motor_vels.mot_2_rad_sec / (2 * math.pi)
        self.mot_1_spd_lbl.config(text=f"{mot_1_spd_rev_sec:.2f}")
        self.mot_2_spd_lbl.config(text=f"{mot_2_spd_rev_sec:.2f}")

    def encoder_val_callback(self, encoder_vals):
        self.mot_1_enc_lbl.config(text=f"{encoder_vals.mot_1_enc_val}")
        self.mot_2_enc_lbl.config(text=f"{encoder_vals.mot_2_enc_val}")

    def update(self):
        self.tk.update()


def main(args=None):
    
    rclpy.init(args=args)

    motor_gui = MotorGui()

    rate = motor_gui.create_rate(20)    
    while rclpy.ok():
        rclpy.spin_once(motor_gui)
        motor_gui.update()


    motor_gui.destroy_node()
    rclpy.shutdown()
