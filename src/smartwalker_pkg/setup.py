from setuptools import find_packages, setup
from glob import glob

package_name = 'smartwalker_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*')),
        ('share/' + package_name + '/map', glob('map/*')),
        ('share/' + package_name + '/model', glob('model/*')),
        ('share/' + package_name + '/param', glob('param/*')),
        ('share/' + package_name + '/rviz', glob('rviz/*')),
        ('share/' + package_name + '/urdf', glob('urdf/*')),
        ('share/' + package_name + '/world', glob('world/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='',
    maintainer_email='@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'velocity_data = src.velocity_data:main',
            'elaborate_data = src.elaborate_data:main',
            'initial_pose = src.initial_pose:main',
            'move_test = src.move_test:main',
            'rehabilitation_guide = src.rehabilitation_guide:main',
            'subscribe_to_data = src.subscribe_to_data:main',
            'odom_data_collector = src.odom_data_collector:main',
            'parameter_server = src.parameter_server:main',
        ],
    },
)
