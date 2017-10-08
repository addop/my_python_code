from tqdm import tqdm
import numpy as np
import pandas as pd
import baggage_script as bs

# 将数据图全部绘制完毕
# 之后通过肉眼进行筛选

# 参数
filePath = '/Users/zhenghao/Desktop/ANA_token/data_20170930/179300%d.txt'
fanwei = [51,52]
filename = 'AllPic%d1_small.png'
# 将文件夹中所有txt循环一遍
for i in tqdm(range(fanwei[0],fanwei[1])):
    filePath_T = filePath%i
    data = bs.txt_read_pandas(filePath_T)# 获取数据

    list_token = bs.data_raise(data,column = 1, threshold = 0.2, delay = 0.25)# 获取dataraise
    filename_T = filename%i# 自动图片命名
    # bs.painting_all(data,list_token,filename_T,column = 1,ylim=[-0.5,0.5])# 批量绘图
    bs.painting(data,list_token,'filename.png',r_s = [0,4,4,8],title='2ms 3.5V All',ylim=[-1.5,1.5])
print('\a')
#
# filePath = '/Users/zhenghao/Desktop/ANA_token/data_20170930/179300%d.txt'
# fanwei = [22,23]
# filename = 'AllPic%d2_small.png'
# # 将文件夹中所有txt循环一遍
# for i in tqdm(range(fanwei[0],fanwei[1])):
#     filePath_T = filePath%i
#     data = bs.txt_read_pandas(filePath_T)# 获取数据
#
#     list_token = bs.data_raise(data,column = 2, threshold = 0.2, delay = 0.25)# 获取dataraise
#     filename_T = filename%i# 自动图片命名
#     bs.painting_all(data,list_token,filename_T,column = 2)# 批量绘图
# print('\a')
