#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from datetime import datetime
import time
from nav_msgs.msg import Odometry
from src.smartwalker_pkg.src.custom_classes import csv_handler as ch
from custom_interfaces.srv import VelocityRegistration, CSVFileName

class VelocityData(Node):
    def __init__(self):
        super().__init__('vel_data')
        self.state = 0
        self.create = False
        self.record = False
        self.iter = 0
        self.realx, self.realy = [], []

        self.create_subscription(
            # Odometry,
            # topic='/ground_truth',
            Odometry, #PoseWithCovarianceStamped,
            topic= '/odometry/filtered_global', #/amcl_pose',
            callback=self.velocity_analyzer,
            qos_profile=10)
        self.csv_server = self.create_service(VelocityRegistration, 'vel_rec', self.get_record)

    def csv_response_callback(self, future):
        try:
            res = future.result()
            self.get_logger().info(f" Server response: {res.message}")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")
        finally:
            pass

    def get_record(self, req, res):
        res.message = "Informatiom recived."
        self.create = req.create
        self.record = req.record
        return res

    def velocity_analyzer(self, msg):
        self.robot_covx = msg.pose.covariance[0]
        self.robot_covy = msg.pose.covariance[7]
        self.robot_covt = msg.pose.covariance[35]
        match self.state:
            case 0:
                if self.create:
                    self.state = 1
            case 1:
                self.now = datetime.now()
                self.csv_file_name = f'TEST_COV_EKF_{self.iter}'
                self.get_logger().info(f"Initializing CSV file. All velocity data will be saved in velocity/{self.csv_file_name}")
                ch.create_csv_file(
                    name_file=self.csv_file_name,
                    dir="cov",
                    col1="Time",
                    col2="CovX",
                    col3="CovY",
                    col4="CovT",
                )
                self.state = 2

            case 2:
                if self.record:
                    self.state = 3
                    self.start_time = time.time()
            case 3:
                ch.save_to_csv_three_values(
                    name_file=self.csv_file_name,
                    dir="cov",
                    val1=self.robot_covx,
                    val2=self.robot_covy,
                    val3=self.robot_covt,
                    start_time=self.start_time
                )
                if not self.record:
                    self.get_logger().info("Sending velocity data")
                    self.state = 0
                    self.iter = self.iter +1


def main(args=None):
    rclpy.init(args=args)
    vel_node = VelocityData()
    try:
        rclpy.spin(vel_node)
    except KeyboardInterrupt:
        print('[INFO] Terminating velocity data node')
    finally:
        vel_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

