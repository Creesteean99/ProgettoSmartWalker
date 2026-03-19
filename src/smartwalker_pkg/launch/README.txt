--------------[ITA]--------------

simulation.launch.py è il file di lancio principale che gestisce l'intero sistema.
È possibile modificare diverse impostazioni direttamente da terminale:

use_sim_time:
    'False' per l'utilizzo con il robot fisico.
    'True' per l'utilizzo in simulazione.
    (default = True)

map_yaml_file:
    Inserire il nome del file .yaml della mappa da caricare in Rviz.
    (default = 'planimetria.yaml')

send_initial_pose:
    'False' per non inviare la posa iniziale ad AMCL.
    'True' per inizializzare AMCL con la posa definita nel nodo initial_pose.py.
    (default = True)

which_locator:
    'AMCL' per raccogliere i dati di posizione dal localizzatore AMCL.
    'EKF' per raccogliere i dati dal pacchetto robot_localization.
    (default = 'AMCL')

rviz_config:
    Inserire il nome del file .rviz da caricare. È possibile utilizzare quello di default.

NB: Se si desidera utilizzare esclusivamente l'EKF, è sufficiente impostare il valore di default su 'EKF' nel DeclareArgument all'interno di simulation.launch.py. In alternativa, è possibile modificare i nodi velocity_data e odom_data_collector per sottoscriverli direttamente ai topic di robot_localization, rimuovendo i DeclareArguments e le LaunchConfigurations corrispondenti.

ESEMPIO:
ros2 launch smartwalker_pkg simulation.launch.py use_sim_time:=False send_initial_pose:=False map_yaml_file:=csmtlab.yaml
RISULTATO: Il sistema si avvia per l'uso fisico (senza Gazebo), non invia la posa iniziale e carica la mappa del laboratorio.

ATTENZIONE: La mappa del laboratorio ('csmtlab.yaml') è estremamente parziale. Si raccomanda vivamente di effettuare una nuova mappatura dell'ambiente prima dell'uso.


--------------[ENG]--------------
simulation.launch.py is the primary launch file that manages the entire system.
Several settings can be modified directly from the terminal:

use_sim_time:
    'False' for physical robot operation.
    'True' for simulation use.
    (default = True)

map_yaml_file:
    The name of the .yaml map file to be loaded in Rviz.
    (default = 'planimetria.yaml')

send_initial_pose:
    'False' to skip AMCL initial pose initialization.
    'True' to initialize AMCL using the pose defined in the initial_pose.py node.
    (default = True)

which_locator:
    'AMCL' to collect positioning data from the AMCL localizer.
    'EKF' to collect data from the robot_localization package.
    (default = 'AMCL')

rviz_config:
    The name of the .rviz configuration file to load. The default file can be used.

NB: To use EKF exclusively, simply change the default value to 'EKF' in the DeclareArgument within simulation.launch.py. Alternatively, you can modify the velocity_data and odom_data_collector nodes to subscribe directly to the robot_localization topics, removing the corresponding DeclareArguments and LaunchConfigurations.

EXAMPLE:
ros2 launch smartwalker_pkg simulation.launch.py use_sim_time:=False send_initial_pose:=False map_yaml_file:=csmtlab.yaml
RESULT: The system launches for physical use (without Gazebo), does not send an initial pose, and loads the laboratory map.

ATTENTION: The laboratory map ('csmtlab.yaml') is very incomplete. It is strongly recommended to perform a new mapping of the environment before use.
