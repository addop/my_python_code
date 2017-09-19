import numpy as np
import def_baggage_666 as db6
import ana_openCV as mf

input_path = '/Users/zhenghao/Desktop/Chew_threshold_ana/idea/yuqingpeng_2/video/20170830/1-2'

# 输入要分析的像素范围
# 软件截图后, 在'预览'中打开并圈出对应区域的两个顶点
# 例如:
# 284 442 ->268 441
# 新视频: 左上角: 450->384
# ced视频+5, VR视频+3

# 视频参数调节

有多少行 = 444
有几个列 = 591
多大的正方形 = 5
试验台是CED还是VR = 'CED'

rectangle_scope = np.array([有多少行,(有多少行+多大的正方形),有几个列,(有几个列+多大的正方形)]) # 分析旧视频

mf.pixel_record_2(input_path, rectangle_scope, video_form = 'mpg', threshold_condition = 0.9, figure_condition_save = 'True', video_mode = 试验台是CED还是VR)# 新视频

#NB pixel_record_2(input_path, r_s, figure_condition_save = 'False', mode = 'real_time', bolt = 25, threshold_condition = 0.95, video_mode = 'CED')
