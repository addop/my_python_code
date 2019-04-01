import cv2
import os
import sys
import numpy as np
from tqdm import tqdm
import copy
import pandas as pd
import random
import serial as sr
import time


class my_cam:
    def __init__(self, frame_number=None):
        self.cam_env_get = None
        self.cam_id = None
        self.cam_state = None
        self.video_path = None
        self.movie_name = None
        self.movie_state = None
        self.out = None
        self.fourcc = None
        self.frame_number = frame_number
        self.cam_on = None
        self.cam_shape = None
        # 串口通信
        self.trigger = None
        self.port = None
        self.port_state = None
        self.time = None
        self.info_log = []
        self.info_get_b = None
        self.info_get = None

        # print('\033[1;31;40m')  # 下一目标输出背景为黑色，颜色红色高亮显示
        # print('*' * 50)
        # print('\033[7;31mplease ignore the OpenCV red warning! \033[1;31;40m')  # 字体颜色红色反白处理
        # print('*' * 50)
        # print('\033[0m')

    def cam_environment(self):
        # 直接返回摄像头编号和每一个的分辨率情况, 以方便后期调用
        grabbed = True
        cam_id_token = 0
        cam_env = []
        while grabbed is True:
            cam_env_token = cv2.VideoCapture(cam_id_token)
            grabbed, get_frame = cam_env_token.read()
            cam_env.append([cam_id_token, grabbed, np.shape(get_frame)])
            cam_env_token.release()
            cv2.destroyAllWindows()
            if grabbed is False:
                break
            cam_id_token += 1
        self.cam_env_get = cam_env
        return self.cam_env_get

    def cam_id_choose(self):
        if self.cam_env_get is None:
            print('WARNING! no cam in here! please run cam_environment()')
            self.cam_state = False
        print('cam environment is ', self.cam_env_get)
        if len(self.cam_env_get) == 1:
            self.cam_id = 0
            self.cam_shape = self.cam_env_get[self.cam_id][2]
            self.cam_state = True
        else:
            self.cam_id = len(self.cam_env_get) - 2  # self.cam_env_get的最后一个是False, 所以是无用数据, 所以这里id应该是len()-2
            self.cam_shape = self.cam_env_get[self.cam_id][2]
            self.cam_state = True
        print('Cam ID is ', self.cam_id)
        print('Cam State is ', self.cam_state)
        print('*'*20)

    def get_frame(self):
        my_cam.read_info(self)  # 这里读取数据, 尝试更改self.trigger
        if self.trigger:
            frame_number_token = 0
            while frame_number_token < self.frame_number:
                record_grabbed, record_frame = self.cam_on.read()
                frame_number_token += 1
                if record_grabbed is not True:
                    continue
                self.out.write(record_frame)
            self.trigger = False

    def prepare_movie(self):
        self.fourcc = cv2.VideoWriter_fourcc(*'H264')
        movie_shape = (self.cam_shape[1], self.cam_shape[0])
        print('movie shape is ', movie_shape)
        self.out = cv2.VideoWriter('output.mov', self.fourcc, 120.0, movie_shape)  # 帧数可调, 注意后面的尺寸大小要一致
        # 格式 | 结果
        # avi | 可以, 但QuickTime无法打开预览
        # rmvb | 可以, QuickTime可以打开但需要转换, 尺寸更小
        # mp4 | 会报错, 但QuickTime可以打开
        # mov | 会报错, 但QuickTime可以打开
        my_cam.get_frame(self)
        self.out.release()

    def start_record(self):
        if self.cam_id is None or self.cam_state is None:
            print('No camera has been chose! please run cam_id_choose()')
            self.movie_state = False
            return self.movie_state
        self.cam_on = cv2.VideoCapture(self.cam_id)
        if self.cam_on.isOpened():
            self.cam_state = True
        else:
            self.cam_state = False
        my_cam.prepare_movie(self)
        self.cam_on.release()
        cv2.destroyAllWindows()

    def open_port(self, port_path=None):
        self.port = sr.Serial(port=port_path, baudrate=9600)
        # self.port.open()
        if self.port.is_open:
            self.port_state = True

    def get_time(self):
        TAG = time.localtime()
        self.time = str(TAG.tm_mon)+'-'+\
                    str(TAG.tm_mday)+'_'+\
                    str(TAG.tm_hour)+'H'+\
                    str(TAG.tm_min)+'M'+\
                    str(TAG.tm_sec)+'S'

    def read_info(self):
        if self.port_state is not True:
            print('port is not open !, please check the open_port() or port_path')
            return None
        my_cam.get_time(self)
        while self.trigger is not True:
            n = self.port.inWaiting()  # 不确定这里不用等待一段时间的话会不会不合适>>>time.sleep(1)
            if n:
                self.info_get_b = self.port.read(n)
                self.info_get = str(self.info_get_b, encoding="utf-8")
                if self.info_get == 'H':
                    self.info_log.append(self.time)
                    self.info_log.append(self.info_get)
                    self.trigger = True


camera = my_cam(frame_number=120)  # 打开class, 设置记录总帧数
result = camera.cam_environment()  # 获取摄像头环境
camera.cam_id_choose()  # 获取摄像头id
camera.open_port(port_path='/dev/cu.usbmodem144301')  # 开启串口
camera.start_record()  # 开始记录
print(camera.info_log)  # 打印每次记录结果
