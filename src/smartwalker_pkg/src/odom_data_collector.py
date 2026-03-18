#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
from custom_interfaces.msg import Parameter
from custom_interfaces.srv import CSVFileName, VelocityRegistration
from .custom_classes import csv_handler as ch
from datetime import datetime
from .custom_classes import curve_manipolation as pl
from rclpy.qos import QoSProfile, DurabilityPolicy
import numpy as np
import time

class OdomSubscriber(Node):
    def __init__(self):
        super().__init__('odom_subscriber')
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

        self.declare_parameter('localization_type', 'AMCL') # Default
        loc_type = self.get_parameter('localization_type').get_parameter_value().string_value
        if loc_type == 'EKF':
            topic_name = '/odometry/filtered_global'
            topic_type = Odometry
        else:
            topic_name = '/amcl_pose'
            topic_type = PoseWithCovarianceStamped

        while not self.csv_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("CSV file name service not available, waiting again...")
        self.csv_req = CSVFileName.Request()

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
            topic_type,
            topic= topic_name,
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
        # Creazione di un'area nel punto iniziale o finale della guida di per l'inizio e l'arresto della registrazione dati
        point = np.array([self.gamma[:,0], self.gamma[:,-1]])
        t = np.array([self.t_i, self.t_f])
        n = np.array([self.n_i, self.n_f])
        dist = self.robot_pose - point[pos]  # Distanza robot- punto. pos rappresenta 0 o 1 a seconda che sia il punto iniziale o finale
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

    # Se il robot è circa in posizione di partenza, fai partire il salvataggio delle posizioni su CSV.
    def send_csv_file_name(self, filename, directory):
        self.csv_req.filename = filename
        self.csv_req.directory = directory
        self.future = self.csv_client.call_async(self.csv_req)
        self.future.add_done_callback(self.csv_response_callback)

    def csv_response_callback(self, future):
        try:
            res = future.result()
            self.get_logger().info(f" Server response: {res.message}")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")
        finally:
            pass

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
                    # Arrivo nell'area precedente il punto di inizio
                    if self.is_inside(0, True):
                        self.state = 1

                case 1:
                    self.send_vel_req(False, True)
                    self.now = datetime.now()
                    self.csv_file_name = f'Test_{self.now:%d%m%y}_{self.now:%H-%M-%S}'
                    self.get_logger().info(f"Initializing CSV file. All data will be saved in odometry/{self.csv_file_name}")
                    ch.create_csv_file(
                        name_file=self.csv_file_name,
                        dir= "odometry",
                        col1="Time",
                        col2="Position X",
                        col3="Position Y",
                    )
                    self.get_logger().info("Everything is set. Registration will be started once you pass starting point.")
                    self.state = 2

                case 2:
                    # Se supero il putno di inizio
                    if self.is_inside(0, False):
                        self.state = 3
                        self.get_logger().info("Data registration started.")
                        self.start_time = time.time()
                        self.send_vel_req(True, False)

                case 3:
                    ch.save_to_csv_two_values(
                        name_file= self.csv_file_name,
                        dir="odometry",
                        val1 = self.robot_x,
                        val2 = self.robot_y,
                        start_time = self.start_time
                    )
                    # MAX_DISTANCE è una distanza massima che se viene superata fa considerare la prova nulla.
                    # POSSIBILE BUG: in questo caso, qualora risulti nulla, velocity_data potrebbe ugualmente mandare il csv
                    # ad elaborate_data, generando un comportamento sconosciuto del nodo.

                    MAX_DISTANCE = 0.3
                    distances = np.linalg.norm(self.gamma - self.robot_pose.reshape(2, 1), axis=0)
                    if np.all(distances > MAX_DISTANCE):
                        self.get_logger().warning("Robot deviated too much from guide. Registration aborted.")
                        self.state = -1
                        self.send_vel_req(False, False)
                        return
                    if self.is_inside(1, False):
                        self.send_csv_file_name(self.csv_file_name, "odometry")
                        self.get_logger().info("Data registration ended.")
                        self.send_vel_req(False, False)
                        self.state= -1
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