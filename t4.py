# 主脚本
import numpy as np
import def_baggage_666 as db6
import main_function as mf

input_path = '/Users/zhenghao/Desktop/Chew_threshold_ana/idea/yuqingpeng/video'

# 输入要分析的像素范围
# 软件截图后, 在'预览'中打开并圈出对应区域的两个顶点
# 例如:
# 285 439 -> 282 445 -> 284 442 ->268 441
# rectangle_scope = np.array([442,443,284,285])
rectangle_scope = np.array([441,442,267,268])

# 测试: 光遗传激活判断
# 判断结果ok, 保存ok
# rectangle_scope = np.array([390,391,225,226])


m_frame = mf.pixel_record_666(input_path, rectangle_scope)


# [x] 需要找到范围判定
# REVIEW 笔记:
# 自动寻找每组阈值的idea:
# 1) 确定向下一段距离一定是光栅的区域, 找到像素点位置
# 2) 采样这个像素点, 取它的最小值的80%作为阈值
# 3) 90%是我拍脑袋想出来的

# 调用def_baggage_666中的函数, 将老大哥的数据导入, 生成01的表格
eye_data_filePath = '/Users/zhenghao/Desktop/Chew_threshold_ana/idea/yuqingpeng/03.csv'
eye_data_nda = db6.eye_csv_read(eye_data_filePath, m_frame)
db6.painting_trees(eye_data_nda[:,1],'result_eye.eps')
