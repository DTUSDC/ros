import rospy
from std_msgs.msg import Float32

# def callback1(ticks):
#    rospy.loginfo(ticks.data)


def callback2(vel):
    rospy.loginfo(vel.data)


def listener():
    rospy.init_node('listener', anonymous=True)

    #rospy.Subscriber("chatter", Float32, callback1)
    rospy.Subscriber("vel", Float32, callback2)

    rospy.spin()


if __name__ == '__main__':
    listener()
