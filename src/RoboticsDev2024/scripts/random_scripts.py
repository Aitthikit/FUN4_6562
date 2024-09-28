#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from math import pi
from spatialmath import *
import roboticstoolbox as rtb
import numpy as np
from geometry_msgs.msg import PoseStamped
from robot_interface.srv import Random
import random

class RandomNode(Node):
    def __init__(self):
        super().__init__('random_node')
        self.random_pub = self.create_publisher(PoseStamped,'/target',10)
        self.create_service(Random,'/random',self.random_callback)
        self.random_client = self.create_client(Random,'/random')
        self.dt = 1
        self.create_timer(self.dt, self.sim_loop)
        self.robot = rtb.DHRobot(
            [
                rtb.RevoluteMDH(d = 0.2),
                rtb.RevoluteMDH(alpha = -pi/2 , d=-0.12 , offset = -pi/2),
                rtb.RevoluteMDH(a=0.25,d= 0.10),
            ],
            name = "RRR_Robot"
            )
        self.tool_frame = SE3( 0,-0.28, 0) @ SE3.RPY(pi/2,0,0) 
        self.robot.tool = self.tool_frame
        print(self.robot)
        self.r_max = (0.28+0.25)**2
        self.r_min = (0.03)**2
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
       
        self.flag = 1
        
    def random_callback(self, request:Random.Request, response:Random.Response):
        if request.randomreq.data == 1:
            self.get_logger().info(f'respond {response}')
            self.flag = 1
            response.randomres.data = True
            return response
        else:
            response.randomres.data = False
            return response
        # if request == 2:
        #     self.flag = 0
            
        #     self.get_logger().info(f'respond {response}')
        # return response
    
    def sim_loop(self):
        if self.flag == 1:
            self.x = random.uniform(-0.52, 0.52)
            self.y = random.uniform(-0.52, 0.52)
            self.z = random.uniform(-0.52, 0.52)+0.2
            self.r = self.x**2 + self.y**2 + (self.z-0.2)**2
            new_pose = SE3(self.x,self.y,self.z)
            self.posi = self.robot.ik_LM(new_pose,mask=[1,1,1,0,0,0]) 
            if self.r > self.r_min and self.r < self.r_max and self.posi[1] == 1:
                # self.get_logger().info(f'R {self.r},{self.r_max},{self.r_min}')
                self.flag = 0
        # if self.flag == 3:
                msg = PoseStamped()
                msg.header.frame_id = 'link_0'
                msg.pose.position.x = self.x
                msg.pose.position.y = self.y
                msg.pose.position.z = self.z
                self.random_pub.publish(msg)
                # self.get_logger().info(f'gopose {self.x},{self.y},{self.z}')
                # self.flag = 1 

        # print(self.robot)
def main(args=None):
    rclpy.init(args=args)
    node = RandomNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()