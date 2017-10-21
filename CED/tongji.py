
# coding: utf-8

# In[29]:


from tqdm import tqdm
import numpy as np
import pandas as pd
import baggage_script as bs
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from scipy.stats import levene


# In[5]:


filePath = '/Users/zhenghao/Documents/pythonfile/my_python_code/CED/Volt_jump_result.csv'
data = np.loadtxt(filePath,dtype=np.float,delimiter=',')
print('已导入需要分析的csv')


# In[19]:


# 求mean
data_mean = []
for i in range(20):
    raw_mean = []
    for raw in range(3):
        item_mean = np.mean(data[raw,i*10:i*10+10])
        raw_mean.append(item_mean)
    data_mean.append(raw_mean)


# In[20]:


# 求sem
data_sem=[]
for i in range(20):
    raw_sem=[]
    for raw in range(3):
        item_raw=np.std(data[raw,i*10:i*10+10])
        #item_raw=item_raw/(10**0.5)
        raw_sem.append(item_raw)
    data_sem.append(raw_sem)


# In[35]:


# 求ttest
data_ttest = []# 同一个肌肉下, 相同电压下, LED1和LED2的ttest
A=data[0,0:10]
B=data[1,0:10]
[a,b] = ttest_ind(A,B)

for i in range(20):
    [a,item] = ttest_ind(data[0,i*10:i*10+10],data[1,i*10:i*10+10])
    data_ttest.append(item)
print(data_ttest)
