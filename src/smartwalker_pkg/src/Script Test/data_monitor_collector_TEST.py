#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import time
from nav_msgs.msg import Odometry,Path
from geometry_msgs.msg import PoseWithCovarianceStamped
from src.smartwalker_pkg.src.custom_classes import csv_handler as ch
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus
from src.smartwalker_pkg.src.custom_classes.parameters import HOME, BED, COUCH, TOILETTE
from custom_interfaces.msg import Parameter
from rclpy.qos import QoSProfile, DurabilityPolicy
import matplotlib.pyplot as plt
import numpy as np
import os

class DataMonitor(Node):
    def __init__(self):
        super().__init__('data_monitor')
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        while not self._action_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().info("Navigate_to_Pose server not available, waiting again...")
        self.start_time = time.time()
        self.flag = False
        # self.path_names = ['S-L', 'L-B', 'B-D', 'D-S']
        self.is_testing = True
        self.current_goal_handle = None
        self.FIRST_MESSAGE = True
        self.loop = 0
        self.i = 0
        self.path_length = []
        self.path = [BED, TOILETTE, COUCH, HOME]
        self.odom = []
        self.plan = []
        self.t_pos = []
        self.t_grd = []
        self.robot_velx = []
        self.robot_vely = []
        self.realx = []
        self.realy = []
        self.robotx = []
        self.roboty = []
        self.robot_covx = []
        self.robot_covy = []
        self.robot_covt = []
        self.fig,self.ax = plt.subplots()
        self.ax.grid(True)
        self.qos = QoSProfile(depth=1)
        self.qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
        # PER LUNGHEZZA DEL PATH COMPILATO
        self.plan_subscriber = self.create_subscription(
            Path,
            topic='/plan',
            callback=self.update_plan,
            qos_profile=5
        )
        # PER TEMPO
        self.odom_subscriber = self.create_subscription(
            Odometry,
            topic='/odometry_filtered',
            callback=self.get_odom,
            qos_profile=10
        )
        # GROUND TRUTH
        self.realpose_subscriber = self.create_subscription(
            Odometry,
            topic='/ground_truth',
            callback=self.get_groundtruth,
            qos_profile=10
        )
        # # SISTEMA DI LOCALIZZAZIONE
        self.robotpose_subscriber = self.create_subscription(
            Odometry, #PoseWithCovarianceStamped,
            topic= '/odometry/filtered_global', #/amcl_pose',
            callback=self.get_realpose,
            qos_profile=10
        )

        # self.parameter_subscription = self.create_subscription(
        #     Parameter,
        #     topic='/parameters_config',
        #     callback= self.get_config_parameters,
        #     qos_profile=self.qos
        # )

        self.move_to_milestone()

    # def get_config_parameters(self, config):
    #     self.record = config.record
    #     self.move_to_milestone()

    def update_plan(self, msg):
        if self.FIRST_MESSAGE:
            self.plan = [[p.pose.position.x, p.pose.position.y] for p in msg.poses]
            self.FIRST_MESSAGE = False

    def get_odom(self, msg):
        if self.is_testing:
            self.robot_velx.append(msg.twist.twist.linear.x)
            self.robot_vely.append(msg.twist.twist.linear.y)
            self.t_pos.append(self.get_clock().now())

    def get_groundtruth(self, msg):
        if self.is_testing:
            self.realx.append(msg.pose.pose.position.x)
            self.realy.append(msg.pose.pose.position.y)
            self.t_grd.append(self.get_clock().now())
    #
    def get_realpose(self, msg):
        if self.is_testing:
            self.robotx.append(msg.pose.pose.position.x)
            self.roboty.append(msg.pose.pose.position.y)
            self.robot_covx.append(msg.pose.covariance[0])
            self.robot_covy.append(msg.pose.covariance[7])
            self.robot_covt.append(msg.pose.covariance[35])

    def send_goal(self, posa):
        goal = NavigateToPose.Goal()
        goal.pose.header.frame_id = "map"
        goal.pose.pose = posa
        self._action_client.wait_for_server()
        self._future_goal = self._action_client.send_goal_async(goal)  # , feedback_callback=self.feedback_callback)
        self._future_goal.add_done_callback(self.goal_callback)

    def goal_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info("Goal Rifiutato!")
            return
        self.get_logger().info("Gaol accettato!")
        self.get_result = goal_handle.get_result_async()
        self.get_result.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.is_testing = False
            self.process_data()
            

    def move_to_milestone(self):
        # if self.record:
            self.realx,self.realy,self.roboty,self.robotx = [],[],[],[]
            self.FIRST_MESSAGE = True
            self.is_testing = True
            # self.flag = True
        # else:
        #     self.is_testing = False
            # if self.flag:
                # self.process_data()
            self.send_goal(self.path[self.i])

    def process_data(self):
        # self.t_pos = np.array(self.t_pos)
        self.realx = np.array(self.realx)
        self.realy = np.array(self.realy)
        self.robotx,self.roboty = np.array(self.robotx), np.array(self.roboty) #ch.read_from_csv_two_values('TEST_LOC_AMCL_1','odometry')
        if self.i == 0:
            self.ax.plot(self.realx, self.realy,color='darkblue',linewidth=2,label='Posizione Reale')
            self.ax.plot(self.robotx, self.roboty,color='coral',linewidth=2,label='Localizzazione EKF')
        else:
            self.ax.plot(self.realx, self.realy, color='darkblue', linewidth=2)
            self.ax.plot(self.robotx, self.roboty, color='coral', linewidth=2)
        self.ax.xaxis.set_label_text("Posizione X")
        self.ax.yaxis.set_label_text("Posizione Y")
        self.i = self.i+1
        if self.i < 4:
            self.move_to_milestone()
        else:
            self.ax.text(HOME.position.x, HOME.position.y - 0.05, 'STAZIONE', fontsize=8, ha='center', va='top')
            self.ax.text(BED.position.x, BED.position.y - 0.05, 'LETTO', fontsize=8, ha='center', va='top')
            self.ax.text(TOILETTE.position.x, TOILETTE.position.y - 0.05, 'BAGNO', fontsize=8, ha='center', va='top')
            self.ax.text(COUCH.position.x, COUCH.position.y - 0.05, 'DIVANO', fontsize=8, ha='center', va='top')
            self.ax.plot(HOME.position.x, HOME.position.y, marker='*', color='black')
            self.ax.plot(BED.position.x, BED.position.y, marker='*', color='black')
            self.ax.plot(TOILETTE.position.x, TOILETTE.position.y, marker='*', color='black')
            self.ax.plot(COUCH.position.x, COUCH.position.y, marker='*', color='black')
            self.ax.legend()
            # output_dir = os.path.expanduser("~/tesi/src/smartwalker_pkg/plots/GTvsRP")
            # filename = "test_EKF.png"
            # path = os.path.join(output_dir, filename)
            # plt.savefig(path, dpi=150)
            plt.show()
            plt.close()
            rclpy.shutdown()


    def get_file_gtvsrp(self):
        ch.create_csv_file(f'test{self.i}_GT','ekf','t','x','y')
        ch.create_csv_file(f'test{self.i}_RP','ekf','t','x','y')
        for k in range (len(self.realx)): ch.save_to_csv_two_values(f'test{self.i}_GT','ekf',self.realx[k],self.realy[k], self.start_time)
        for k in range (len(self.robotx)): ch.save_to_csv_two_values(f'test{self.i}_RP','ekf',self.robotx[k],self.roboty[k], self.start_time)
        self. fig, self.ax = plt.subplots()
        self.ax.plot(self.realx, self.realy,linewidth=2, color='darkblue', label='Posizione Reale')
        self.ax.plot(self.robotx, self.roboty,linewidth=2, color='coral', label='Posizione localizzats')
        plt.grid()
        self.realx,self.realy,self.robotx,self.roboty  = [],[],[],[]
        output_dir = os.path.expanduser("~/tesi/src/smartwalker_pkg/plots/EKF - GT vs RP")
        filename = f"test{self.i}.png"
        path = os.path.join(output_dir, filename)
        plt.savefig(path, dpi=150)
        plt.close()
        self.i = self.i + 1
        if self.i > 9:
            rclpy.shutdown()

    def get_path_length(self):
        self.get_logger().info(f'Lunghezza ground truth: {len(self.realx)}\n Lunghezza robot: {len(self.roboty)}')
        self.plan = np.array(self.plan)
        current_path = np.sum(np.sqrt((self.plan[1:, 0] - self.plan[0:-1, 0]) ** 2 + (self.plan[1:, 1] - self.plan[0:-1, 1]) ** 2))
        for k in range(len(self.plan)): ch.save_to_csv_two_values(self.namefile, 'planners', self.plan[k, 0],self.plan[k, 1], self.start_time)
        self.computing_time = (self.stop - self.start).nanoseconds / 1e6
        self.get_logger().info(f'Computing Time: {self.computing_time}')
        self.path_length.append(current_path)
        self.i=self.i+1
        if self.i < 4:
            self.move_to_milestone()
        else:
            self.path_length = np.sum(self.path_length)
            self.get_logger().info(f'Path length THETAS: {self.path_length}')
            self.realx=np.array(self.realx)
            self.realy=np.array(self.realy)
            rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    dm = DataMonitor()
    try:
        rclpy.spin(dm)
    except KeyboardInterrupt:
        rclpy.shutdown()
        pass
    finally:
        dm.destroy_node()

if __name__ == '__main__':
    main()