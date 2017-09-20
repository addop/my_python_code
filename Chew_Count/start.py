import numpy as np
import def_baggage_666 as db6
import ana_openCV as mf

input_path = '/Users/zhenghao/Desktop/Chew_threshold_ana/data/video_ana_2'

# 输入要分析的像素范围
# 软件截图后, 在'预览'中打开并圈出对应区域的两个顶点
# 例如:
# 284 442 ->268 441
# 新视频: 左上角: 450->384
# ced视频+5, VR视频+3

# 视频参数调节
# 输入要分析的区域和模式
有多少行 = 435
有几个列 = 332
多大的正方形 = 5
rectangle_scope = np.array([有多少行,(有多少行+多大的正方形),有几个列,(有几个列+多大的正方形*10)]) # 分析旧视频
# 输入LED点亮的区域
# LED点亮行 = 0
# LED点亮列 = 0
# LED_scope = np.array([LED点亮行,(LED点亮行+2),LED点亮列,(LED点亮列+2)])
# 选取分析模式
# 试验台是CED还是VR = 'NaN'

# 进行分析
mf.pixel_record_2(input_path, rectangle_scope, video_form = 'mov', figure_condition_save = 'True', start_video = 'True')# 新视频
print ('\a'*7) # 程序完结后发出声音
#NB pixel_record_2(input_path, r_s, figure_condition_save = 'False', mode = 'real_time', bolt = 25, threshold_condition = 0.95, video_mode = 'CED')
