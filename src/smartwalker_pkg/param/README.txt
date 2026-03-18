Contrariamente da quanto scritto nell'elaborato, l'utilizzo delle accelerazioni lineari nel EKF è sconsigliato,
visto il rumore e il bias delle IMU. Questo comporta generalmente a drift continuo in situazioni in cui il robot
è fermo. Questo vale sia per l'EKF locale che quello globale.
Inoltre, l'EKF globale dovrebbe integrare i dati provenienti da odometry/filtered, ovvero l'EKF locale e le correzioni
di AMCL. Sebbene questo funzionasse in simulato, in reale ha generato problemi i quali non sono stati approfonditi,
ritornando alla configurazione attuale.

NB I: La taratura dei parametri dei due filtri EKF è stata eseguita in modo empirici e sperimentale, non ottimale. Si consiglia
      vivamente un approccio più metodico per ottenere risultati migliori.

NB II: Qualora si voglia usare AMCL come sistema di localizzazione e pubblicazione tf, bisogna andare nel file nav2_param.yaml ed assicurarsi che tf_broadcast sia a True.
       In questa configuazione, però, il filtro ekf globale NON dovrà pubblicare le tf, altrimenti si creano problemi di tf_tree.
       Viceversa, se è Robot_localization ad essere scelto come localizzatore, publish_tf va settato a true in ekf_globale, SETTANDO A FALSE quello di AMCL in nav2_param.yaml

NB III: Utilizzando anche un EKF locale per la previsione dell'odometria, è necessario che EKF locale pubblichi le tf del
        sistema e non il robot/Gazebo. Per il robot fisico, ci sono i passaggi da  seguire all'interno del libretto nel laboratorio.
        In Gazebo, è necessario aprire il file burger_model.sdf nella directory  "model" e, a riga circa 405, modificare <publish_odom_tf> a false.
