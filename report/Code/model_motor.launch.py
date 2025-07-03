from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch.actions import ExecuteProcess

def generate_launch_description():
    # Path to the URDF/Xacro file
    urdf_file_path = '/home/noi/pw2/scr/digital_twin/model/description/robo.urdf.xacro'
    control_yaml = "/home/noi/pw2/scr/digital_twin/model/config/control.yaml"

    return LaunchDescription([
        # Node for robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': Command(['xacro ', urdf_file_path])
            }]
        ),
        
        # Joint State Publisher
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen'
        ),
        ################################################################################################
        # Node for RViz2
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', '/home/noi/pw2/scr/digital_twin/model/config/batmobil_config.rviz']  # Path to your RViz config file
        ),

        # Node(
        #     package='tf2_ros',
        #     executable='static_transform_publisher',
        #     name='static_tf_pub',
        #     arguments=['0', '0', '0', '0', '0', '0', 'odom', 'dummy_link'],
        #     output='screen'
        # ),
        ###############################################################################################
        
        # Gazebo starten mit "gz sim"
        ExecuteProcess(
            cmd=['gz', 'sim', '-r', 'empty.sdf'],
            output='screen'
        ),
        
        Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_robot',
        arguments=[
            '-topic', '/robot_description',  # Beschreibung des Roboters
            '-name', 'batmobile'  # Name des Roboters in Gazebo
            ],
            output='screen',
        ),

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='cmd_vel_bridge',
            arguments=['/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist'],
            output='screen'
        ),
        ##########################################################################################################

        Node(
            package='serial_motor_demo',  # Ersetze mit deinem Paketnamen
            executable='cmd_vel_to_motor_command',
            name='cmd_vel_to_motor_command',
            output='screen'
        ),
         # Node for MotorGui
        #  Node(
        #      package='serial_motor_demo',
        #      executable='gui',
        #      name='motor_gui',
        #     output='screen'
        # ),


    ])
