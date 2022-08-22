# import the opencv library
#!/home/pannatorn/anaconda3/bin/python

import math
import rospy
import sys
import cv2
import numpy as np
from sensor_msgs.msg import Image as msgImage
from cv_bridge import CvBridge,CvBridgeError
class RealsenseListener:
    def __init__(self):
        self.ground=[]
        self.topic()
        self.bridge=CvBridge()
        self.publisher()
        self.subscriber()
    def topic(self):
        self.DepthTopic='/camera/depth/image_rect_raw'
        self.DepthprocessTopic='/camera/depth/depth_process'
    def subscriber(self):
        self.DepthSub=rospy.Subscriber(self.DepthTopic,msgImage,self.imageDepthCallback)
    def publisher(self):
        self.Depth_process_pub = rospy.Publisher(self.DepthprocessTopic, msgImage, queue_size=10)
    def imageDepthCallback(self,data):
        try:
            cv_image=self.bridge.imgmsg_to_cv2(data,"passthrough")
            if len(self.ground) != 0:
                depth_process=abs(cv_image-self.ground.any())
                median=cv2.medianBlur(cv_image,5)
                msg_image=self.bridge.cv2_to_imgmsg(depth_process,"passthrough") 
                self.Depth_process_pub.publish(msg_image)
            cv2.imshow("frame",cv_image)
            if cv2.waitKey(1) & 0xFF==ord('s'):
                cv2.imwrite('/home/pannatorn/catkin_ws/src/imu_orientation/image/base.png',cv_image)
                self.ground=cv_image
        except CvBridgeError as e:
            print(e)
            return

if __name__=="__main__":
    rospy.init_node("depth_image_processor")
    listener=RealsenseListener()
    rospy.spin()
    
    