#!/usr/bin/env python3

# Questo nodo risulta utile da utilizzare in simulato per non dover andare ogni volta a fornire "2D Pose Estimate" da Rviz
# ogni volta che parte la simulazione.
# ATTENZIONE: modificare da qui la posizione NON modificherà anche la posizione di spawn del turtlebot3 all'interno di gazebo,
# questo viene fatto nel file di lancio gazebo_simulation.launch.py

import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseWithCovariance
from .custom_classes.parameters import HOME

class InitialPosePublisher(Node):
    def __init__(self):
        super().__init__('initial_pose_publisher')

        self.publisher_ = self.create_publisher(
            PoseWithCovarianceStamped,
            '/initialpose',
            10
        )

    def publish_initial_pose(self):
        msg = PoseWithCovarianceStamped()
        #
        # Header
        msg.header.frame_id = "map"

        home_pose = PoseWithCovariance()
        home_pose.pose = HOME
        home_pose.covariance = [0.0]*36
        msg.pose = home_pose
        self.publisher_.publish(msg)

class AMCLChecker(Node):
    def __init__(self):
        super().__init__('AMCLChecker')
        self.pose_recived = False
        self.create_subscription(PoseWithCovarianceStamped, "/amcl_pose", self.check_amcl_initialization, 10)

    def check_amcl_initialization(self, pos):
        amcl_x = pos.pose.pose.position.x
        amcl_y = pos.pose.pose.position.y

        amcl_quat = (
            pos.pose.pose.orientation.x,
            pos.pose.pose.orientation.y,
            pos.pose.pose.orientation.z,
            pos.pose.pose.orientation.w
        )
        if abs(amcl_x - HOME.position.x) < 0.05 and abs(amcl_y - HOME.position.y) < 0.05 and abs(
                amcl_quat[2] - HOME.orientation.z) < 0.05:
            self.get_logger().info("AMCL inizializzato.")
            self.pose_recived = True




def main(args=None):
    rclpy.init(args=args)
    initialPosePub = InitialPosePublisher()
    amclChecker = AMCLChecker()

    while rclpy.ok() and not amclChecker.pose_recived:
        initialPosePub.publish_initial_pose()
        rclpy.spin_once(initialPosePub, timeout_sec=0.1)
        rclpy.spin_once(amclChecker, timeout_sec=0.1)
        time.sleep(0.1)

    initialPosePub.destroy_node()
    amclChecker.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
