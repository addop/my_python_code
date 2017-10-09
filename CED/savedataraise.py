from tqdm import tqdm
import numpy as np
import pandas as pd
import baggage_script as bs

# 批量导出所有全视图和每个dataraise对应的CSV
filePath = '/Users/zhenghao/Desktop/ANA_token/data_20170930/179300%d.txt'
fanwei = [22,64]
filename = '1AllPic%d1_small.png'
for i in tqdm(range(fanwei[0],fanwei[1])):
    filePath_T = filePath%i
    data = bs.txt_read_pandas(filePath_T)# 获取数据
    list_token = bs.data_raise(data,column = 1, threshold = 0.2, delay = 0.25)# 获取dataraise
    filename_T = filename%i# 自动图片命名
    bs.painting_all(data,list_token,filename_T,column = 1,ylim=[-1.5,1.5])# 批量绘图
    for index in tqdm(range(len(list_token))):
        item = list_token[index]
        raisedata = data[item-50:item+150,:]
        filename_csv = '{}_{}.csv'.format(i, index)# 两个变量控制命名
        bs.save2csv(raisedata,filename_csv)
print('\a')
