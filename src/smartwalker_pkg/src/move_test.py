#!/usr/bin/env python3

# Primissimo script creato per comprendere il funzionamento dei future e dei Ros Action Server.
# Ha rappresentato poi lo script di funzionamento per il movimento autonomo da pannello.

import rclpy
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus
from .custom_classes.parameters import HOME, BED, COUCH, TOILETTE
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from tf_transformations import quaternion_from_euler
import math

class MovementTest(Node):

    def __init__(self):
        super().__init__('movement_test_client')
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.home, self.bed, self.couch, self.toilette = HOME, BED, COUCH, TOILETTE

    def start(self):
        self.get_logger().info('Nodo di movimentazione attivato. Premere Ctrl+C per terminarlo.')
        while KeyboardInterrupt:
            self.get_method()

    def get_method(self):
        method = int(input('Inserisci \n\t1: se vuoi muoverti tramite coordinate, \n\t2: tramite punti di riferimento.\n\n\tSelezionando: '))
        match method:
            case 1:
                self.get_coordinates()
            case 2:
                self.move_to_milestone()
            case _:
                self.get_logger().info("Errore nell'inserimento valore, riprovare")
                self.get_method()

    def move_to_milestone(self):
        milestone = int(input('[INFO] Seleziona il riferimento da raggiungere:\n\t(1) Letto\n\t(2) Bagno\n\t(3) Divano\n\t(4) Stazione di ricarica.\n\n\tSelezionando: '))
        match milestone:
            case 1:
                self.send_goal(self.bed)
            case 2:
                self.send_goal(self.toilette)
            case 3:
                self.send_goal(self.couch)
            case 4:
                self.send_goal(self.home)
            case _:
                self.get_logger().info("Errore nell'inserimento valore, riprovare")
                self.get_to_milestone()

    def get_to_milestone(self):
        self.move_to_milestone()

    def get_coordinates(self):                                                                                          # Permette di ottenere le coordinate da terminale.
        x = float(input("[OP] Inserisci la coordinata X: "))
        y = float(input("[OP] Inserisci la coordinata Y: "))
        theta = float(input("[OP] Inserisci l'angolo: "))

        q = quaternion_from_euler(0,0,math.radians(theta))
        posa = PoseStamped()
        posa.header.frame_id = "map"
        posa.header.stamp = self.get_clock().now().to_msg()

        posa.pose.position.x = x
        posa.pose.position.y = y
        posa.pose.position.z = 0.0

        posa.pose.orientation.x = q[0]
        posa.pose.orientation.y = q[1]
        posa.pose.orientation.z = q[2]
        posa.pose.orientation.w = q[3]

        self.send_goal(posa)

    def send_goal(self, posa):
        goal = NavigateToPose.Goal()
        goal.pose = posa                                                                                                # NOTA BENE: NavigateToPose è un action alla directory /opt/ros/humble/share/nav2_msgs/action
                                                                                                                        # da definizione, goal.pose è di timpo PoseStamped. all'interno quindi vi sarà .pose.position e .pose.orientation

        self._action_client.wait_for_server()
        self._future_goal = self._action_client.send_goal_async(goal)#, feedback_callback=self.feedback_callback)
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
        if status == GoalStatus.STATUS_ABORTED:
            self.get_logger().info("Goal Aborted. Can't reach the target position.")
            rclpy.shutdown()
            return
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().info("Gaol cancelled.")
            rclpy.shutdown()
            return
        elif status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("Goal Reached.")
            rclpy.shutdown()
            return
        
def main(args = None):
    rclpy.init(args=args)
    test_node = MovementTest()
    try:
        test_node.start()
        rclpy.spin(test_node)
    except KeyboardInterrupt:
        print("\n[INFO] Nodo arrestato. Shutdown in corso!")
    finally:
        test_node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
        print("[INFO] Shutdown eseguito correttamente!")
            
if __name__ == "__main__":
    main()