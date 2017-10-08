import numpy as np
import def_baggage_666 as db6
import ana_openCV as mf
import pandas as pd
import csv

input_path = '/Users/zhenghao/Desktop/ana_movies'
# 适用于两点分析的Chew, 共同取平均值计算
有多少行_1 = 507
有几个列_1 = 1557
有多少行_2 = 520
有几个列_2 = 1735

rectangle_scope_token = np.array([有多少行_1,(有多少行_1+70),有几个列_1,(有几个列_1+10),有多少行_2,(有多少行_2+70),有几个列_2,(有几个列_2+10)]) # 分析旧视频

LED点亮行 = 293
LED点亮列 = 225
LED_scope_token = np.array([LED点亮行,(LED点亮行+2),LED点亮列,(LED点亮列+2)])

grating探测行 = 74
grating探测列 = 169
grating_detect_token = np.array([grating探测行,(grating探测行+2),grating探测列,(grating探测列+2)])
# 进行分析
mf.pixel_record_2(input_path, r_s = rectangle_scope_token, grating_detect = grating_detect_token, LED_scope = LED_scope_token, video_form = 'mov', figure_condition_save = 'True', start_video = 'False', ana_frame_num = 'All')# 新视频
print ('\a'*7) # 程序完结后发出声音
# pixel_record_2(input_path, r_s, figure_condition_save = 'False', mode = 'real_time', bolt = 25, threshold_condition = 0.95, video_mode = 'CED')
