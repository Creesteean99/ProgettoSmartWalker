#!/usr/bin/env python3

# Il seguente nodo sottoscrive al topic di odometria per salvare i dati di velocità. Nato principalmente per utilizzarlo con la
# localizzazione AMCL. Qualora si usasse la localizzazione con Robot_Localization, e quindi i filtri EKF, si può aggiungere
# a odom_data_collector il salvataggio di Twist, essendo la posa fornita dal localizzatore di tipo Odometry.
# NB: il comportamento del tipo Twist di Robot_Localization non è noto, potrebbe essere pieno di rumore e quindi necessita
# di filtraggio.

# L'action "VelocityRegistration" viene settata in odom_data_collector, e serve solo ad orchestrare quando registrare e quando no.
# Era per evitare un copia e incolla di odom_data_collector, sicuramente può essere fatto meglio.

# L'action "CSVFileName" è utilizzata da elaborate_data per andare a ricercare i CSV per il post processing.

import rclpy
from rclpy.node import Node
from datetime import datetime
import time
from nav_msgs.msg import Odometry
from .custom_classes import csv_handler as ch
from custom_interfaces.srv import VelocityRegistration, CSVFileName

class VelocityData(Node):
    def __init__(self):
        super().__init__('vel_data')
        self.state = 0
        self.create = False
        self.record = False
        self.create_subscription(
            msg_type=Odometry,
            topic= "/odom",
            callback=self.velocity_analyzer,
            qos_profile=10)
        self.csv_server = self.create_service(VelocityRegistration, 'vel_rec', self.get_record)
        self.csv_client = self.create_client(CSVFileName, "csv_file")

        while not self.csv_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("CSV file name service not available, waiting again...")
        self.csv_req = CSVFileName.Request()

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

    def get_record(self, req, res):
        res.message = "Informatiom recived."
        self.create = req.create
        self.record = req.record
        return res

    def velocity_analyzer(self, msg):
        self.x = msg.twist.twist.linear.x
        match self.state:
            case 0:
                if self.create:
                    self.state = 1
            case 1:
                self.now = datetime.now()
                self.csv_file_name = f'Test_{self.now:%d%m%y}_{self.now:%H-%M-%S}'
                self.get_logger().info(f"Initializing CSV file. All velocity data will be saved in velocity/{self.csv_file_name}")
                ch.create_csv_file(
                    name_file=self.csv_file_name,
                    dir="velocity",
                    col1="Time",
                    col2="X",
                )
                self.state = 2

            case 2:
                if self.record:
                    self.state = 3
                    self.start_time = time.time()
            case 3:
                ch.save_to_csv_one_value(
                    name_file=self.csv_file_name,
                    dir="velocity",
                    val1=self.x,
                    start_time=self.start_time
                )
                if not self.record:
                    self.get_logger().info("Sending velocity data")
                    self.send_csv_file_name(self.csv_file_name, "velocity")
                    self.state = 0


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

