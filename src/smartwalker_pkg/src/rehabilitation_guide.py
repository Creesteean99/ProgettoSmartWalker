#!/usr/bin/env python3

# Questo nodo semplicemente prende i dati di configurazione della guida e crea un topic di tipo Marker per
# visualizzare la guida di riabilitazione su Rviz

import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from std_msgs.msg import ColorRGBA
from rclpy.qos import QoSProfile, DurabilityPolicy
from .custom_classes import curve_manipolation as pl
from custom_interfaces.msg import Parameter
from geometry_msgs.msg import Point

class CreateGuide(Node):
    def __init__(self):
        super().__init__('guide_creator')
        self.qos = QoSProfile(depth=1)
        self.qos.durability = DurabilityPolicy.TRANSIENT_LOCAL

        self.guide_pub=self.create_publisher(
            msg_type=Marker,
            topic="/rehab_guide",
            qos_profile=self.qos)
        self.guide_message = Marker()
        self.num = 10000

        self.parameter_subscription = self.create_subscription(
            Parameter,
            topic='/parameters_config',
            callback=self.get_config_parameters,
            qos_profile=self.qos
        )
        self.guide_message = Marker()
        self.num = 10000

    def get_config_parameters(self, config):
        self.guide_type = config.guide_type
        self.start_point = config.start_point
        self.end_point = config.end_point
        self.thickness = config.thickness
        self.amplitude = config.amplitude
        if -1 < self.guide_type < 4:
            self.generate_guide_message()
        else:
            self.get_logger().warning("Guide not selected! Please select a guide type.")

    def generate_guide_message(self):
        self.curve = pl.parametric_guide(self.guide_type, self.start_point, self.end_point, self.amplitude, self.num)
        self.guide_points = tuple(Point(x=float(self.curve[0, i]),
                                        y=float(self.curve[1, i]),
                                        z=0.0)
                                  for i in range(self.curve.shape[1]))
        self.guide_message.header.frame_id = "map"
        self.guide_message.header.stamp = self.get_clock().now().to_msg()
        self.guide_message.ns = "rehab_guide"
        self.guide_message.id = 1
        self.guide_message.type = Marker.LINE_STRIP
        self.guide_message.action = Marker.ADD
        self.guide_message.points = self.guide_points
        self.guide_message.color = ColorRGBA(
            r=1.0,
            g=0.0,
            b=0.0,
            a=1.0)
        self.guide_message.scale.x = self.thickness
        self.publish_guide()

    def publish_guide(self):
        self.guide_pub.publish(self.guide_message)
        self.get_logger().info("Guide created")

    def return_guide_type(self):
        return self.guide_type

def main(args=None):
    rclpy.init(args=args)
    guide_node = CreateGuide()
    try:
        rclpy.spin(guide_node)
    except KeyboardInterrupt:
        print("Terminating...")
    finally:
        guide_node.destroy_node()


if __name__ == '__main__':
    main()