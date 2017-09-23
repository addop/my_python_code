import numpy as np
import def_baggage_666 as db6
import ana_openCV as mf
import pandas as pd
import csv

input_path = '/Users/zhenghao/Desktop/yuqingpeng/idea/yuqingpeng_2/video_demo/20170905/1-1'

有多少行 = 398
有几个列 = 642
多大的正方形 = 3
rectangle_scope_token = np.array([有多少行,(有多少行+多大的正方形),有几个列,(有几个列+多大的正方形)]) # 分析旧视频

LED点亮行 = 293
LED点亮列 = 225
LED_scope_token = np.array([LED点亮行,(LED点亮行+2),LED点亮列,(LED点亮列+2)])

grating探测行 = 74
grating探测列 = 169
grating_detect_token = np.array([grating探测行,(grating探测行+2),grating探测列,(grating探测列+2)])
# 进行分析
mf.pixel_record_2(input_path, r_s = rectangle_scope_token, grating_detect = grating_detect_token, LED_scope = LED_scope_token, video_form = 'mpg', figure_condition_save = 'False', start_video = 'True', ana_frame_num = 'All', video_mode = 'CED')# 新视频
print ('\a'*7) # 程序完结后发出声音
# pixel_record_2(input_path, r_s, figure_condition_save = 'False', mode = 'real_time', bolt = 25, threshold_condition = 0.95, video_mode = 'CED')
