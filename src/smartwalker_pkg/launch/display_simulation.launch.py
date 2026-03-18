#-------------------------------------------------------------
#   Questo launch file si limita ad attivare
#   il map_server contenente la mappa anticipatamente
#   creata tramite lo SLAM-toolbox e lanciare Rviz
#   con il file di configurazione creato.
#   Essendo map_server un lifecycle Node, bisogna
#   attivare il nodo con il nav2_lifecycle manager
#   Inoltre, verrà attivato l'AMCL (Adaptive Monte Carlo Localization)
#   in modo da poter avere la trasformazione map->odom necessaria
#   a sincronizzare la posizione su Gazebo e Rviz
#-------------------------------------------------------------

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterFile
from launch.conditions import IfCondition


def generate_launch_description():

    ld = LaunchDescription()
    bringup_dir = get_package_share_directory('tesi_pkg')
    lifecycle_node = ['map_server', 'amcl']
    package = 'smartwalker_pkg'

# Generazione delle variabili di configurazione di lancio --------------------------------------------------------------
    map_yaml_file = LaunchConfiguration('map_yaml_file')
    use_sim_time = LaunchConfiguration('use_sim_time')
    send_initial_pose = LaunchConfiguration('send_initial_pose')
    rviz_config = LaunchConfiguration('rviz_config')

# Dichiarazione degli argomenti ----------------------------------------------------------------------------------------

    declare_map_yaml_cmd = DeclareLaunchArgument(
        'map_yaml_file',
        default_value= 'planimetria2.yaml',
        description='Full path to map file to load')


    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value = 'True',
        description= 'Use simulation (Gazebo) clock if true',
    )

    declare_rviz_config = DeclareLaunchArgument(
        'rviz_config',
        default_value=os.path.join(bringup_dir, 'rviz', 'sim_config.rviz'),
        description= 'Full path to rviz config file',
    )

    configured_params = ParameterFile(
        param_file=os.path.join(bringup_dir, 'param', 'nav2_params.yaml'),
    )

    declare_send_initial_pose_cmd = DeclareLaunchArgument(
        'send_initial_pose',
        default_value = 'True',
        description= 'Send the initial pose of the robot automatically.',
    )

# MAP SERVER -----------------------------------------------------------------------------------------------------------
    start_map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{
            'yaml_filename': PathJoinSubstitution([bringup_dir,'map',map_yaml_file]),
            'use_sim_time': use_sim_time
        }],
    )

# AMCL -----------------------------------------------------------------------------------------------------------------
    start_amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[configured_params],
    )

# LIFE CYCLE MANAGER ---------------------------------------------------------------------------------------------------
    start_lifecycle_manager_cmd = Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_map_server',
            output='screen',
            arguments=['--ros-args', '--log-level', 'info'],
            parameters=[{'use_sim_time': use_sim_time,
                        'autostart': True,
                        'node_names': lifecycle_node,
                        'bond_timeout': 5.0,}])
# RVIZZ ----------------------------------------------------------------------------------------------------------------
    start_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': use_sim_time}],
    )

# INITIAL POSE NODE ----------------------------------------------------------------------------------------------------
    send_initial_pose = Node(
        package=package,
        executable='initial_pose',
        name= 'send_initial_pose',
        output='screen',
        condition=IfCondition(send_initial_pose),
    )

    ld.add_action(declare_map_yaml_cmd)
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_rviz_config)
    ld.add_action(declare_send_initial_pose_cmd)
    ld.add_action(send_initial_pose)
    ld.add_action(start_amcl)
    ld.add_action(start_map_server)
    ld.add_action(start_lifecycle_manager_cmd)
    ld.add_action(start_rviz)

    return ld