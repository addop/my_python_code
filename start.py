import numpy as np
import def_baggage_666 as db6
import ana_openCV as mf

input_path = '/Users/zhenghao/Desktop/Chew_threshold_ana/data/video'

# 输入要分析的像素范围
# 软件截图后, 在'预览'中打开并圈出对应区域的两个顶点
# 例如:
# 284 442 ->268 441
# 新视频: 左上角: 450->384
# ced视频+5, VR视频+3
rectangle_scope = np.array([377,377+3,361,361+20]) # 分析旧视频
mf.pixel_record_2(input_path, rectangle_scope, threshold_condition = 0.8, figure_condition_save = 'True')# 新视频
#NB pixel_record_2(input_path, r_s, figure_condition_save = 'False', mode = 'real_time', bolt = 25, threshold_condition = 0.95)
