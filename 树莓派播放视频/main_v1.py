#!/usr/bin/python3

# 播放视频的同时从高电平输出信号
# 程序需要在树莓派上使用

# 视频模块
from omxplayer import OMXPlayer
from pathlib import Path
from time import sleep
import os

# 高低电平控制模块
import RPi.GPIO as GPIO
import time


class high_signal:
    def __init__(self, channels):
        self.channels = channels
        self.logging = None
        self.channel = None

        GPIO.setmode(GPIO.BOARD)
        for channel in channels:
            GPIO.setup(channel, GPIO.OUT)

    def on(self, channel):
        GPIO.output(channel, GPIO.HIGH)

    def off(self, channel):
        GPIO.output(channel, GPIO.LOW)

    def clean(self):
        GPIO.cleanup()

    def run(self, channel):
        self.on(channel)
        self.time.sleep(0.1)
        self.off(channel)


class video_and_tag:
    def __init__(self, fl_path):
        self.movie_fl_path = None
        self.channels = None
        self.player = None
        self.movie_pool = None
        self.fl_path = fl_path
        self.play_log = None

    def logging(self, info):
        self.play_log = self.play_log + info

    def get_file_pool(self):
        file_pool = []
        file_box = os.listdir(self.fl_path)
        for item in file_box:
            if item.split('.')[0] == '' or item.split('.')[-1] != 'mp4':  # 这里不能用is not
                continue
            file_pool.append(item)
        file_pool.sort()
        self.movie_pool = file_pool

    def play_movie(self, fl_path):
        self.movie_fl_path = fl_path
        VIDEO_PATH = Path(self.movie_fl_path)
        self.player = OMXPlayer(VIDEO_PATH)

    def stop_movie(self):
        self.player.quit()

sleep(5) # 等待5秒后开始刺激

signal = high_signal([7])  # 7号可以驱动LED点亮
video = video_and_tag(fl_path='/media/pi/KINGSTON/movie_bag')
video.get_file_pool()

for file in video.movie_pool:
    print(file)

    signal.on(signal.channels[0])
    video.play_movie(video.fl_path + '/' + file)

    sleep(1)
    # print('yes')
    signal.off(signal.channels[0])
    sleep(4.9)

signal.clean()
