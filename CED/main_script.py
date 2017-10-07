# 将txt读取
from tqdm import tqdm
import numpy as np
import pandas as pd
import baggage_script as bs

filePathA = '/Users/zhenghao/Desktop/ANA_token/data_20170930/179300%d.txt'
filePathC = '.txt'
fileName = 'test%d.png'
for i in tqdm(range(51,64)):
    filePath = filePathA%i
    data = bs.txt_read_pandas(filePath)
    list_token = bs.data_raise(data,column = 1)
    bs.painting_test(data,list_token,fileName%i)
# # 阴性对照
# filePath = '/Users/zhenghao/Desktop/ANA_token/data_20171001/17o01003.txt'
# data_NAGControl = bs.txt_read_pandas(filePath)
# list_token_NAGControl = bs.data_raise(data_NAGControl,column = 1)
# print(len(list_token_NAGControl))

# bs.painting_test(data,list_token,'test.png')
print('\a')
