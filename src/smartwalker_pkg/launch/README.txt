simulation.launch.py è il file di lancio comprensivo di tutto il sistema.
Si possono modificare da terminale alcune impostazioni direttamente tra cui:

- use_sim_time = 'False' per l'utilizzo del robot,
                 'True'  per l'uso in simulato
                 (default = True)

- map_yaml_file = Inserire la stringa del nome della mappa .yaml da caricare in Rviz.
                  (default = 'planimetria.yaml')

- send_initial_pose = 'False' per non inizializzare la posa iniziale di AMCL
                      'True' per inizializzare l'AMCL con la posa definita nel nodo initial_pose.py
                      (default = True)

- which_locator = 'AMCL' per raccogliere i dati di posizione dal localizzatore AMCL
                  'EKF' per raccogliere i dati di posizione dal localizzatore Robot_localization
                  (default = 'AMCL')

- rviz_config = Inserire la stringa del nome del file .rviz da caricare. Quello di default può essere comunque utilizzata.

NB: qualora si volesse utilizzare esclusivamente EKF, basta modificare il DeclareArgument in simulation.launch.py ed inserire
in default 'EKF'. Altrimenti, si possono modificare i vari velocity_data e odom_data_collector per sottoscriversi esclusivamente
al topic di robot_localization, rimuovendo i DeclareArguemtns e LaunchCOnfiguration.

ESEMPIO: ros2 launch smartwalker_pkg simulation.launch.py use_sim_time:=False send_initial_pose:=False map_yaml_file:=csmtlab.yaml
RISULTATO: La simulazione parte senza aprire Gazebo, non inviando la posizione iniziale e all'interno della mappa del laboratorio.


ATTENZIONE: La mappa del laboratorio è stata mappata non parzialmente, di più. Fortemente consigliato una rimappatura dell'ambiente.