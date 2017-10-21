from tqdm import tqdm
import numpy as np
import pandas as pd
import baggage_script as bs
import painting_20171017

# 数据结构说明:1为采样点, 2为电流源通道, 3为CH1, 4为CH2
# LED1点亮4次, LED2点亮4次, 只统计前8次
# 每组数据理应有100个点

# 参数
fanwei1 = [9]# ib
# fanwei1 = [1,2,3,4,5,6,7,8,9]# ib
fanwei2 = [2]# ia

# 将文件夹中所有txt循环一遍


for ia in tqdm(fanwei2):
    Area_List = []
    for ib in fanwei1:
        filePath_T = '/Users/zhenghao/Desktop/ANA_token/data_20171011/171011_C{}_{}.txt'.format(ia, ib)
        filename = 'AllPic_C{}_{}_1_small.png'.format(ia, ib)
        filename_single = 'single_C{}_{}.eps'.format(ia, ib)
        filename_bar = 'bar_C{}_{}.png'.format(ia, ib)
        data = bs.txt_read_pandas(filePath_T)# 获取数据
        data[:,2] = data[:,2]# 将数据方向改变
        # print(np.shape(data))
        list_token = bs.data_raise(data,column = 1, threshold = 2, delay = 3)# 获取dataraise

        # 获取Area
        Area = []
        for index in range(8):
            Area_token = bs.GetTheArea(data, list_token_item=list_token[index], column=2,after=250-50)
            Area.append(Area_token)
        for index in range(8):
            Area_token = bs.GetTheArea(data, list_token_item=list_token[index], column=3,after=250-50)
            Area.append(Area_token)

        Area_List.append(Area)


        # bs.painting_all(data,list_token,filename,column = 2,ylim=[-1.5,1.5])# 批量绘图

        bs.painting(data,list_token,filename_single,r_s = [0,4,4,8],title=filename_single,ylim=[-13,12],after = int(500))
        print('图像绘制完毕')
    # Area_array = np.array(Area_List)
    # bs.save2csv(data=Area_array, filename='Volt_jump_result.csv')
    # painting_20171017.painting_errorbar(ia)
print('\a')
