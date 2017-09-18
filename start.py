import numpy as np
import def_baggage_666 as db6
import ana_openCV as mf

input_path = '/Users/zhenghao/Desktop/Chew_threshold_ana/idea/yuqingpeng/test'

# 输入要分析的像素范围
# 软件截图后, 在'预览'中打开并圈出对应区域的两个顶点
# 例如:
# 284 442 ->268 441
# 新视频: 左上角: 450->384
# ced视频+5, VR视频+3
hang = 380
lie = 367
rectangle_scope = np.array([hang,(hang+5),lie,(lie+20)]) # 分析旧视频
mf.pixel_record_2(input_path, rectangle_scope, video_form = 'mov', threshold_condition = 0.9, figure_condition_save = 'False')# 新视频
#NB pixel_record_2(input_path, r_s, figure_condition_save = 'False', mode = 'real_time', bolt = 25, threshold_condition = 0.95)
