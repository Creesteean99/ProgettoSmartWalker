#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
from custom_interfaces.msg import Parameter
from custom_interfaces.srv import CSVFileName, VelocityRegistration
from src.smartwalker_pkg.src.custom_classes import csv_handler as ch
from datetime import datetime
from src.smartwalker_pkg.src.custom_classes import curve_manipolation as pl
from rclpy.qos import QoSProfile, DurabilityPolicy
import numpy as np
import time

class OdomSubscriber(Node):
    def __init__(self):
        super().__init__('odom_subscriber')
        self.dir = 'ekf'
        self.csv_file_name = None
        self.state = -1
        self.csv_client = self.create_client(CSVFileName, "csv_file")
        self.vel_rec_client = self.create_client(VelocityRegistration, "vel_rec")
        self.record = False
        self.guide_type = None
        self.num_points = 10000
        self.d_box = 0.15
        self.qos = QoSProfile(depth=1)
        self.qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
        self.iter = 0

        while not self.vel_rec_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                "Velocity registration service not available, waiting again...")
        self.vel_rec_req = VelocityRegistration.Request()

        self.parameter_subscription = self.create_subscription(
            Parameter,
            topic='/parameters_config',
            callback= self.get_config_parameters,
            qos_profile=self.qos
        )

        self.odom_sub = self.create_subscription(
            Odometry , #PoseWithCovarianceStamped #
            topic= '/odometry/filtered_global',  #'/amcl_pose',             # USATO FINO AD ORA AMCL_POSE
            callback= self.odom_handler,
            qos_profile=10
        )

    def send_vel_req(self, rec, crt):
        self.vel_rec_req.record = rec
        self.vel_rec_req.create = crt
        self.future = self.vel_rec_client.call_async(self.vel_rec_req)
        self.future.add_done_callback(self.vel_req_response_callback)

    def vel_req_response_callback(self, future):
        try:
            res = future.result()
            self.get_logger().info(f" Server response: {res.message}")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")
        finally:
            pass

    def is_inside(self, pos, reverse = False):
        point = np.array([self.gamma[:,0], self.gamma[:,-1]])
        t = np.array([self.t_i, self.t_f])
        n = np.array([self.n_i, self.n_f])
        dist = self.robot_pose - point[pos]  # Distanza robot- punto
        dist_n = dist @ n[pos]         # Proiezione lungo normale
        if reverse:
            dist_t = -dist @ t[pos]
        else:
            dist_t = dist @ t[pos]          # Proiezione lungo tangente
        return (0 <= dist_t <= self.d_box) and (-2*self.d_box <= dist_n <= 2*self.d_box)   # True solo se è interno all'area

    def get_config_parameters(self, config):
        self.guide_type = config.guide_type
        self.start_point = config.start_point
        self.end_point = config.end_point
        self.thickness = config.thickness
        self.record = config.record
        self.amplitude = config.amplitude
        self.gamma  = pl.parametric_guide(self.guide_type, self.start_point, self.end_point, self.amplitude, self.num_points)

        # Direzioni normali e tangenti per aree di start and stop
        vi = self.gamma[:,1] - self.gamma[:,0]
        vf = self.gamma[:,-1] - self.gamma[:,-2]
        Li = np.linalg.norm(vi)
        Lf = np.linalg.norm(vf)
        self.t_i = vi/Li
        self.t_f = vf/Lf
        self.n_i = np.array([-self.t_i[1], self.t_i[0]])
        self.n_f = np.array([-self.t_f[1], self.t_f[0]])

    # Sottoscrivendoci al topic di Odom, se il robot è circa in posizione di partenza, fai partire il salvataggio delle
    # posizioni su CSV.

    def odom_handler(self, odom_pose):
        self.robot_x = odom_pose.pose.pose.position.x
        self.robot_y = odom_pose.pose.pose.position.y
        self.robot_pose = np.array([self.robot_x, self.robot_y])
        if self.record is True:
            if self.guide_type is None:
                raise ValueError("Guide type not set.")
            match self.state:
                case -1:
                    self.get_logger().info("Waiting to allign with starter point...")
                    self.state = 0

                case 0:
                    if self.is_inside(0, True):
                        self.state = 1

                case 1:
                    self.send_vel_req(False, True)
                    self.now = datetime.now()
                    # self.csv_file_name = f'Test_{self.now:%d%m%y}_{self.now:%H-%M-%S}'
                    self.csv_file_name = f'TEST_LOC_EKF_{self.iter}'
                    self.get_logger().info(f"Initializing CSV file. All data will be saved.")
                    ch.create_csv_file(
                        name_file=self.csv_file_name,
                        dir= self.dir,
                        col1="Time",
                        col2="Position X",
                        col3="Position Y",
                    )
                    self.get_logger().info("Everything is set. Registration will be started once you pass starting point.")
                    self.state = 2

                case 2:
                    if self.is_inside(0, False) and self.guide_type != 1 \
                            or self.is_inside(0, False)and self.guide_type == 1:
                        self.state = 3
                        self.get_logger().info("Data registration started.")
                        self.start_time = time.time()
                        self.send_vel_req(True, False)

                case 3:
                    ch.save_to_csv_two_values(
                        name_file= self.csv_file_name,
                        dir=self.dir,
                        val1 = self.robot_x,
                        val2 = self.robot_y,
                        start_time = self.start_time
                    )
                    MAX_DISTANCE = 0.3
                    distances = np.linalg.norm(self.gamma - self.robot_pose.reshape(2, 1), axis=0)
                    if np.all(distances > MAX_DISTANCE):
                        self.get_logger().warning("Robot deviated too much from guide. Registration aborted.")
                        self.state = -1
                        self.send_vel_req(False, False)
                        return
                    if self.is_inside(1) and self.guide_type != 1 \
                            or self.is_inside(1) and self.guide_type == 1:
                        self.get_logger().info("Data registration ended.")
                        self.send_vel_req(False, False)
                        self.state= -1
                        self.iter = self.iter+1
        else:
            self.state = -1

def main(args=None):
    rclpy.init(args=args)
    rehab_test = OdomSubscriber()
    try:
        rclpy.spin(rehab_test)
    except KeyboardInterrupt:
        print("Terminating...")
    finally:
        rehab_test.destroy_node()

if __name__ == '__main__':
    main()