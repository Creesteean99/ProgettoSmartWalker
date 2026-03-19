#!/usr/bin/env python3

import os.path
import numpy as np
import rclpy
from rclpy.node import Node
from .custom_classes import csv_handler as ch
from .custom_classes import curve_manipolation as pl
from custom_interfaces.srv import CSVFileName
from custom_interfaces.msg import Parameter
from rclpy.qos import QoSProfile, DurabilityPolicy

import matplotlib.pyplot as plt

class DataElaborator(Node):
    def __init__(self):
        super().__init__('data_elaborator')
        self.csv_file_name = 'testNonOk'
        self.csv_server = self.create_service(CSVFileName, 'csv_file', self.get_filename)
        self.get_logger().info("Ready to recive CSV files.")
        self.guide_type = None
        self.num_points = 10000
        self.qos = QoSProfile(depth=1)
        self.qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
        self.parameter_subscription = self.create_subscription(
            Parameter,
            topic='/parameters_config',
            callback=self.get_config_parameters,
            qos_profile=self.qos
        )

    def get_config_parameters(self, config):
        # Aggiorna i parametri ricevuti da pannello di controllo
        self.guide_type = config.guide_type
        self.start_point = config.start_point
        self.end_point = config.end_point
        self.thickness = config.thickness
        self.amplitude = config.amplitude
        self.delta = self.thickness / 2

    def get_filename(self, req, res):
        res.message = "File recived."
        self.csv_file_name = req.filename
        self.directory = req.directory
        if self.guide_type is None:
            res.message = "No guide was selected. Ensure the guide has been declared and re-run the test."
            raise ValueError("No guide selected!")
        else:
            self.get_logger().info("CSV file recived.. Processing data.")
            self.plot_data()
        return res


    def guide_rs_transform(self): # Calcolo della matrice di rototraslazione per il sistema di riferimento solidale con la giuda.
        # Definizione dei due sistemi di riferimento
        global_axis = np.array([[1.0,0.0], [0.0,1.0]])
        origin = self.start_point
        vector = np.array([[self.end_point.x - self.start_point.x, self.end_point.y - self.start_point.y]])
        norme = np.linalg.norm(vector)
        base_rs = np.divide(vector,norme)

        # Creazione matrice di rototraslazione
        costheta = np.dot(global_axis[0],base_rs[0])
        sintheta = np.dot(global_axis[1], base_rs[0])
        R = np.vstack(((costheta,-sintheta),(sintheta,costheta)))
        t = np.vstack([[origin.x,origin.y]])
        M = np.eye(3)
        M[:2,:2] = R
        M[:2,2] = t
        M_t = np.linalg.inv(M)  # M_10
        return M,M_t

    def plot_data(self):
        match self.directory:
            # Finita la prova, odom_data_collector invia il CSV PRIMA di velocity_data. Qualora venisse cambiato questo
            # ordine, lo script dovrebbe non funzionare.
            case "odometry":
                self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1,
                                                              figsize=(10, 8),
                                                              gridspec_kw={"height_ratios": [3, 1]},
                                                              constrained_layout=True,
                                                              )
                self.get_logger().info("Started Odometry")
                t, x, y = ch.read_from_csv_two_values(self.csv_file_name, dir= 'odometry')
                M, M_t = self.guide_rs_transform()

                robot_abs_coord = np.vstack(
                    (np.interp(np.linspace(0,1,self.num_points),
                               np.linspace(0,1,len(x)),
                               x),
                     np.interp(np.linspace(0, 1, self.num_points),
                               np.linspace(0, 1, len(y)),
                               y),
                     np.ones(self.num_points)))


                self.gamma, self.reference = pl.parametric_guide(self.guide_type, self.start_point, self.end_point, self.amplitude, self.num_points, M_t)
                subject_perf = M_t @ robot_abs_coord
                self.ax1.plot(subject_perf[0, :], subject_perf[1, :], label="Traiettoria Paziente", linewidth=3, color='coral')
                self.ax1.grid()
                self.ax1.axis("equal")

                # Adding guide thickness
                poly_x, poly_y = pl.get_band_area(self.reference[:-1,:], self.delta)
                self.ax1.fill(poly_x, poly_y, alpha=0.25, color="blue", label="Guida")

                # Accuracy evaluation
                accuracy = pl.calculate_errors(gamma= self.reference,
                                               robot=subject_perf,
                                               Emax=self.thickness,
                                               delta=self.delta)
                self.ax1.text(
                    0.02, 0.98,
                    f"Accuratezza: {accuracy:.2f}%",
                    transform=self.ax1.transAxes,
                    fontsize=15,
                    verticalalignment='top',
                    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
                )
                self.ax1.set_xlabel("Posizione X [m]")
                self.ax1.set_ylabel("Posizione Y [m]")
                self.ax1.legend(loc="upper right", fontsize = 15)
                self.get_logger().info("Finished Odometry")

            case "velocity":
                t, vel = ch.read_from_csv_one_value(self.csv_file_name, dir='velocity')
                dt = np.diff(t)
                mean_vel = np.cumsum(vel[1:] * dt)[-1] / t[-1]
                self.ax2.plot(t,vel,label="Velocity")
                self.ax2.grid()
                self.ax2.text(
                    0.85, 0.3,
                    f"Velocità media: {mean_vel:.2f}m/s\nTempo totale: {t[-1]:.2f}s",
                    transform=self.ax2.transAxes,
                    fontsize=15,
                    verticalalignment='top',
                    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
                )
                self.ax2.set_xlabel("Tempo [s]")
                self.ax2.set_ylabel("Velocità [m/s]")
                output_dir = os.path.expanduser("~/tesi/src/smartwalker_pkg/plots")
                filename = f"{self.csv_file_name}_summary.png"
                path = os.path.join(output_dir, filename)
                plt.savefig(path, dpi=150)
                plt.show()
                plt.close()
                self.get_logger().info(f"Plot saved to: {path}")


def main(args=None):
    rclpy.init(args=args)
    data_elab = DataElaborator()
    try:
        rclpy.spin(data_elab)
    except KeyboardInterrupt:
        print("Terminating...")
    finally:
        data_elab.destroy_node()

if __name__ == '__main__':
    main()