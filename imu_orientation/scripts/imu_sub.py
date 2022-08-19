#!/usr/bin/env python

import math
import rospy
import sys
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion

class imu_orientation :

  def __init__(self):
      self.param_initial()
      self.Subscriber()
      print(1)
      

  def param_initial(self):
      self.X=None
      self.Y=None
      self.Z=None
      self.W=None
      
  def Subscriber(self):
      self.sub_Orientation=rospy.Subscriber("/imu/data",Imu,self.callback)


  def euler_from_quaterniin(self,w,x,y,z):
    """
    Convert a quaternion into euler angles (roll, pitch, yaw)
    roll is rotation around x in radians (counterclockwise)
    pitch is rotation around y in radians (counterclockwise)
    yaw is rotation around z in radians (counterclockwise)
    """
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)
    if roll_x <0 : 
       roll_x+=(22/7)*2
    if pitch_y<0:
      pitch_y+=(22/7)*2
    if yaw_z<0:
       yaw_z+=(22/7)*2

    return roll_x, pitch_y, yaw_z # in radians
 


  
  
        
  def callback(self,Imu_info):
      self.X=Imu_info.orientation.x
      self.Y=Imu_info.orientation.y
      self.Z=Imu_info.orientation.z
      self.W=Imu_info.orientation.w
      roll_x,pitch_y,yaw_z = self.euler_from_quaterniin(self.W,self.X,self.Y,self.Z)
      print(roll_x,pitch_y,yaw_z)
      #print(self.W,self.X,self.Y,self.Z)



def main(args):
  imu_node = imu_orientation()
  rospy.init_node('imu_orientation')
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)
