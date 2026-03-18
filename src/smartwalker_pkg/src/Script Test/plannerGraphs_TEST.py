#!/usr/bin/env python3
from cProfile import label

import numpy as np
import matplotlib.pyplot as plt
from custom_classes.parameters import HOME, BED, TOILETTE, COUCH
from custom_classes import csv_handler as ch
import os

def main():
    vs = 'p' #'l' per localizzatori, 'p' per pianificatori
    match vs:
        case 'p':
            _, plan_navfn_x, plan_navfn_y = ch.read_from_csv_two_values('navfn','planners')
            _, plan_smac_x, plan_smac_y = ch.read_from_csv_two_values('smac','planners')
            _, plan_thetas_x, plan_thetas_y = ch.read_from_csv_two_values('thetas','planners')
            fig, ax_plan = plt.subplots()
            ax_plan.plot(plan_navfn_x, plan_navfn_y, linewidth=1, color='coral', label='Navfn')
            ax_plan.plot(plan_smac_x, plan_smac_y, linewidth=1, color='yellowgreen', label='SMAC2D')
            ax_plan.plot(plan_thetas_x, plan_thetas_y, linewidth=1, color='blue', label='ThetaStar')
            ax_plan.text(HOME.position.x, HOME.position.y - 0.05, 'STAZIONE', fontsize=8, ha='center', va='top')
            ax_plan.text(BED.position.x, BED.position.y - 0.05, 'LETTO', fontsize=8, ha='center', va='top')
            ax_plan.text(TOILETTE.position.x, TOILETTE.position.y - 0.05, 'BAGNO', fontsize=8, ha='center', va='top')
            ax_plan.text(COUCH.position.x, COUCH.position.y - 0.05, 'DIVANO', fontsize=8, ha='center', va='top')
            ax_plan.plot(HOME.position.x, HOME.position.y, marker='*', color='black')
            ax_plan.plot(BED.position.x, BED.position.y, marker='*', color='black')
            ax_plan.plot(TOILETTE.position.x, TOILETTE.position.y, marker='*', color='black')
            ax_plan.plot(COUCH.position.x, COUCH.position.y, marker='*', color='black')
            ax_plan.legend()
            ax_plan.grid(True)
            ax_plan.xaxis.set_label_text("Posizione X")
            ax_plan.yaxis.set_label_text("Posizione Y")
            output_dir = os.path.expanduser("/src/smartwalker_pkg/plots/plannerTests")
            filename = "test1.png"
            path = os.path.join(output_dir, filename)
            plt.savefig(path, dpi=150)
            plt.show()
            plt.close()
        case 'l':
            all_errors = []
            fig, ax = plt.subplots()
            for i in range(10):
                t_gt, gtx, gty = ch.read_from_csv_two_values(f'TEST_GT_EKF_{i}','ekf')
                t_rp, rpx, rpy = ch.read_from_csv_two_values(f'TEST_LOC_EKF_{i}','ekf')
                t = np.linspace(0, 1, 10000)
                gtx_n = np.interp(t, np.linspace(0, 1, len(gtx)), gtx)
                gty_n = np.interp(t, np.linspace(0, 1, len(gty)), gty)
                rpx_n = np.interp(t, np.linspace(0, 1, len(rpx)), rpx)
                rpy_n = np.interp(t, np.linspace(0, 1, len(rpy)), rpy)

                errors = np.sqrt((gtx_n-rpx_n)**2 + (gty_n-rpy_n)**2)
                all_errors.append(errors)
                ax.plot(t,errors, label= f'test{i+1}',linewidth=1)

            mean_error = np.mean(all_errors)
            mean_error_constant = np.full_like(t, mean_error)
            ax.plot(t, mean_error_constant, color='red', linewidth=2, label='Errore Medio (RMSE)')

            # ax.set_title("Andamento Errore di Localizzazione (EKF vs GT)")
            ax.set_xlabel("Percorso [%]")
            ax.set_ylabel("Errore [m]")
            ax.grid(True, linestyle='--')
            ax.grid(True)
            ax.legend()
            output_dir = os.path.expanduser("/src/smartwalker_pkg/plots/GTvsRP")
            filename = "EKF.png"
            path = os.path.join(output_dir, filename)
            plt.savefig(path,
                        dpi=300,  # 300 DPI è lo standard per la stampa/tesi
                        bbox_inches='tight',  # Rimuove i bordi bianchi inutili e non taglia le scritte
                        format='png',  # Specifica il formato
                        facecolor='white')
            plt.show()
            plt.close()


if __name__ == '__main__':
    main()