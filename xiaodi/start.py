import numpy as np
import def_baggage_666 as db6
import ana_openCV as mf
import pandas as pd
import csv

input_path = '/Volumes/HaoZsData/WorkSpace/CodeAnaToken/video_ana'

有多少行 = 354
有几个列 = 302
多大的正方形 = 3
rectangle_scope = np.array([有多少行,(有多少行+多大的正方形),有几个列,(有几个列+多大的正方形)]) # 分析旧视频

LED点亮行 = 293
LED点亮列 = 225
LED_scope = np.array([LED点亮行,(LED点亮行+2),LED点亮列,(LED点亮列+2)])

# 进行分析
mf.pixel_record_2(input_path, rectangle_scope, LED_scope, video_form = 'mpg', figure_condition_save = 'True', start_video = 'False', ana_frame_num = 'All', video_mode = 'VR')# 新视频
print ('\a'*7) # 程序完结后发出声音
# pixel_record_2(input_path, r_s, figure_condition_save = 'False', mode = 'real_time', bolt = 25, threshold_condition = 0.95, video_mode = 'CED')
