import cv2
import numpy as np
import os
import random
import time
from tqdm import tqdm


class movie_cutter:
    def __init__(self, filepath, savepath):
        self.movie_name = None
        self.material_name_box = []
        self.material_choose_box = []
        self.material_filepath = filepath
        self.material_pool = []
        self.log = filepath.split('/')[-1]
        self.time = None

        TAG = time.localtime()
        self.time = str(TAG.tm_mon) + '-' + \
                    str(TAG.tm_mday) + '_' + \
                    str(TAG.tm_hour) + 'H' + \
                    str(TAG.tm_min) + 'M' + \
                    str(TAG.tm_sec) + 'S'
        self.movie_name = savepath+filepath.split('/')[-1]+self.time+'.mp4'

        self.black_pic = np.ones((540, 960, 3), np.uint8)

    def logging(self, info):
        self.log = self.log + info

    def get_material_pool(self):
        """
        获取需要的素材

        随机选择40个素材, 每个素材3秒钟, 停顿时间3秒钟.

        - [X] 打开文件夹, 获取文件名, 核验
        - [X] 随机选取入盒子中
        - [X] 读取每一个视频, 做长度限定
        - [X] 结果保存在一个矩阵或列表中
        :return: 返回列表或矩阵
        """
        file_box = os.listdir(self.material_filepath)
        for item in file_box:
            if item.split('.')[0] == '' or item.split('.')[-1] != 'mp4': # 这里不能用is not
                continue
            self.material_name_box.append(item)
        self.logging('--choose_file')

        index_token = [random.randint(0, len(self.material_name_box)-1) for i in range(40)]
        for index in index_token:
            self.material_choose_box.append(self.material_name_box[index])
        self.logging('--random_file')

        cap = cv2.VideoCapture()


        for material_choose in self.material_choose_box:
            cap.open(self.material_filepath + '/' + material_choose)
            frame_box_token = []
            for n_frame in range(75):
                nap, frame = cap.read()
                frame_box_token.append(frame)
            self.logging('--' + material_choose.split('.')[0])
            self.material_pool.append(frame_box_token)

        pass

    def merging(self):
        """
        将内参self.material_pool中的矩阵读取出来并合成成一个新的视频

        - [X] 循环读取内参内容
        - [X] 循环每帧, 写入视频
        :return: 保存在桌面的视频
        """
        frame_count = 0 # 设立一个对总帧数做计数的参数
        print('视频个数: ', len(self.material_pool))

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(self.movie_name, fourcc, 25.0, (960, 540))

        for item_first_floor in tqdm(self.material_pool):
            [out.write(self.black_pic) for i in range(75)] # 黑色背景插入
            for item_second_floor in item_first_floor:
                out.write(item_second_floor)
                frame_count += 1
        out.release()  # 导出视频时释放
        self.logging('--video_saved')
        self.logging('frame_count-'+str(frame_count))
        print(np.shape(item_second_floor))

    def log_saving(self):
        with open(self.movie_name+'.txt', 'w') as fileobject:  # 使用‘w’来提醒python用写入的方式打开
            fileobject.write(self.log)


savepath = '/Users/zhenghao/Desktop/'
filepath = '/Volumes/HaoZHD4/hospitalData/病人刺激视频/实验视频/SEEG_stim_video'
my_dog = movie_cutter(filepath, savepath)
my_dog.get_material_pool()
my_dog.merging()
my_dog.log_saving()
# print(my_dog.log)