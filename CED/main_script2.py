from tqdm import tqdm
import numpy as np
import pandas as pd
import baggage_script as bs

# 将数据图全部绘制完毕
# 之后通过肉眼进行筛选

# 参数
filePath = '/Users/zhenghao/Desktop/ANA_token/data_20170930/179300%d.txt'
fanwei = [22,64]
filename = 'AllPic%d1.eps'
# 将文件夹中所有txt循环一遍
for i in tqdm(range(fanwei[0],fanwei[1])):
    filePath_T = filePath%i
    data = bs.txt_read_pandas(filePath_T)# 获取数据

    list_token = bs.data_raise(data,column = 1, threshold = 0.2, delay = 0.25)# 获取dataraise
    filename_T = filename%i# 自动图片命名
    bs.painting_all(data,list_token,filename_T)# 批量绘图

print('\a')

filePath = '/Users/zhenghao/Desktop/ANA_token/data_20170930/179300%d.txt'
fanwei = [22,64]
filename = 'AllPic%d2.eps'
# 将文件夹中所有txt循环一遍
for i in tqdm(range(fanwei[0],fanwei[1])):
    filePath_T = filePath%i
    data = bs.txt_read_pandas(filePath_T)# 获取数据

    list_token = bs.data_raise(data,column = 2, threshold = 0.2, delay = 0.25)# 获取dataraise
    filename_T = filename%i# 自动图片命名
    bs.painting_all(data,list_token,filename_T)# 批量绘图

print('\a')
