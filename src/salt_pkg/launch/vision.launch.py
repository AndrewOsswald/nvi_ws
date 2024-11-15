import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
import launch

def generate_launch_description():

  use_sim_time = LaunchConfiguration('use_sim_time', default='false')
  xacro_file_name = '/home/seniorproject/nvi_ws/install/salt_pkg/share/salt_pkg/urdf/robot_model.xacro'

  launch.actions.ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'], output='screen'),

  config_rviz2 = os.path.join(
        get_package_share_directory('zed_display_rviz2'),
        'rviz2',
        'zedm' + '.rviz'
    )

  return LaunchDescription([
        
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui'
        ),  
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[
                {'use_sim_time': LaunchConfiguration('use_sim_time')},
                {'robot_description': Command([
                    'xacro', ' ', xacro_file_name, ' ',
                    
                    ])},
            ],
            #remappings=[
            #    ('/tf', 'tf'),
            #    ('/tf_static', 'tf_static')
            #]
        ),
        Node(
            package='rviz2',
            namespace='zedm',
            executable='rviz2',
            name='zedm_rviz2',
            arguments=['-d', '/home/seniorproject/nvi_ws/src/salt_pkg/config/config.rviz'],
            output='screen',
        ),
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            arguments=['-d', '/home/seniorproject/nvi_ws/src/salt_pkg/config/config.rviz']
        ),
        Node(
            package='zed_wrapper',
            executable='zed_wrapper',
            parameters=[
                {'camera_model': 'zedm'},
            ],
            namespace='zedm',
            name='zed_node',
        ),
        

        
    
        
  ])