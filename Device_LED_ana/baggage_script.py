# baggage
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import urllib
from pyheatmap.heatmap import HeatMap

def txt_read_pandas(filePath):
    data = pd.read_table(filePath)
    data_A = np.array(data)
    return(data_A)

def data_raise_down(data, column, threshold = 0.2, delay = 0.25, sample_F = 30000):#delay = 0.25是ok的
    # delay的值我通过观察spike2的结果得出, 初步检测能够使用
    count_token = 0 # 计数
    index_list = []
    for index in tqdm(range(int(len(data)-1))):
        if data[index, column] != 'NaN':
            if data[index, column] < threshold or data[index, column] > -threshold-0.1:
                if data[index+1, column] >= threshold or data[index+1, column] <= -threshold-0.1:
                    count_token = count_token + 1
                    index_list.append(index)
    # print('第',column,'列的数据中 data_raise 的个数为: ', count_token)
    # print('data_raise 时刻列表为: ', index_list)
    index_list_del = []
    index_list_del.append(index_list[0]) # 将index_list第一个值传递给index_list_del
    while len(index_list) > 0:
        item = index_list.pop(0)# 把index_list一个个pop出来, 给item
        # print(item)
        if item - index_list_del[-1] > delay*sample_F:
            index_list_del.append(item)
    # print('增加delay后, data_raise 时刻列表为: ', index_list_del)
    return(index_list_del)

def data_raise(data, column, threshold = 0.2, delay = 0.25):#delay = 0.25是ok的
    # delay的值我通过观察spike2的结果得出, 初步检测能够使用
    count_token = 0 # 计数
    index_list = []
    for index in tqdm(range(int(len(data)-1))):
        if data[index, column] != 'NaN':
            if data[index, column] < threshold:
                if data[index+1, column] >= threshold:
                    count_token = count_token + 1
                    index_list.append(index)
    # print('第',column,'列的数据中 data_raise 的个数为: ', count_token)
    # print('data_raise 时刻列表为: ', index_list)
    index_list_del = []
    index_list_del.append(index_list[0]) # 将index_list第一个值传递给index_list_del
    while len(index_list) > 0:
        item = index_list.pop(0)# 把index_list一个个pop出来, 给item
        # print(item)
        if item - index_list_del[-1] > delay*30000:
            index_list_del.append(item)
    # print('增加delay后, data_raise 时刻列表为: ', index_list_del)
    return(index_list_del)

# 不同肌肉, 相同电压, 绘制在一起
def painting(data,list_token,filename,r_s,title,ylim, after=150):
    # NOTE: 绘图主函数
    plt.figure(figsize=(10,3))# figsize不能过大, 想要清楚就去改dpi

    for index in range(r_s[0],r_s[1]):
        a = list_token[index]
        plt.plot(data[a-50:a+after, 2], 'red', label = str(a))#label = str(a)
        # plt.plot(data[a-100:a+300, 2], 'red', label = str(a))

    for index in range(r_s[0],r_s[1]):
        a = list_token[index]
        # plt.plot(data[a-100:a+300, 1], 'black', label = str(a))
        plt.plot(data[a-50:a+after, 3], 'green', label = str(a))

    for index in range(r_s[2],r_s[3]):
        a = list_token[index]
        plt.plot(data[a-50:a+after, 2], 'yellow', label = str(a))
        # plt.plot(data[a-100:a+300, 2], 'red', label = str(a))

    for index in range(r_s[2],r_s[3]):
        a = list_token[index]
        # plt.plot(data[a-100:a+300, 1], 'black', label = str(a))
        plt.plot(data[a-50:a+after, 3], 'black', label = str(a))


    plt.legend()
    # plt.xticks([0,50,100,150,200], ('-5','0','5','10','15'))
    plt.ylim(ylim[0],ylim[1])
    plt.title(title)
    plt.xlabel('point(10kHz/s)')
    plt.ylabel('Volt(mV)')
    plt.savefig(filename, dpi = 300, bbox_inches = 'tight')
    return()

def painting_test(data,list_token,filename):
    #NOTE: 将一个txt结果完整绘图出来, 方便人工分析出位置
    # 我需要一个数据输入, 然后算出的结果输入
    plt.figure(figsize=(30,3))

    # 将list_token中的点在data中设置为1
    data_token = [0 for _ in range(len(data[:,0]))] # 快速建立全0的列表
    for item in list_token:
        data_token[item+5] = 0.5 # 方便图片观察, 将二者错开

    plt.plot(data[:,1], 'gray')
    plt.plot(np.array(data_token)+0.3, 'red')#让y的数值上下移动, 需要做array化
    plt.ylim(-0.5,0.5)
    plt.title('Token')
    plt.xlabel('10K Hz')
    plt.ylabel('mV')
    plt.savefig(filename, dpi = 300, bbox_inches = 'tight')
    return()

def painting_all(data,list_token,filename,column,ylim):# ok
    # NOTE:
    # 先画出一个全局的图片, 然后向下依次画出dataraise点的前后距离的图, 需要新建的画布的尺寸可由程序自动控制
    # [-]y轴范围可由数据自动控制, 取dataraise后25~200之间最大的值, 设置为最终的y值

    # 将list_token中的点在data中设置确定的值
    data_token = [0 for _ in range(len(data[:,0]))] # 快速建立全0的列表
    for item in list_token:
        data_token[item+5] = 0.5 # 方便图片观察, 将二者错开

    # 确定图片尺寸
    plt.figure(figsize=(20,3*len(list_token)))#30,3

    # 设置当前绘图位置
    # 图片构成, 需要len(list_token)+1的个数
    plt.subplot(len(list_token)+1,1,1)

    # 绘制数据结果
    plt.plot(data[:,1], 'gray')
    # 绘制dataraise结果
    plt.plot(np.array(data_token)+0.3, 'red')#让y的数值上下移动, 需要做array化
    # 确定此图片的参数
    plt.ylim(ylim[0],ylim[1])
    # plt.title('')


    # for循环绘制接下来的情况
    for index in range(len(list_token)):
        # 确定绘制位置
        plt.subplot(len(list_token)+1,1,index+2)
        a = list_token[index]
        plt.plot(data[a-50:a+150, column], 'blue', label = str(a))# 100, 300
        plt.ylim(-1.5,1.5)

    plt.subplots_adjust(hspace = 0)# 设置区块之间距离
    plt.savefig(filename, dpi = 300, bbox_inches = 'tight')# 保存图片

    return()

def painting_bar(data1, data2, filename):
    plt.figure(figsize = (8,5))
    plt.plot(data1,'o')
    plt.plot(data2,'*')
    plt.xlabel('x')
    plt.ylabel('mV * ms')
    plt.savefig(filename, dpi = 300, bbox_inches = 'tight')

def save2csv(data, filename):# ok
    np.savetxt(filename, data, delimiter=',')# header可能存在问题导致之后没有办法自动分列, header可能没有问题, 问题在双重矩阵

def readcsv2pic(filePathList, filename):
    for item in filePathList:
        data = pd.read_csv(item, names = ['sampling_spot','gastrocnemius','tibialis anterior'])# names很好
    return()

def GetTheArea(data, list_token_item, column,after=1000-50):
    # 函数很棒, 经过了许多测试, 能够完美工作
    # 输入参数说明:
    # data: 原始数据
    # list_token_item: list_token中的item, 是给光刺激的时刻
    # column: data中需要分析的column


    data_target = data[list_token_item-50:list_token_item+after,column]# 刺激后4s内都要算进去,(4*10000-50)
    # 取基线的值
    data_base = np.mean(data_target[:45])
    # 将数据基线拉到0
    data_zero = data_target - data_base
    # 对数据求绝对值, 使最终面积都为正
    data_abs = np.abs(data_zero)
    Area = np.sum(data_abs[50:])*0.1# 这里0.1是以毫秒为单位, 1ms是10个采样点, 采样点间间隔0.1ms
    return(Area)

def Sort_Channel(sum_array):
    # 给data排序, data要是一个一维数组, 维度为6
    List_token = [15,16,14,7,13,6,12,5,11,4,10,3,9,2,8,1]
    data_sort = np.empty([16,16])
    for index in range(16):
        R = List_token[index]
        data_sort[:,index]=sum_array[:,R-1]
    print(data_sort)
    return(data_sort)


def data_derection(data_sort_A):
    # 求方向
    # 将一个矩阵输入转化为矩阵输出
    # 四个电压的刺激, 每个电压刺激四次
    direction_x = np.array([-2,-1,1,2,-2,-1,1,2,-2,-1,1,2,-2,-1,1,2])
    direction_y = np.array([2,2,2,2,1,1,1,1,-1,-1,-1,-1,-2,-2,-2,-2])
    d=[]
    for i in range(4):
        a = np.sum(data_sort_A[i,:]*direction_x)
        b = np.sum(data_sort_A[i,:]*direction_y)
        c.append([a,b])
    f=np.array(c)
    # print(f)
    return(f)


def firing_sum(data, index_list_del):
    # count the times of firing
    sum_list=[]
    for index_1 in index_list_del:
        raw_token = []
        for i_1 in range(1,17):
            raw_token.append(np.sum(data[index_1:index_1+30000,i_1]))
        sum_list.append(raw_token)
        sum_array = np.array(sum_list)
        sum_array[:,0] = 0
    return(sum_array)