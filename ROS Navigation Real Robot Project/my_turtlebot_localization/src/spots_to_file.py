#! /usr/bin/env python

import rospy
from my_turtlebot_localization.srv import MyServiceMessage, MyServiceMessageResponse
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseWithCovarianceStamped
import time

class SaveSpots(object):

    def __init__(self):

        self.pose = PoseWithCovarianceStamped()
        self.detection_dict = {"corner1":self.pose, "corner2":self.pose, "pedestrian":self.pose}
        self.my_service = rospy.Service('/save_spot', MyServiceMessage , self.srv_callback)
        self.pose_sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped , self.sub_callback)
    
    def sub_callback(self, msg):

        self.pose = msg

    def srv_callback(self, request):

        label = request.label
        response = MyServiceMessageResponse()


        if label == "corner1":
            self.detection_dict["corner1"] = self.pose
            response.message = "Saved Pose for corner1 spot"
            
        elif label == "corner2":
            self.detection_dict["corner2"] = self.pose
            response.message = "Saved Pose for corner2 spot"
            
        elif label == "pedestrian":
            self.detection_dict["pedestrian"] = self.pose
            response.message = "Saved Pose for pedestrian spot"
        
        elif label == "end":
            with open('spots.txt', 'w') as file:
                
                for key, value in self.detection_dict.iteritems():
                    if value:
                        file.write(str(key) + ':\n----------\n' + str(value) + '\n===========\n')
                
                response.message = "Written Poses to spots.txt file"
                
        else:
            response.message = "No label with this name. Try with corner1, corner2, pedestrian or end(to write the file)"
        
        
        response.success = True
        
        return response

if __name__ == '__main__':

    rospy.init_node('spot_recorder')
    save_spot = SaveSpots()
    rospy.spin()

