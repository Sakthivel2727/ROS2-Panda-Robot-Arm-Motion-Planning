import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint


class MotionSequenceNode(Node):

    def __init__(self):
        super().__init__('motion_sequence_node')

        self._action_client = ActionClient(
            self,
            FollowJointTrajectory,
            '/panda_arm_controller/follow_joint_trajectory'
        )

    def move_arm(self, positions):

        self.get_logger().info('Waiting for Panda controller...')

        if not self._action_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('Panda controller not available.')
            return False

        goal = FollowJointTrajectory.Goal()

        goal.trajectory.joint_names = [
            'panda_joint1',
            'panda_joint2',
            'panda_joint3',
            'panda_joint4',
            'panda_joint5',
            'panda_joint6',
            'panda_joint7'
        ]

        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start.sec = 3

        goal.trajectory.points.append(point)

        self.get_logger().info('Sending motion goal...')

        future = self._action_client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, future)

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error('Motion goal rejected.')
            return False

        self.get_logger().info('Motion goal accepted.')

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)

        self.get_logger().info('Motion completed.')

        return True


def main(args=None):

    rclpy.init(args=args)

    node = MotionSequenceNode()

    # Small movement from the current Panda position
    target = [
        0.20,
        -0.785,
        0.00,
        -2.356,
        0.00,
        1.571,
        0.785
    ]

    node.move_arm(target)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
