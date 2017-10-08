from tqdm import tqdm
import numpy as np
import pandas as pd
import baggage_script as bs

filePath = '/Users/zhenghao/Desktop/ANA_token/data_20170930/179300%d.txt'
fanwei = [60,61]
filename = 'AllPic%d1_small.png'
# 将文件夹中所有txt循环一遍
for i in tqdm(range(fanwei[0],fanwei[1])):
    filePath_T = filePath%i
    data = bs.txt_read_pandas(filePath_T)# 获取数据

    list_token = bs.data_raise(data,column = 1, threshold = 0.2, delay = 0.25)# 获取dataraise
    filename_T = filename%i# 自动图片命名
    bs.painting_all(data,list_token,filename_T,column = 1,ylim=[-1.5,1.5])# 批量绘图

    for item in list_token:
        raisedata = data[item-50:item+150,:]
        bs.save2csv(raisedata,filename_csv)

print('\a')
