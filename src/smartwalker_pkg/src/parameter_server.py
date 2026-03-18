#!/usr/bin/env python3

# A riga 440 circa c'è implementazione di codice per la movimentazione. Sembra un muro invalicabile questo script, ma è banalissimo
# è solo la creazione della GUI.


import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from rclpy.qos import QoSProfile, DurabilityPolicy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped
from .custom_classes.parameters import START_POINT, END_POINT,THICKNESS, HOME, BED, COUCH, TOILETTE
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import Point
from custom_interfaces.msg import Parameter
from .custom_classes import csv_handler as ch
import threading
import queue
#-----------------------------------------------------------------------------------------------------------------------
#                                                 GUI
#                                           IMPLEMENTATION
#-----------------------------------------------------------------------------------------------------------------------

class ParameterServer(Node):
    def __init__(self):
        super().__init__('parameter_server')

        # QoS TRANSIENT_LOCAL: nuovo subscriber riceve l'ultimo messaggio
        self.qos = QoSProfile(depth=1)
        self.qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
        self.guide_type = 0
        self.start_point = [START_POINT.x, START_POINT.y]
        self.end_point = [END_POINT.x, END_POINT.y]
        self.thickness = THICKNESS
        self.amplitude = 0.5
        self.case = -1
        self.pose = [HOME, BED, COUCH, TOILETTE]
        self.pose_labels = ['Home Station', 'Bed', 'Couch', 'Toilette']
        self.ros_queue = queue.Queue()
        self.create_timer(0.1, self.process_queue)

        self.declare_parameter('localization_type', 'AMCL') # Default
        loc_type = self.get_parameter('localization_type').get_parameter_value().string_value
        if loc_type == 'EKF':
            topic_name = '/odometry/filtered_global'
            topic_type = Odometry
        else:
            topic_name = '/amcl_pose'
            topic_type = PoseWithCovarianceStamped

        # Publisher
        self.parameter_publisher = self.create_publisher(
            msg_type=Parameter,
            topic='parameters_config',
            qos_profile=self.qos
        )
        # Client per il goal in navigazione
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        while not self._action_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().info("CSV file name service not available, waiting again...")
        self.current_goal_handle = None
        self.home, self.bed, self.couch, self.toilette = HOME, BED, COUCH, TOILETTE

        # Subscriber
        self.pose_subscriber = self.create_subscription(
            topic_type,
            topic=topic_name,
            callback=self.pose_handler,
            qos_profile=10
        )
        self.initializeGUI()

    def pose_handler(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        self.orientation = msg.pose.pose.orientation
        match self.case:
            case -1:
                pass
            case 0: # Set Starter point
                self.start_point = [self.x, self.y]
                self.case = -1
            case 1: # Set End Point
                self.end_point = [self.x, self.y]
                self.case = -1
            case 2: # State Machine per traiettoria custom
                ch.create_csv_file(
                    name_file="custom",
                    dir= "",
                    col1="Time",
                    col2="Position X",
                    col3="Position Y",
                )
                self.case = 100

            case 4: # salvo il punto finale
                self.end_point = [self.x, self.y]
                self.case = -1
            case 100: # Salvo posizione iniziale e salvo
                self.start_point = [self.x, self.y]
                ch.save_to_csv_two_values(
                    name_file= "custom",
                    dir="",
                    val1 = self.x,
                    val2 = self.y,
                    start_time = 0
                )
                self.case = 101
            case 101: # Salvo solo le coordinate
                ch.save_to_csv_two_values(
                    name_file="custom",
                    dir="",
                    val1=self.x,
                    val2=self.y,
                    start_time=0
                )

    def update_parameters(self):
        if self.val_x_sp.get():
            self.start_point[0] = float(self.val_x_sp.get())
        if self.val_y_sp.get() != "":
            self.start_point[1] = float(self.val_y_sp.get())
        if self.val_x_ep.get() != "":
            self.end_point[0] = float(self.val_x_ep.get())
        if self.val_y_ep.get() != "":
            self.end_point[1] = float(self.val_y_ep.get())
        if self.val_thick.get() != "":
            self.thickness = float(self.val_thick.get())
        if self.val_amp.get() != "":
            self.amplitude = float(self.val_amp.get())

        msg = Parameter(guide_type=self.guide_type,
                        start_point=Point(x=self.start_point[0],
                                          y=self.start_point[1],
                                          z=0.0),
                        end_point=Point(x=self.end_point[0],
                                        y=self.end_point[1],
                                        z=0.0),
                        thickness=self.thickness,
                        amplitude=self.amplitude,
                        record= is_on)
        self.parameter_publisher.publish(msg)

    def initializeGUI(self):
        import tkinter as tk

        # ---------------------------------------------
        #               PARAMETERS
        #                   &
        #             BUTTON FUCTIONS
        # ---------------------------------------------

        BTN_WIDTH = 10
        BTN_GUIDE_TXT = ["Straight line", "Circonference", "Onduline line", "Manual guide"]
        global is_on
        is_on = False

        def pose_cases(num):
            self.case = num

        def new_window():
            global label
            new_w = tk.Toplevel(self.window)
            start_button = tk.Button(new_w,
                                     text= "Start Record",
                                     command= lambda i=2: pose_cases(i),
                                     bg="#B2DFDB",
                                     fg="#263238",
                                     bd=2,
                                     relief="solid",
                                     font=("Helvetica", 15, "italic", "bold"),)
            start_button.grid(row=0, column=0, padx=10, pady=10)
            end_button = tk.Button(new_w,
                                     text= "End Record",
                                     command= lambda i=4: pose_cases(i),
                                     bg="#B2DFDB",
                                     fg="#263238",
                                     bd=2,
                                     relief="solid",
                                     font=("Helvetica", 15, "italic", "bold"),)
            end_button.grid(row=0, column=1, padx=10, pady=10)
            label = tk.Label(new_w,text="Press 'start record' and move the robot. Once you're done, click on 'end record' and then update the parameters")
            label.grid(row=1, column=0, padx=10, pady=10)

        def set_guide_type(num):
            self.guide_type = num
            if num == 3:
                new_window()

        def switch():
            global is_on
            match is_on:
                case False:
                    is_on = True
                    self.on_button.config(image=self.on_registration)
                case True:
                    is_on = False
                    self.on_button.config(image=self.off_registration)

        # ---------------------------------------------
        #                   WINDOW
        # ---------------------------------------------
        self.window = tk.Tk()
        self.window.geometry("1400x1000")
        self.window.title("GUI Turtlebot3")
        self.window.resizable(True, False)
        self.window.minsize(width=1100, height=900)
        self.window.configure(background="white")
        self.window.grid_rowconfigure(0, weight=0)
        self.window.grid_rowconfigure(1, weight=1)  # Allarga completamente la riga 1
        self.window.grid_columnconfigure(0, weight=1)  # Allarga completamente la col 1

        # ---------------------------------------------
        #                   HEADER
        # ---------------------------------------------

        self.header_mainframe = tk.Frame(self.window, bg="#B0BEC5")
        self.header_mainframe.grid(row=0, column=0, sticky="nsew")
        self.header_mainframe.grid_columnconfigure(0, weight=1)
        self.header_mainframe.grid_rowconfigure(0, weight=1)

        self.header_frame = tk.Frame(self.header_mainframe, bg="#1B9AAA", padx=10, pady=10, bd=2, relief="solid")
        self.header_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_rowconfigure(0, weight=1)

        self.header_label = tk.Label(
            self.header_frame,
            text="Turtlebot Graphic Interface",
            font=("Helvetica", 40, "bold"),
            fg="#263238",
            bg=self.header_frame.cget("bg")
        )
        self.header_label.grid(row=0, column=0, sticky="nsew")
        # ---------------------------------------------
        #                   MAIN FRAME                  # Riga 1, colonna 0: Occupa tutta la parte inferiore
        # ---------------------------------------------
        self.main_frame = tk.Frame(self.window, bg="#B0BEC5", padx=5, pady=5)
        self.main_frame.grid(row=1, column=0, sticky="nsew")
        self.main_frame.columnconfigure(0, weight=2)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        self.left_frame = tk.Frame(self.main_frame, bg="#B0BEC5")
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.left_frame.rowconfigure(0, weight=1)
        self.left_frame.rowconfigure(1, weight=3)
        self.left_frame.columnconfigure(0, weight=1)

        self.right_frame = tk.Frame(self.main_frame, bg="#B0BEC5", padx=5, pady=5)
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.rowconfigure(0, weight=1)
        self.right_frame.columnconfigure(0, weight=1)

        # ---------------------------------------------
        #               BUTTOM FRAME (LEFT)
        # ---------------------------------------------
        self.button_frame = tk.Frame(self.left_frame, bg="#E0F7F5", padx=5, pady=5, bd=2, relief="solid")
        self.button_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.button_frame.rowconfigure("all", weight=1)
        self.button_frame.columnconfigure(0, weight=1, minsize=BTN_WIDTH)
        self.button_frame.columnconfigure(1, weight=1, minsize=BTN_WIDTH)

        self.l_b = tk.Label(self.button_frame,
                            text="Select the guide type for the next Test",
                            font=("Helvetica", 20, "bold"),
                            fg="#263238",
                            bg="#FAF9F6",
                            height=2,
                            bd=2,
                            relief="solid")
        self.l_b.grid(row=0, column=0, sticky="nsew", columnspan=2, padx=10, pady=10)

        for i in range(4):
            self.b_b = tk.Button(self.button_frame,
                                 width=BTN_WIDTH,
                                 height=2,
                                 command= lambda i=i: set_guide_type(i),
                                 text=BTN_GUIDE_TXT[i],
                                 bg="#B2DFDB",
                                 fg="#263238",
                                 bd=2,
                                 relief="solid",
                                 font=("Helvetica", 15, "italic", "bold"), )
            if i < 2:
                self.b_b.grid(row=1, column=i, sticky="nsew", padx=15, pady=15)
            else:
                self.b_b.grid(row=2, column=i - 2, sticky="nsew", padx=15, pady=15)

        # ---------------------------------------------
        #                 PARAMETER FRAME (LEFT)
        # ---------------------------------------------
        self.parameter_frame = tk.Frame(self.left_frame, bg="#E0F7F5", padx=5, pady=5, bd=2, relief="solid")
        self.parameter_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.parameter_frame.rowconfigure(0, weight=1)
        self.parameter_frame.rowconfigure(1, weight=1)
        self.parameter_frame.rowconfigure(2, weight=1)
        self.parameter_frame.rowconfigure(3, weight=1)
        self.parameter_frame.rowconfigure(4, weight=1)
        self.parameter_frame.rowconfigure(5, weight=1)
        self.parameter_frame.columnconfigure(0, weight=1, minsize=BTN_WIDTH)
        self.parameter_frame.columnconfigure(1, weight=1, minsize=BTN_WIDTH)
        self.parameter_frame.columnconfigure(2, weight=1, minsize=BTN_WIDTH)
        self.parameter_frame.columnconfigure(3, weight=1, minsize=BTN_WIDTH)

        self.l_ps = tk.Label(self.parameter_frame,
                             text="Record data",
                             font=("Helvetica", 20, "bold"),
                             fg="#263238",
                             bg="#FAF9F6",
                             bd=2,
                             relief="solid")
        self.l_ps.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.on_registration = tk.PhotoImage(file="~/tesi/src/smartwalker_pkg/images/on.png")
        self.off_registration = tk.PhotoImage(file="~/tesi/src/smartwalker_pkg/images/off.png")
        self.on_button = tk.Button(self.parameter_frame, image=self.off_registration, bg="#E0F7F5", bd=0, command=switch,
                                   activebackground="#E0F7F5", highlightthickness=0)
        self.on_button.grid(row=0, column=2, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.l1_ps = tk.Label(self.parameter_frame,
                              text="Modify guide parameters down here",
                              font=("Helvetica", 30, "bold"),
                              bd=2,
                              fg="#263238",
                              bg="#E0F7F5",
                              relief="solid")
        self.l1_ps.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        self.x_l_ps = tk.Label(self.parameter_frame,
                               text="x",
                               font=("Helvetica", 20, "bold"),
                               fg="#263238",
                               bg="#E0F7F5", )
        self.x_l_ps.grid(row=2, column=2, sticky="nsew", padx=10, pady=10)

        self.y_l_ps = tk.Label(self.parameter_frame,
                               text="y",
                               font=("Helvetica", 20, "bold"),
                               fg="#263238",
                               bg="#E0F7F5", )
        self.y_l_ps.grid(row=2, column=3, sticky="nsew", padx=10, pady=10)

        self.start_point_l_ps = tk.Label(self.parameter_frame,
                                         text="Start point",
                                         font=("Helvetica", 20, "bold"),
                                         fg="#263238",
                                         bg="#E0F7F5", )
        self.start_point_l_ps.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        self.val_x_sp = tk.Entry(self.parameter_frame, width=BTN_WIDTH)
        self.val_x_sp.grid(row=3, column=2, sticky="nsew", padx=5, pady=5)
        self.val_y_sp = tk.Entry(self.parameter_frame, width=BTN_WIDTH)
        self.val_y_sp.grid(row=3, column=3, sticky="nsew", padx=5, pady=5)

        manual_sp_set = tk.Button(self.parameter_frame,
                                  width=BTN_WIDTH,
                                  height=2,
                                  command= lambda i=0: pose_cases(i),
                                  text="Manual Set",
                                  bg="#B2DFDB",
                                  fg="#263238",
                                  bd=2,
                                  relief="solid",
                                  font=("Helvetica", 15, "italic", "bold"),)
        manual_sp_set.grid(row=3, column=4, sticky="nsew", padx=10, pady=10)

        self.end_point_l_ps = tk.Label(self.parameter_frame,
                                       text="End point",
                                       font=("Helvetica", 20, "bold"),
                                       fg="#263238",
                                       bg="#E0F7F5", )
        self.end_point_l_ps.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)

        manual_ep_set = tk.Button(self.parameter_frame,
                                  width=BTN_WIDTH,
                                  height=2,
                                  command= lambda i=1: pose_cases(i),
                                  text="Manual Set",
                                  bg="#B2DFDB",
                                  fg="#263238",
                                  bd=2,
                                  relief="solid",
                                  font=("Helvetica", 15, "italic", "bold"), )
        manual_ep_set.grid(row=4, column=4, sticky="nsew", padx=10, pady=10)

        self.val_x_ep = tk.Entry(self.parameter_frame, width=BTN_WIDTH)
        self.val_x_ep.grid(row=4, column=2, sticky="nsew", padx=5, pady=5)
        self.val_y_ep = tk.Entry(self.parameter_frame, width=BTN_WIDTH)
        self.val_y_ep.grid(row=4, column=3, sticky="nsew", padx=5, pady=5)

        self.thick_point_l_ps = tk.Label(self.parameter_frame,
                                         text="Thickness [m]",
                                         font=("Helvetica", 20, "bold"),
                                         fg="#263238",
                                         bg="#E0F7F5", )
        self.thick_point_l_ps.grid(row=5, column=0, sticky="nsew", padx=10, pady=10)

        self.val_thick = tk.Entry(self.parameter_frame, width=BTN_WIDTH)
        self.val_thick.grid(row=5, column=2, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.amp_point_l_ps = tk.Label(self.parameter_frame,
                                       text="Amplitude (only for onduline)",
                                       font=("Helvetica", 20, "bold"),
                                       fg="#263238",
                                       bg="#E0F7F5", )
        self.amp_point_l_ps.grid(row=6, column=0, sticky="nsew", padx=10, pady=10)

        self.val_amp = tk.Entry(self.parameter_frame, width=BTN_WIDTH)
        self.val_amp.grid(row=6, column=2, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.update_button = tk.Button(self.parameter_frame,
                                       text="Update parameters",
                                       font=("Helvetica", 20, "bold"),
                                       bg="#B2DFDB",
                                       fg="#263238",
                                       command = self.update_parameters)
        self.update_button.grid(row=7, column=0, sticky="nsew", padx=10, pady=10, columnspan=4)

        # ---------------------------------------------
        #           NAVIGATION FRAME (RIGHT)
        # ---------------------------------------------
        self.navigation_frame = tk.Frame(self.main_frame, bg="#E0F7F5", padx=5, pady=5, bd=2, relief="solid")
        self.navigation_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.navigation_frame.rowconfigure(0, weight=1)
        self.navigation_frame.rowconfigure(1, weight=1)
        self.navigation_frame.rowconfigure(2, weight=1)
        self.navigation_frame.rowconfigure(3, weight=1)
        self.navigation_frame.rowconfigure(4, weight=1)
        self.navigation_frame.columnconfigure(0, weight=1)
        self.nav_label = tk.Label(self.navigation_frame,
                                  text= "Navigate to these locations",
                                  font=("Helvetica", 20, "bold"),
                                  fg="#263238",
                                  bg="#FAF9F6",
                                  bd=2,
                                  relief="solid")
        self.nav_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        for i in range(4):
            self.nav_butt = tk.Button(self.navigation_frame,
                                 height=2,
                                 command= lambda i=i: self.ros_queue.put(self.pose[i]),
                                 text=self.pose_labels[i],
                                 bg="#B2DFDB",
                                 fg="#263238",
                                 bd=2,
                                 relief="solid",
                                 font=("Helvetica", 15, "italic", "bold"),)
            self.nav_butt.grid(row=i+1, column=0, sticky="nsew", padx=10, pady=10)

    def process_queue(self):
        try:
            goal = self.ros_queue.get_nowait()
            self.send_goal(goal)
        except queue.Empty:
            pass

# rifarsi a move_test per capire il funzionamento
    def send_goal(self, posa):
        goal = NavigateToPose.Goal()
        goal.pose.header.frame_id = "map"
        goal.pose.pose = posa
        self._future_goal = self._action_client.send_goal_async(goal)
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
            return
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().info("Gaol cancelled.")
            return
        elif status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("Goal Reached.")
            return

def main(args=None):
    rclpy.init(args=args)
    param_server = ParameterServer()
    try:
        ros_thread = threading.Thread(
            target=rclpy.spin,
            args=(param_server,),
            daemon=True
        )
        ros_thread.start()

        param_server.window.mainloop()
    except KeyboardInterrupt:
        print("Terminating...")
        param_server.window.destroy()
    finally:
        param_server.destroy_node()

if __name__ == '__main__':
    main()