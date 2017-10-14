from tqdm import tqdm
import numpy as np
import pandas as pd
import baggage_script as bs

# 数据结构说明:1为采样点, 2为电流源通道, 3为CH1, 4为CH2

# 参数
filePath = '/Users/zhenghao/Desktop/ANA_token/data_20171011/17o1100%d.txt'
fanwei = [7]
filename = 'AllPic_%d_1_small.png'
filename_single = 'single_%d.png'
filename_bar = 'bar_%d.png'
# 将文件夹中所有txt循环一遍

Area_List = []
for i in tqdm(fanwei):
    filePath_T = filePath%i
    data = bs.txt_read_pandas(filePath_T)# 获取数据
    data[:,2] = data[:,2]# 将数据方向改变
    # print(np.shape(data))
    list_token = bs.data_raise(data,column = 1, threshold = 2, delay = 3)# 获取dataraise

    # 获得最大的ylim:
    ylimup = []
    for item in list_token:
        ylimup.append(max(data[item+10:item+150,3]))
    token = max(ylimup)+5

    # 获取Area
    Area = []
    for index in range(12):
        Area_token = bs.GetTheArea(data, list_token_item=list_token[index], column=2)
        Area.append(Area_token)
    for index in range(12):
        Area_token = bs.GetTheArea(data, list_token_item=list_token[index], column=3)
        Area.append(Area_token)
    # print('len Area: ',len(Area))
    # print('Area data: ', Area)

    # average
    # data_LED1 = np.mean(Area[0:4])
    # data_LED2 = np.mean(Area[4:8])
    # data_LEDALL = np.mean(Area[8:12])

    # filename_bar_T = 'bar_{}_{}.png'.format(i, 'LED1')# 两个变量控制命名
    # bs.painting_bar(data1=Area[0:4], data2=Area[12:16], filename = filename_bar_T)
    # filename_bar_T = 'bar_{}_{}.png'.format(i, 'LED2')# 两个变量控制命名
    # bs.painting_bar(data1=Area[4:8], data2=Area[16:20], filename = filename_bar_T)
    # filename_bar_T = 'bar_{}_{}.png'.format(i, 'LEDAll')# 两个变量控制命名
    # bs.painting_bar(data1=Area[8:12], data2=Area[20:24], filename = filename_bar_T)

    # print(token)
    # print('yes')
    # filename_T = filename%i# 自动图片命名
    # bs.painting_all(data,list_token,filename_T,column = 1,ylim=[-1.5,1.5])# 批量绘图

    # filename_single_T = filename_single%i
    # bs.painting(data,list_token,filename_single_T,r_s = [0,4,4,8],title=filename_single_T,ylim=[-10,10])
print('\a')
