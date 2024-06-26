#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math

class SimpleRobot:
    def __init__(self):
        # 初始化ROS節點
        rospy.init_node('simple_robot', anonymous=True)
        # 定義速度話題發布
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        # 定義雷射掃描的數據
        self.laser_subscriber = rospy.Subscriber('/scan', LaserScan, self.laser_callback)
        # 初始化Twist消息
        self.cmd = Twist()
        # 設置循環頻率
        self.rate = rospy.Rate(10)
        # 定義安全距離
        self.safe_distance = 0.5
        # 前方距離初始化
        self.front_distance = float('inf')

    def laser_callback(self, data):
        # 獲取前方一定角度範圍內的最小距離
        front_angles = range(-10, 10)
        self.front_distance = min([data.ranges[i] for i in front_angles])

    def move(self):
        while not rospy.is_shutdown():
            # 如果前方距離小於安全距離，則轉向
            if self.front_distance < self.safe_distance:
                self.cmd.linear.x = 0.0
                self.cmd.angular.z = 0.5
            # 否則，向前移動
            else:
                self.cmd.linear.x = 0.5
                self.cmd.angular.z = 0.0
            # 發布速度命令
            self.velocity_publisher.publish(self.cmd)
            # 休眠一段時間以保持循環頻率
            self.rate.sleep()

if __name__ == '__main__':
    try:
        robot = SimpleRobot()
        robot.move()
    except rospy.ROSInterruptException:
        pass
