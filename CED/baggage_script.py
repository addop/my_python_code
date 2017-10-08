# baggage
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

def txt_read_pandas(filePath):
    data = pd.read_table(filePath)
    data_A = np.array(data)
    return(data_A)

def data_raise(data, column, threshold = 0.2, delay = 0.25):#delay = 0.25是ok的
    # delay的值我通过观察spike2的结果得出, 初步检测能够使用
    count_token = 0 # 计数
    index_list = []
    for index in range(int(len(data))):
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
        if item - index_list_del[-1] > delay*10000:
            index_list_del.append(item)
    # print('增加delay后, data_raise 时刻列表为: ', index_list_del)
    return(index_list_del)

def painting(data,list_token,filename):
    # NOTE: 绘图主函数
    plt.figure(figsize=(10,3))# figsize不能过大, 想要清楚就去改dpi
    # 阴性对照
    # for index in range(len(list_token_NAGControl)):
    #     a = list_token_NAGControl[index]
    #     plt.plot(data_NAGControl[a-100:a+300, 1], 'gray', label = str(a))
    #     plt.plot(data_NAGControl[a-100:a+300, 2], 'gray', label = str(a))
    # LED1
    for index in range(3,6):
        a = list_token[index]
        plt.plot(data[a-100:a+300, 1], 'black', label = str(a))
        # plt.plot(data[a-100:a+300, 2], 'red', label = str(a))
    # LED2
    for index in range(6,10):
        a = list_token[index]
        # plt.plot(data[a-100:a+300, 1], 'black', label = str(a))
        plt.plot(data[a-100:a+300, 1], 'red', label = str(a))

    plt.legend()
    plt.xticks([0,100,200,300,400], ('-10','0','10','20','30'))
    # plt.ylim(-1,1)
    plt.title('200ms ')
    plt.xlabel('ms')
    plt.ylabel('mV')
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

def painting_all(data,list_token,filename):
    # NOTE:
    # 先画出一个全局的图片, 然后向下依次画出dataraise点的前后距离的图, 需要新建的画布的尺寸可由程序自动控制
    # [-]y轴范围可由数据自动控制, 取dataraise后25~200之间最大的值, 设置为最终的y值

    # 将list_token中的点在data中设置确定的值
    data_token = [0 for _ in range(len(data[:,0]))] # 快速建立全0的列表
    for item in list_token:
        data_token[item+5] = 0.5 # 方便图片观察, 将二者错开

    # 确定图片尺寸
    plt.figure(figsize=(30,3*len(list_token)))

    # 设置当前绘图位置
    # 图片构成, 需要len(list_token)+1的个数
    plt.subplot(len(list_token)+1,1,1)

    # 绘制数据结果
    plt.plot(data[:,1], 'gray')
    # 绘制dataraise结果
    plt.plot(np.array(data_token)+0.3, 'red')#让y的数值上下移动, 需要做array化
    # 确定此图片的参数
    plt.ylim(-0.5,0.5)
    # plt.title('')


    # for循环绘制接下来的情况
    for index in range(len(list_token)):
        # 确定绘制位置
        plt.subplot(len(list_token)+1,1,index+2)
        a = list_token[index]
        plt.plot(data[a-100:a+300, 1], 'blue', label = str(a))
        plt.ylim(-1,1)

    plt.subplots_adjust(hspace = 0)# 设置区块之间距离
    plt.savefig(filename, dpi = 300, bbox_inches = 'tight')# 保存图片

    return()