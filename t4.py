#REVIEW 测试
import numpy as np

import main_function as mf

input_path = '/Users/zhenghao/Desktop/Chew_threshold_ana/idea/yuqingpeng/video'

# 输入要分析的像素范围
# 软件截图后, 在'预览'中打开并圈出对应区域的两个顶点
# 例如:
# 285 439 -> 282 445 -> 284 442
rectangle_scope = np.array([442,443,284,285])
rectangle_scope_background = np.array([140,150,268,282])
# [ ] 需要找到范围判定

mf.pixel_record_666(input_path, rectangle_scope, rectangle_scope_background)
