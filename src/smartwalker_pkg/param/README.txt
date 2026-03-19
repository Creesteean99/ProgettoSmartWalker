--------------[ITA]--------------

L'utilizzo delle accelerazioni lineari nell'EKF è sconsigliato a causa del rumore e del bias intrinseco delle IMU. Questo causa generalmente un drift continuo, anche quando il robot è fermo, influenzando sia l'EKF locale che quello globale.
Inoltre, l'EKF globale dovrebbe teoricamente integrare i dati di 'odometry/filtered' (EKF locale) e le correzioni di AMCL. Sebbene questa configurazione funzionasse in simulazione, ha generato problemi non approfonditi nel sistema reale, portando al ripristino della configurazione attuale.

NB I: La taratura dei parametri dei due filtri EKF è stata eseguita in modo empirico e sperimentale. Si raccomanda vivamente un approccio più metodico per ottimizzare i risultati.

NB II: Se si utilizza AMCL per la localizzazione e la pubblicazione delle trasformate (TF), assicurarsi che 'tf_broadcast' sia impostato su 'True' nel file 'nav2_param.yaml'. In questo caso, l'EKF globale NON deve pubblicare le TF per evitare conflitti nel TF tree. Viceversa, se si sceglie Robot_localization come localizzatore primario, impostare 'publish_tf' su 'True' nell'EKF globale e su 'False' in AMCL.

NB III: Quando si utilizza l'EKF locale per la stima dell'odometria, è necessario che sia quest'ultimo a pubblicare le TF di sistema, e non il driver del robot o Gazebo.

_Per il robot reale: seguire la procedura indicata nel manuale presente in laboratorio.

_In Gazebo: aprire il file 'burger_model.sdf' (directory 'model') e, approssimativamente alla riga 405, impostare <publish_odom_tf> su 'false'.

--------------[ENG]--------------

Using linear accelerations in the EKF is discouraged due to IMU noise and bias. This typically leads to continuous drift even when the robot is stationary, affecting both local and global EKF instances.
Additionally, the global EKF should theoretically integrate data from 'odometry/filtered' (local EKF) and AMCL corrections. While this setup worked in simulation, it caused unresolved issues on the physical robot; therefore, the system was reverted to its current configuration.

NOTE I: The parameter tuning for both EKF filters was performed empirically. A more methodical calibration approach is strongly recommended to achieve better performance.

NOTE II: If using AMCL as the primary localization and TF broadcasting system, ensure that 'tf_broadcast' is set to 'True' in 'nav2_param.yaml'. In this configuration, the global EKF must NOT publish TFs to avoid TF tree conflicts. Conversely, if Robot_localization is chosen for global positioning, set 'publish_tf' to 'True' in the global EKF and 'False' in the AMCL configuration.

NOTE III: When using a local EKF for odometry estimation, the EKF must publish the system TFs instead of the robot driver or Gazebo.

    Physical Robot: Follow the steps outlined in the laboratory manual.

    Gazebo: Open the 'burger_model.sdf' file in the 'model' directory and, near line 405, set <publish_odom_tf> to 'false'.
