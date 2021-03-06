#! /usr/bin/env python

import rospy
import time
import os
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class rgbd_saver():
    def __init__(self):
        rospy.init_node('camera_save_node')
        rospy.on_shutdown(self.shutdown)
        # function of transform ROS_image to opencv_image
        self.bridge = CvBridge()

        # ROS callback function, receive /image_raw mesage
        rospy.Subscriber('/d400/color/image_raw', Image, self.image_callback)
        rospy.Subscriber('/d400/aligned_depth_to_color/image_raw', Image, self.depth_callback)

        # prevents overwriting for saved images in the past
        self.file_path = os.path.expanduser('~') + "/images/"
        file_list = os.listdir(self.file_path)
        numbers=[]

        if len(file_list) > 0:
            for i in file_list:
                numbers.append(int(i[:-10]))
            self.group_number = max(numbers)+1
        else:
            self.group_number = 1
        print("group number is", self.group_number)
        self.seq = 1
        
    def image_callback(self, msg):
        # transform ROS_image to opencv_image
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            print "Cv_Brdige_Error"

    def depth_callback(self, msg):
        # transform ROS_image to opencv_image
        try:
            self.cv_image_depth = self.bridge.imgmsg_to_cv2(msg, "passthrough")
            #self.depth_array = np.array(self.cv_image_depth, dtype=np.uint16)
        except CvBridgeError as e:
            print e

    def shutdown(self):
        print "shutdown"

    def loop(self):
        while not rospy.is_shutdown():
            try:
                self.cv_image
                self.cv_image_depth
            except AttributeError as e:
                print(e)
                continue
            img8 = (self.cv_image_depth).astype('uint8')
            depth_colormap = cv2.applyColorMap(img8, cv2.COLORMAP_JET);

            cv2.imshow("rgb", self.cv_image)
            cv2.imshow("depth", depth_colormap)
            key = cv2.waitKey(1)

            # save images
            if key == ord("v"):
                print(self.cv_image_depth)

            # next group_number
            if key == ord("n"):
                self.group_number = self.group_number +1
                print("move to the next group_number", self.group_number)
                self.seq = 1

            if key == 27: #[esc] key
                break
    
if __name__ == '__main__':
    r = rgbd_saver()
    r.loop()
