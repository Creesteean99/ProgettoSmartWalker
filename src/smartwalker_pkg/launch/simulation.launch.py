from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PythonExpression
from launch.conditions import IfCondition
from launch_ros.actions import Node
import os

def generate_launch_description():

    ld = LaunchDescription()

    use_sim_time = LaunchConfiguration('use_sim_time')
    map_yaml_file = LaunchConfiguration('map_yaml_file')
    send_initial_pose = LaunchConfiguration('send_initial_pose')
    which_locator = LaunchConfiguration('locator')
    rviz_config = LaunchConfiguration('rviz_config')
    bringup_dir = get_package_share_directory('smartwalker_pkg')


# DICHIARAZIONE VARIABILI D'AMBIENTE -----------------------------------------------------------------------------------

    declare_map_yaml_cmd = DeclareLaunchArgument(
        'map_yaml_file',
        default_value = 'planimetria.yaml',
        description='Full path to map file to load')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value = 'True',
        description= 'Use simulation (Gazebo) clock if true.',
    )

    declare_send_initial_pose_cmd = DeclareLaunchArgument(
        'send_initial_pose',
        default_value = 'True',
        description= 'Send initial pose to simulation.',
    )

    declare_locator = DeclareLaunchArgument(
        'locator',
        default_value='AMCL',
        description='Which locator to use: EKF or AMCL'
    )

    declare_rviz_config = DeclareLaunchArgument(
        'rviz_config',
        default_value = os.path.join(bringup_dir, 'rviz', 'sim_config.rviz'),
        description='Which RViz config to use')

# LAUNCH DI GAZEBO -----------------------------------------------------------------------------------------------------
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                bringup_dir,
                'launch',
                'gazebo_simulation.launch.py'
            )
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
        condition=IfCondition(use_sim_time)
    )

# LAUNCH DI RVIZ, MAP SERVER E AMCL ------------------------------------------------------------------------------------
    display= IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                bringup_dir,
                'launch',
                'display_simulation.launch.py'
            )
        ),
        launch_arguments={'use_sim_time': use_sim_time,
                          'map_yaml_file':map_yaml_file,
                          'send_initial_pose':send_initial_pose,
                          'rviz_config':rviz_config}.items()
    )

# LAUNCH NAVIGATION PLUGIN -------- ------------------------------------------------------------------------------------
    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('nav2_bringup'),
                'launch',
                'navigation_launch.py'
            )
        ),
        launch_arguments={
            'namespace': '',
            'use_sim_time': use_sim_time,
            'autostart': 'true',
            'params_file': os.path.join(bringup_dir, 'param', 'nav2_params.yaml'),
        }.items()
    )

# LAUNCH DEI VARI NODI DI SIMULAZIONE ----------------------------------------------------------------------------------
    data_nodes = IncludeLaunchDescription(

        PythonLaunchDescriptionSource(
            os.path.join(
                bringup_dir,
                'launch',
                'data_nodes.launch.py'
            )
        ),
        launch_arguments={'localizator': which_locator}.items()
    )

# LAUNCH DEGLI EKF LOCALE E GLOBALE ------------------------------------------------------------------------------------
    start_local_ekf = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_local_filter',
        output='screen',
        parameters=[os.path.join(
            bringup_dir,
            'param',
            'ekf_local.yaml'
        )],
        condition=IfCondition(
            PythonExpression(["'", which_locator, "' == 'EKF'"])
        )
    )
    start_global_ekf = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_global_filter',
        output='screen',
        parameters=[os.path.join(
            bringup_dir,
            'param',
            'ekf_global.yaml'
        )],
        remappings=[('/odometry/filtered','/odometry/filtered_global')],
        condition=IfCondition(
            PythonExpression(["'", which_locator, "' == 'EKF'"])
        )
    )

    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_map_yaml_cmd)
    ld.add_action(declare_send_initial_pose_cmd)
    ld.add_action(declare_locator)
    ld.add_action(declare_rviz_config)
    ld.add_action(gazebo)
    ld.add_action(display)
    ld.add_action(data_nodes)
    ld.add_action(navigation)
    ld.add_action(start_local_ekf)
    ld.add_action(start_global_ekf)
    return ld