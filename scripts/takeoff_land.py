#! /usr/bin/env python
import sys
import rospy

import actionlib
from iarc7_motion.msg import QuadMoveGoal, QuadMoveAction
from iarc7_safety.SafetyClient import SafetyClient

def takeoff_land():
    safety_client = SafetyClient('takeoff_land_abstract')
    # Since this abstract is top level in the control chain there is no need to check
    # for a safety state. We can also get away with not checking for a fatal state since
    # all nodes below will shut down.
    assert(safety_client.form_bond())
    if rospy.is_shutdown(): return

    # Creates the SimpleActionClient, passing the type of the action
    # (QuadMoveAction) to the constructor. (Look in the action folder)
    client = actionlib.SimpleActionClient("motion_planner_server", QuadMoveAction)

    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()
    if rospy.is_shutdown(): return

    rospy.sleep(5.0)

    for i in range(0, 2):
        # Test takeoff
        goal = QuadMoveGoal(movement_type="takeoff")
        # Sends the goal to the action server.
        client.send_goal(goal)
        # Waits for the server to finish performing the action.
        client.wait_for_result()
        if rospy.is_shutdown(): return
        rospy.logwarn("Takeoff success: {}".format(client.get_result()))

        #rospy.logwarn("Begin hovering")
        #goal = QuadMoveGoal(movement_type="velocity_test", x_velocity=0.0, y_velocity=0.0, z_position=0.4)
        # Sends the goal to the action server.
        #client.send_goal(goal)
        #rospy.sleep(10.0)
        #client.cancel_goal()
        #if rospy.is_shutdown(): return
        #rospy.logwarn("Done hovering")

        for i in range(0, 1):

            rospy.logwarn("Ascending")
            goal = QuadMoveGoal(movement_type="velocity_test", x_velocity=0.0, y_velocity=0.0, z_position=1.0)
            # Sends the goal to the action server.
            client.send_goal(goal)
            rospy.sleep(3.0)
            client.cancel_goal()
            if rospy.is_shutdown(): return
            rospy.logwarn("Done asending")


            rospy.logwarn("Descending")
            goal = QuadMoveGoal(movement_type="velocity_test", x_velocity=0.0, y_velocity=0.0, z_position=0.8)
            # Sends the goal to the action server.
            client.send_goal(goal)
            rospy.sleep(3.0)
            client.cancel_goal()
            if rospy.is_shutdown(): return
            rospy.logwarn("Done descending")

        # Test land
        goal = QuadMoveGoal(movement_type="land")
        # Sends the goal to the action server.
        client.send_goal(goal)
        # Waits for the server to finish performing the action.
        client.wait_for_result()
        if rospy.is_shutdown(): return
        rospy.logwarn("Land success: {}".format(client.get_result()))

if __name__ == '__main__':
    # Initializes a rospy node so that the SimpleActionClient can
    # publish and subscribe over ROS.
    rospy.init_node('takeoff_land_abstract')
    takeoff_land()
    rospy.spin()
