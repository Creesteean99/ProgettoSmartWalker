#-------------------------------------------------------------
#   Questo launch file si limita ad attivare
#   Gazebo e a far spawnare il robot all'interno
#   della simulazione. Verranno attivati anche
#   il robot_state_publisher per permettere
#   ad Rviz di mostrare nella sua finestra.
#-------------------------------------------------------------
import math
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
# from src.tesi_pkg.src.custom_classes.parameters import HOME

def generate_launch_description():

    ld = LaunchDescription()
    bringup_dir = get_package_share_directory('tesi_pkg')
    gazebo_pkg = get_package_share_directory('gazebo_ros')

    # Generazione delle variabili di configurazione di lancio
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Variabili di configurazione di lancio specifiche della simulazione
    world = LaunchConfiguration('world')
    pose = {'x': LaunchConfiguration('x_pose', default='2.5'),
            'y': LaunchConfiguration('y_pose', default='-2.1'),
            'z': LaunchConfiguration('z_pose', default='0.03'),
            'R': LaunchConfiguration('roll', default='0.0'),
            'P': LaunchConfiguration('pitch', default='0.0'),
            'Y': LaunchConfiguration('yaw', default=f'{math.radians(90)}'),}
    robot_name = LaunchConfiguration('robot_name')
    robot_sdf = LaunchConfiguration('robot_sdf')

    # Dichiarazioni variabili di lancio
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value = 'true',
        description= 'Use simulation (Gazebo) clock if true',
    )
    declare_world_cmd = DeclareLaunchArgument(
        'world',
        default_value=os.path.join(bringup_dir, 'world', 'planimetria_with_guide.world'),
        description='Full path to world file to load'
    )

    declare_robot_name_cmd = DeclareLaunchArgument(
        'robot_name',
        default_value='turtlebot3_burger',
        description='Robot name to use'
    )

    declare_robot_sdf_cmd = DeclareLaunchArgument(
        'robot_sdf',
        default_value=os.path.join(bringup_dir,'model','burger_model.sdf'),
        description='Full path to SDF file to load'
    )

    start_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gazebo_pkg, 'launch', 'gazebo.launch.py')),
        launch_arguments = {'world': world}.items()
    )

    urdf = os.path.join(bringup_dir, 'urdf', 'turtlebot3_burger.urdf')
    with open(urdf, 'r') as infp:
        robot_description = infp.read()

    start_gazebo_spawner_cmd = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        output='screen',
        arguments=[
            '-entity', robot_name,
            '-file', robot_sdf,
            '-robot_namespace', '',
            '-x', pose['x'], '-y', pose['y'], '-z', pose['z'],
            '-R', pose['R'], '-P', pose['P'], '-Y', pose['Y']])


    #
    start_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name= 'robot_state_publisher_launch',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_description},],
    )

    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_world_cmd)
    ld.add_action(declare_robot_name_cmd)
    ld.add_action(declare_robot_sdf_cmd)

    ld.add_action(start_gazebo)
    ld.add_action(start_gazebo_spawner_cmd)
    ld.add_action(start_robot_state_publisher)

    return ld