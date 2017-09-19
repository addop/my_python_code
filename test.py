import cv2
import os
import sys
import numpy as np
from tqdm import tqdm
import copy
import pandas as pd
import random

import def_baggage_666 as db6
input_path = '/Users/zhenghao/Desktop/Chew_threshold_ana/idea/yuqingpeng/test'
video_form = 'mpg'
filenames = os.listdir(input_path)
video_prefix = input_path.split(os.sep)[-1]
frame_path = '{}_LEDon'.format(input_path)
if not os.path.exists(frame_path):
    os.mkdir(frame_path)
cap = cv2.VideoCapture()
filename = filenames[1]

token = 0

print(filename)
for filename in tqdm(filenames):
    print('filename is: ', filename)
    if filename == '.DS_Store':
        continue
    if filename.split('.')[1] == video_form:
        filepath = os.sep.join([input_path, filename])
        # VideoCapture::open函数可以从文件获取视频
        cap.open(filepath)
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        for i in tqdm(range(int(n_frames/10))):
            nap, frame = cap.read()
            shape_frame = np.shape(frame)
            if nap == True:
                # 在frame中识别第一个面是否小于和第二个面大于
                # [ ]如何把一个矩阵从1920*1080*3
                # 利用乘法
                frame_after = frame[:,:,0]*frame[:,:,2]
                if True in frame_after:
                    token = token + 1
                    # break
                # 判断具体是哪个区域大于240, 取最中间的那个点
                # if [True, True] in frame_blind:
                #     print('我找到了那个点')
                #     imagename = '{}_{}_LEDon.jpg'.format(video_prefix, filename.split('.')[0])
                #     imagepath = os.sep.join([frame_path, imagename])
                #     cv2.imwrite(imagepath, frame)
                            # break
print('亮瞎眼数目: ', token)
cap.release()
