from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    ld= LaunchDescription()
    which_locator = LaunchConfiguration('locator')
    package = 'smartwalker_pkg'

    declare_locator = DeclareLaunchArgument(
        'locator',
        default_value='AMCL',
        description='Tipo di localizzazione: EKF o AMCL'
    )

    start_parameter_server = Node(
        package=package,
        executable='parameter_server',
        name= 'parameter_server',
        output='screen',
        parameters=[{
            'localization_type': which_locator,
        }]
    )

    start_elaborate_data = Node(
        package=package,
        executable='elaborate_data',
        name='elaborate_data',
        output='screen',
    )

    start_odom_data_collector = Node(
        package= package,
        executable='odom_data_collector',
        name='odom_data_collector',
        output='screen',
        parameters=[{
            'localization_type': which_locator,
        }]
    )

    start_rehabilitation_guide = Node(
        package=package,
        executable='rehabilitation_guide',
        name='rehabilitation_guide_maker',
        output='screen',
    )

    start_velocity_data = Node(
        package= package,
        executable='velocity_data',
        name='velocity_data_collector',
        output='screen',
    )

    ld.add_action(declare_locator)
    ld.add_action(start_parameter_server)
    ld.add_action(start_velocity_data)
    ld.add_action(start_elaborate_data)
    ld.add_action(start_odom_data_collector)
    ld.add_action(start_rehabilitation_guide)
    return ld