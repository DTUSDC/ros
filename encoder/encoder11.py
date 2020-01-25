import rospy
from std_msgs.msg import Int16

def callback(data):
    rospy.loginfo(data.data)
    
def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("chatter", Int16, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()