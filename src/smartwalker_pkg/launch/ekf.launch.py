from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    ld= LaunchDescription()
    bringup_dir = get_package_share_directory('tesi_pkg')
    start_ekf = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_global_filter',
        output='screen',
        parameters=[os.path.join(
            bringup_dir,
            'param',
            'ekf_global.yaml'
        )]
    )

    ld.add_action(start_ekf)

    return ld