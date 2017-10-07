# 将txt读取
from tqdm import tqdm
import numpy as np
import pandas as pd
import baggage_script as bs


def result_csv_got(filePath, fanwei):
    # 收集结果
    data_bag = []
    for i in tqdm(range(fanwei[0],fanwei[1])):
        filePath_T = filePath%i
        data = bs.txt_read_pandas(filePath_T)
        list_token = bs.data_raise(data,column = 1, threshold = 0.2, delay = 0.25)
        for item in list_token:
            data_bag.append(data[item-100:item+300, :])
        bs.painting_test(data,list_token,'test.png')
    return(data_bag)
    print('\a')

def text_save_fnda(data,filename):
    token = np.array(data)
    np.savetxt(filename, token)
    return()

filePath = '/Users/zhenghao/Desktop/ANA_token/data_20170930/179300%d.txt'
fanwei = [51,52]
data = result_csv_got(filePath, fanwei)
print(len(data))
text_save_fnda(data, 'test.npy')
