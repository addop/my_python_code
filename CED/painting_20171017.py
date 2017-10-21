
# coding: utf-8

# In[1]:


from tqdm import tqdm
import numpy as np
import pandas as pd
import baggage_script as bs
import matplotlib.pyplot as plt


# In[5]:
def painting_errorbar(ia):

    filePath = '/Users/zhenghao/Documents/pythonfile/my_python_code/CED/Volt_jump_result.csv'
    data = np.loadtxt(filePath,dtype=np.float,delimiter=',')
    # print(np.shape(data))
    data_num = 3

    # In[19]:


    # 求mean
    data_mean = []
    for i in range(20):
        raw_mean = []
        for raw in range(data_num):
            item_mean = np.mean(data[raw,i*10:i*10+10])# item_mean = np.mean(data[raw,i*10:i*10+10])
            raw_mean.append(item_mean)
        data_mean.append(raw_mean)
    # print(data_mean)


    # In[20]:


    # 求sem
    data_sem=[]
    for i in range(20):
        raw_sem=[]
        for raw in range(data_num):
            item_raw=np.std(data[raw,i*10:i*10+10])
            #item_raw=item_raw/(10**0.5)
            raw_sem.append(item_raw)
        data_sem.append(raw_sem)
    # print(data_sem)


    # In[26]:


    # 绘图
    data_mean=np.array(data_mean)
    data_sem=np.array(data_sem)

    plt.figure(figsize=(8,5))

    x = np.array([3.5,3.4,3.3,3.2,3.1,3.0,2.9,2.8,2.7,2.6])

    y = data_mean[0:10,1]
    yerr = data_sem[0:10,1]
    plt.errorbar(x,y,yerr=yerr,label = 'tibialis anterior muscle-LED1')
    y = data_mean[0:10,2]
    yerr = data_sem[0:10,2]
    plt.errorbar(x,y,yerr=yerr,label = 'tibialis anterior muscle-LED2')

    y = data_mean[10:20,1]
    yerr = data_sem[10:20,1]
    plt.errorbar(x,y,yerr=yerr,label = 'gastrocnemius muscle-LED1')
    y = data_mean[10:20,2]
    yerr = data_sem[10:20,2]
    plt.errorbar(x,y,yerr=yerr,label = 'gastrocnemius muscle-LED2')

    filename = '20171018_C{}_Result.png'.format(ia)
    plt.legend()
    plt.title(filename)
    plt.xlabel('Volt(V)')
    plt.ylabel('Area(mV*ms)')
    plt.savefig(filename, dpi = 300, bbox_inches = 'tight')
    return()


def painting_errorbar_101711(ia, data_num=9):

    filePath = '/Users/zhenghao/Documents/pythonfile/my_python_code/CED/Volt_jump_result.csv'
    data = np.loadtxt(filePath,dtype=np.float,delimiter=',')
    # print(np.shape(data))

    # In[19]:


    # 求mean
    data_mean = []
    for i in range(4):
        raw_mean = []
        for raw in range(data_num):
            item_mean = np.mean(data[raw,i*4:i*4+4])# item_mean = np.mean(data[raw,i*10:i*10+10])
            raw_mean.append(item_mean)
        data_mean.append(raw_mean)
    # print(data_mean)


    # In[20]:


    # 求sem
    data_sem=[]
    for i in range(4):
        raw_sem=[]
        for raw in range(data_num):
            item_raw=np.std(data[raw,i*4:i*4+4])
            #item_raw=item_raw/(10**0.5)
            raw_sem.append(item_raw)
        data_sem.append(raw_sem)
    # print(data_sem)


    # In[26]:


    # 绘图
    data_mean=np.array(data_mean)
    data_sem=np.array(data_sem)

    plt.figure(figsize=(8,5))

    x = np.array([3.5,3.4,3.3,3.2,3.1,3.0,2.9,2.8,2.7,2.6])

    y = data_mean[0:10,1]
    yerr = data_sem[0:10,1]
    plt.errorbar(x,y,yerr=yerr,label = 'tibialis anterior muscle-LED1')
    y = data_mean[0:10,2]
    yerr = data_sem[0:10,2]
    plt.errorbar(x,y,yerr=yerr,label = 'tibialis anterior muscle-LED2')

    y = data_mean[10:20,1]
    yerr = data_sem[10:20,1]
    plt.errorbar(x,y,yerr=yerr,label = 'gastrocnemius muscle-LED1')
    y = data_mean[10:20,2]
    yerr = data_sem[10:20,2]
    plt.errorbar(x,y,yerr=yerr,label = 'gastrocnemius muscle-LED2')

    filename = '20171018_C{}_Result.png'.format(ia)
    plt.legend()
    plt.title(filename)
    plt.xlabel('Volt(V)')
    plt.ylabel('Area(mV*ms)')
    plt.savefig(filename, dpi = 300, bbox_inches = 'tight')
    return()
