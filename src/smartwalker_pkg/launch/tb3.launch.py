import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node

def generate_launch_description():

    ld = LaunchDescription()

    bringup_dir = get_package_share_directory('tesi_pkg')
    gazebo_pkg = get_package_share_directory('gazebo_ros')

    # Generazione delle variabili di configurazione di lancio
    map_yaml_file = LaunchConfiguration('map')
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Variabili di configurazione di lancio specifiche della simulazione
    rviz_config_file = LaunchConfiguration('rviz_config_file')
    world = LaunchConfiguration('world')
    pose = {'x': LaunchConfiguration('x_pose', default='2.50'),
            'y': LaunchConfiguration('y_pose', default='-2.50'),
            'z': LaunchConfiguration('z_pose', default='0.01'),
            'R': LaunchConfiguration('roll', default='0.00'),
            'P': LaunchConfiguration('pitch', default='0.00'),
            'Y': LaunchConfiguration('yaw', default='0.00')}
    robot_name = LaunchConfiguration('robot_name')
    robot_sdf = LaunchConfiguration('robot_sdf')

    # Variables
    lifecycle_node = ['map_server','amcl']

    # Dichiarazione degli argomenti
    declare_map_yaml_cmd = DeclareLaunchArgument(
        'map',
        default_value=os.path.join(
            bringup_dir, 'map', 'planimetria.yaml'),
        description='Full path to map file to load')


    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value = 'true',
        description= 'Use simulation (Gazebo) clock if true',
    )

    declare_rviz_config_cmd = DeclareLaunchArgument(
        'rviz_config_file',
        default_value=os.path.join(bringup_dir, 'rviz', 'base_config.rviz'),
        description='Full path to rviz config file to load'
    )

    declare_world_cmd = DeclareLaunchArgument(
        'world',
        default_value=os.path.join(bringup_dir, 'world', 'planimetria.world'),
        description='Full path to world file to load'
    )

    declare_robot_name_cmd = DeclareLaunchArgument(
        'robot_name',
        default_value='turtlebot3_waffle',
        description='Robot name to use'
    )

    declare_robot_sdf_cmd = DeclareLaunchArgument(
        'robot_sdf',
        default_value=os.path.join(bringup_dir, 'model', 'turtlebot3_waffle.sdf'),
        description='Full path to SDF file to load'
    )

    start_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gazebo_pkg, 'launch', 'gazebo.launch.py')),
        launch_arguments = {'world': world}.items()
    )

    urdf = os.path.join(bringup_dir, 'urdf', 'turtlebot3_burger.urdf')
    with open(urdf, 'r') as infp:
        robot_description = infp.read()

    start_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name= 'robot_state_publisher_launch',
        output='screen',
        parameters=[{'use_sim_time': True, 'robot_description': robot_description}],
    )

    start_gazebo_spawner_cmd = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        output='screen',
        arguments=[
            '-entity', robot_name,
            '-file', robot_sdf,
            '-x', pose['x'], '-y', pose['y'], '-z', pose['z'],
            '-R', pose['R'], '-P', pose['P'], '-Y', pose['Y']])

    start_map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{
            'yaml_filename': map_yaml_file,
            'use_sim_time': use_sim_time
        }],
        respawn_delay = 2.0
    )

    start_amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
    )

    start_lifecycle_manager_cmd = Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_map_server',
            output='screen',
            arguments=['--ros-args', '--log-level', 'info'],
            parameters=[{'use_sim_time': use_sim_time},
                        {'autostart': True},
                        {'node_names': lifecycle_node}])

    start_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen',
    )

    ld.add_action(declare_map_yaml_cmd)
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_rviz_config_cmd)
    ld.add_action(declare_world_cmd)
    ld.add_action(declare_robot_name_cmd)
    ld.add_action(declare_robot_sdf_cmd)
    ld.add_action(start_gazebo)
    ld.add_action(start_robot_state_publisher)
    ld.add_action(start_gazebo_spawner_cmd)
    ld.add_action(start_map_server)
    ld.add_action(start_amcl)
    ld.add_action(start_lifecycle_manager_cmd)
    ld.add_action(start_rviz)
    return ld

# import os
#
# from ament_index_python.packages import get_package_share_directory
# from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch.substitutions import Command, LaunchConfiguration
# from launch_ros.actions import Node
#
#
# def generate_launch_description():
#     pkg_share = get_package_share_directory('tesi_pkg')
#     default_model_path = os.path.join(pkg_share, 'src', 'description', 'turtlebot3_description.sdf')
#     default_rviz_config_path = os.path.join(pkg_share, 'rviz', 'config.rviz')
#     world_path = os.path.join(pkg_share, 'world', 'planimetria.world')
#
#     robot_state_publisher_node = Node(
#         package='robot_state_publisher',
#         executable='robot_state_publisher',
#         parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('model')])}, {'use_sim_time': LaunchConfiguration('use_sim_time')}]
#     )
#     rviz_node = Node(
#         package='rviz2',
#         executable='rviz2',
#         name='rviz2',
#         output='screen',
#         arguments=['-d', LaunchConfiguration('rvizconfig')],
#     )
#
#     launch.actions.ExecuteProcess(
#         cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'],
#         output='screen'),
#
#     # Spawn robot
#     spawn_entity = launch_ros.actions.Node(
#         package='gazebo_ros',
#         executable='spawn_entity.py',
#         arguments=['-entity', 'turtlebot', '-topic', 'robot_description'],
#         output='screen'
#     )
#
#     robot_localization_node = Node(
#         package='robot_localization',
#         executable='ekf_node',
#         name='ekf_node',
#         output='screen',
#         parameters=[os.path.join(pkg_share, 'config/ekf.yaml'), {'use_sim_time': LaunchConfiguration('use_sim_time')}],
#     )
#
#     return LaunchDescription([
#         DeclareLaunchArgument(name='model', default_value=default_model_path, description='Absolute path to robot model file'),
#         DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path, description='Absolute path to rviz config file'),
#         DeclareLaunchArgument(name='use_sim_time', default_value='True', description='Flag to enable use_sim_time'),
#         ExecuteProcess(cmd=['gz', 'sim', '-g'], output='screen'),
#         robot_state_publisher_node,
#         spawn_entity,
#         rviz_node,
#         robot_localization_node,
#     ])