from tqdm import tqdm
import numpy as np
import pandas as pd
import baggage_script as bs
import matplotlib.pyplot as plt

# 将data_ave_result 中的数据绘图

filePath = '/Users/zhenghao/Documents/pythonfile/my_python_code/CED/data_ave_result.csv'
data = np.loadtxt(filePath,dtype=np.float,delimiter=',')


y_list = [1,2,4,5]
yerr_list = [7,8,10,11]

x = data[:,0]
plt.figure(figsize=(8,5))
for index in range(4):
    y = data[:,y_list[index]]
    yerr = data[:,yerr_list[index]]

    plt.errorbar(x,y,yerr=yerr)

filename = 'test.png'
plt.savefig(filename, dpi = 300, bbox_inches = 'tight')
