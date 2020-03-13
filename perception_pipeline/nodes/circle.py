#!/usr/bin/env python

# Takes image input from a ROS topic, converts to OpenCV image using ROSBridge,
# draws a circle on it and publishes it to another topic

from __future__ import print_function
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import String
import cv2
import rospy
import sys

import roslib
roslib.load_manifest('perception_pipeline')

class image_converter:

    def __init__(self):
        self.image_pub = rospy.Publisher(
            "camera/rgb/image_raw", Image, queue_size=10)

        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber(
            "/usb_cam/image_raw", Image, self.callback)

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        (rows, cols, channels) = cv_image.shape
        if cols > 60 and rows > 60:
            cv2.circle(cv_image, (200, 200), 100, 255)

        cv2.imshow("Image window", cv_image)
        cv2.waitKey(3)

        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        except CvBridgeError as e:
            print(e)


def main(args):
    rospy.init_node('image_converter', anonymous=True)
    ic = image_converter()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
