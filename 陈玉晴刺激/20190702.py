import serial as sr
# https://pyserial.readthedocs.io/en/latest/pyserial_api.html

# import numpy as np
# import matplotlib.pyplot as plt
# from tqdm import tqdm
import time
# import traceback # 处理异常
import random


def get_time_now():
    # 获取时间
    tag = time.localtime()
    # 将时间作为文件夹名称
    input_path = str(tag.tm_year) + '-' + str(tag.tm_mon) + '-' + \
                 str(tag.tm_mday) + '_' + str(tag.tm_hour) + 'H' + \
                 str(tag.tm_min) + 'M'
    return input_path


class SerialPort:
    def __init__(self, port_path):
        self.port_path = None
        self.port = None
        self.port_state = None
        self.info_send = None
        self.info_get = None
        self.info_send_state = None
        self.info_get_state = None
        self.state = None
        self.log = None

        self.port_path = port_path
        self.log = ['start']

    def open_port(self):
        self.port = sr.Serial(port=self.port_path, baudrate=9600)
        # self.port.open()
        if self.port.is_open:
            self.port_state = True

    def send_info(self, info):
        self.info_send = info
        self.info_send_state = False
        self.port.write(self.info_send)
        time_now = get_time_now()
        self.log.append(time_now)
        self.log.append(self.info_send)
        self.info_send_state = True


path = '/dev/cu.usbmodem144301'
my_port = SerialPort(port_path=path)
my_port.open_port()


# 数据发送
send_state = input('输入刺激模式:(0或1)')

if send_state == '0':

    # 随机
    num_add = 0
    num_box = []
    while num_add < 120:  # 100-8
        num_box.append(random.uniform(10, 14))
        num_add = sum(num_box)
    print(num_box)

    for i in num_box:
        my_port.send_info(b'H')
        print(i)
        time.sleep(i)

if send_state == '1':
    random_count = 0
    while random_count <= 3:
        random_count += 1
        # 随机
        num_add = 0
        num_box = []
        while num_add < 173:  # 100-8
            num_box.append(random.uniform(7, 11))
            num_add = sum(num_box)
        print(num_box)

        for i in num_box:
            my_port.send_info(b'H')
            print(i)
            time.sleep(i)
        time.sleep(1*10)
    # 1s-4s 20次, 10组, 间隔1分钟
    random_count = 0
    while random_count <= 10:
        random_count += 1
        pulse_count = 0
        while pulse_count <= 20:
            pulse_count += 1
            my_port.send_info(b'H')
            print(pulse_count)
            time.sleep(5)
        time.sleep(1*10)


my_port.state = 'finished'
my_port.port.close()
print(my_port.log)
print(my_port.port_state)
