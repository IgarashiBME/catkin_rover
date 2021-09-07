#!/usr/bin/python
# -*- coding: utf-8 -*-
import rospy
import tf2_ros

class tf_test():
    def __init__(self):
        # ROS ノードの初期化処理
        rospy.init_node('tf2_listener')

        # リスナーの登録
        self.tfBuffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tfBuffer)

    def loop(self):
        rate=rospy.Rate(10.0)

        while not rospy.is_shutdown():
            # /map に対する /base_link の Transform を取得
            try:
                #t = tfBuffer.lookup_transform('xxx', 'world', rospy.Time())
                t = self.tfBuffer.lookup_transform('map', 'base_link', rospy.Time())
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
                print(e)
                rate.sleep()
                continue

            rover_pos = t.transform.translation
            rover_quat = t.transform.rotation
            print('pos x:{0:.3f}, y:{1:.3f}, z:{2:.3f}'.format(
                rover_pos.x,
                rover_pos.y,
                rover_pos.z
            ))
            print('quat x:{0:.2f}, y:{1:.2f}, z:{2:.2f}, w:{3:.2f}\n\n'.format(
                rover_quat.x,
                rover_quat.y,
                rover_quat.z,
                rover_quat.w
            ))

            rate.sleep()

if __name__ == '__main__':
    # start the cmd_vel subscriber
    t = tf_test()
    t.loop()
