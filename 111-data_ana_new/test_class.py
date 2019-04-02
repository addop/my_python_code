# coding=utf-8
import pandas as pd
import numpy as np
# from tqdm import tqdm
import matplotlib.pyplot as plt
# from scipy import signal
import os
from itertools import product
# import mne
# from scipy.fftpack import fft, ifft
import seaborn as sns
import scipy.stats as stats
from matplotlib.colors import LinearSegmentedColormap
from scipy import signal
# from scipy.fftpack import fft, ifft

from itertools import product

import warnings# 取消warning
warnings.filterwarnings("ignore")


# import cv2


# https://cloud.tencent.com/developer/ask/188729

# 构成:
# 1. 从txt中获得Area的csv
# 2. 改变csv数据结构以适应分析
# 3. 分析
#
# 将读取的csv的这个东西作为一个类, 然后改变结构和分析设置为方法


def baseline_check(data):
    baseline = np.mean(data[:30])
    data_baseline_check = data - baseline
    return (data_baseline_check)


def band_pass(data, bandpass_num=None, sample_freq=10000):
    baseline = np.mean(data)

    # bandpass
    # bandpass_num = [100, 300]  # bandpass范围
    # sample_freq = 10000
    # b, a = signal.butter(1, [(bandpass_num[0] * 2 * 3.14) / sample_freq, (bandpass_num[1] * 2 * 3.14) / sample_freq],
    #                      btype='bandpass', analog=True)
    b, a = signal.butter(1, [(bandpass_num[0] * 2) / sample_freq, (bandpass_num[1] * 2) / sample_freq],
                         btype='bandpass')

    # zi = signal.lfilter_zi(b, a)
    # z, _ = signal.lfilter(b, a, data, zi=zi * data[0])
    # z2, _ = signal.lfilter(b, a, z, zi=zi * z[0])

    y = signal.filtfilt(b, a, data)

    # plt.subplot(2, 1, 1)
    # plt.plot(data, 'r')
    # plt.subplot(2, 1, 2)
    # plt.plot(y, 'b')
    # plt.show()
    return (y)


def get_title_list(data, mode=0):
    '''
    获取数据的一些固定tag的非重复内容

    获取数据的一些固定tag
    :param data: dataframe
    :param mode: 针对不同tag，其中mode=3是指除了第一个Area以外都算进来，适合整理过的数据
    :return: 返回我们查看的tag列表，以及对应的非重复内容
    '''
    title_list = data.columns.values.tolist()
    if mode == 0:
        tag_box = ['LeftOrRight', 'MiceNum', 'ElePosition', 'LedNum', 'OtherTags']
    if mode == 1:
        tag_box = ['LeftOrRight', 'MiceNum', 'ElePosition', 'LedNum', 'OtherTags', 'Muscle']
    if mode == 3:
        tag_box_token = list(data.columns.values)
        tag_box_token.pop(0)
        tag_box = tag_box_token
    def_token = lambda x: data.drop_duplicates(subset=x, keep='first')[x].tolist()
    # 或者可以用这个: muscle = data_alltrials.MuscleName.unique()
    tag_box_list = [def_token(item) for item in tag_box]
    # 将两个列表关联起来，用dict
    # 利用zip函数
    # https://www.cnblogs.com/fh-fendou/p/7515775.html
    tag_box_dict = dict(zip(tag_box, tag_box_list))
    return tag_box, tag_box_list, tag_box_dict


def normalize_data(data_need_normalized):
    # 对一个矩阵进行normalized, 并返回一个矩阵
    data_normalized = data_need_normalized / max(data_need_normalized)
    return data_normalized


class EMG_database:
    # csv数据库的基类(2通道肌电)
    def __init__(self, name, txt_file_path=None, csv_file_path=None, paint_raw=None, signal_scope=None,
                 bandpass_num=None):
        self.name = None
        self.txt_file_path = None
        self.txt = None
        self.csv_file_path = None
        self.csv = None
        self.paint_raw = None
        self.bandpass_num = None

        self.name = name
        self.csv_file_path = csv_file_path
        self.txt_file_path = txt_file_path
        self.paint_raw = paint_raw
        self.signal_scope = signal_scope
        self.bandpass_num = bandpass_num

        print('分析名称:', self.name)
        print('csv路径:', self.csv_file_path)
        print('txt路径:', self.txt_file_path)
        print('绘画叠加:', self.paint_raw)
        print('信号区域 = i ~ i+', self.signal_scope)
        print('bandpass范围:', self.bandpass_num)

        if self.txt_file_path is not None and self.paint_raw is None:
            EMG_database.find_ele_area(self, input_path=self.txt_file_path, bandpass=self.bandpass_num,
                                       signal_scope=self.signal_scope)
        if self.paint_raw is not None:
            EMG_database.paint_raw_data(self, txt_file_path, trail_times=self.paint_raw, bandpass=self.bandpass_num)

        if self.csv_file_path is not None:
            self.csv = pd.read_csv(self.csv_file_path)

        if self.csv is not None:
            print('csv get! ')

    def volt_box_get(self, number):
        volt_number = number

        if volt_number == 310:
            volt_box = []
            for i in range(31):
                for j in range(10):
                    token = (40 + i) * 0.05
                    token = '%.2f' % token
                    volt_box.append(token)

        if volt_number == 186:
            volt_box = []
            for i in range(31):
                for j in range(6):
                    token = (40 + i) * 0.05
                    token = '%.2f' % token
                    volt_box.append(token)

        if volt_number == 126:
            volt_box = []
            for i in range(21):
                for j in range(6):
                    token = (46 + i) * 0.05
                    token = '%.2f' % token
                    volt_box.append(token)

        if volt_number == 24:
            volt_box = []
            for i in range(8):
                for j in range(3):
                    token = (52 + i * 2) * 0.05
                    token = '%.2f' % token
                    volt_box.append(token)
        return (volt_box)

    def read_txt(self, input_path):
        if input_path.split('.')[-1] != 'txt':
            # 列出文件夹下所有的txt文件
            file_names = os.listdir(input_path)

            # 去除描述文件
            file_names_check = []

            for filename in file_names:

                if filename.split('.')[1] == 'txt':
                    file_names_check.append(filename)
        for filename in file_names_check:
            txtfilepath = input_path + '/' + filename  # 完整文件路径
            self.txt = pd.read_csv(txtfilepath, sep='\t')  # 读取txt
        pass

    def find_ele_area(self, input_path, bandpass=None, signal_scope=None):
        # 列出文件夹下所有的txt文件
        file_names = os.listdir(input_path)

        # 去除描述文件
        file_names_check = []

        for filename in file_names:

            if filename.split('.')[1] == 'txt':
                file_names_check.append(filename)

        #     print('files num: ',len(file_names),'>>> files check num: ',len(file_names_check))

        # 建立空表格
        dataFrame = pd.DataFrame()
        channel1Area = []
        channel2Area = []
        VoltNumList = []

        # 增加身体左右, 小鼠品系, 小鼠编号, 记录位点, led号码和其它标记
        trails = []
        leftorright = []
        miceStrain = []
        miceNum = []
        elePosition = []
        ledNum = []
        otherTags = []

        # 遍历filenamesCheck
        clocktoken = 0  # 计数

        for filename in file_names_check:

            clocktoken += 1  # 计数
            txtfilepath = input_path + '/' + filename  # 完整文件路径
            data = pd.read_csv(txtfilepath, sep='\t')  # 读取txt
            # 剔除data中的nan, 否则会影响bandpass, 得到nan
            # 一个传统的方法是在读取data的时候就把前面一点的数据都删掉, 或者都赋值为0
            # 这里拍了脑袋定了100个点, 10000采样频率来说相当于剪掉了1ms的数据, 对整体应该没有影响
            data.iloc[:100, :] = 0

            light_channel = data.iloc[:, 1]  # 找到lightChannel
            lightPosition = np.where(light_channel == 1)[0]  # 找到给光时间点
            channel2_raw = np.array(data.iloc[:, 2])
            channel1_raw = np.array(data.iloc[:, 3])

            # bandpass
            if bandpass is not None:
                channel1 = band_pass(channel1_raw, bandpass_num=bandpass)
                channel2 = band_pass(channel2_raw, bandpass_num=bandpass)

            pulse_time = sum(np.array(data.iloc[:, 1]))  # get light pulse times

            volt_box = EMG_database.volt_box_get(self, pulse_time)

            trails_token = 0
            trails_time = 3
            if signal_scope is None:
                for i in lightPosition:  # 遍历trigger附近的肌电情况并绘图
                    token_1 = baseline_check(channel1[i - 150:i + 450])  # 校正基线
                    # 计算area
                    channel1Area.append(sum(abs(token_1)))

                    token_2 = baseline_check(channel2[i - 150:i + 450])  # 校正基线
                    # 计算area
                    channel2Area.append(sum(abs(token_2)))

                    # 增加电压列
                    volt_token = volt_box.pop(0)
                    VoltNumList.append(volt_token)

                    # 增加其它tag
                    trails_token += 1
                    if trails_token > trails_time:
                        trails_token = 1
                    trails.append(trails_token)
                    leftorright.append(filename.split('-')[0])
                    miceStrain.append(filename.split('-')[1].split('_')[0])
                    miceNum.append(filename.split('-')[1].split('_')[1])
                    elePosition.append(filename.split('-')[1].split('_')[2])
                    ledNum.append(filename.split('-')[1].split('_')[3])
                    otherTags.append(filename.split('-')[2].split('.')[0])
            if signal_scope is not None:
                for i in lightPosition:  # 遍历trigger附近的肌电情况并绘图
                    token_1 = baseline_check(channel1[i:i + signal_scope])  # 校正基线
                    # 计算area
                    channel1Area.append(sum(abs(token_1)))

                    token_2 = baseline_check(channel2[i:i + signal_scope])  # 校正基线
                    # 计算area
                    channel2Area.append(sum(abs(token_2)))

                    # 增加电压列
                    volt_token = volt_box.pop(0)
                    VoltNumList.append(volt_token)

                    # 增加其它tag
                    trails_token += 1
                    if trails_token > trails_time:
                        trails_token = 1
                    trails.append(trails_token)
                    leftorright.append(filename.split('-')[0])
                    miceStrain.append(filename.split('-')[1].split('_')[0])
                    miceNum.append(filename.split('-')[1].split('_')[1])
                    elePosition.append(filename.split('-')[1].split('_')[2])
                    ledNum.append(filename.split('-')[1].split('_')[3])
                    otherTags.append(filename.split('-')[2].split('.')[0])

        dataFrame['Channel1'] = channel1Area  # 结果赋予表格并按文件名称命名
        dataFrame['Channel2'] = channel2Area
        dataFrame['VoltNum'] = VoltNumList
        dataFrame['Trails'] = trails
        dataFrame['leftorright'] = leftorright
        dataFrame['miceStrain'] = miceStrain
        dataFrame['miceNum'] = miceNum
        dataFrame['elePosition'] = elePosition
        dataFrame['ledNum'] = ledNum
        dataFrame['otherTags'] = otherTags

        dataFrame.to_csv(str(pulse_time) + '_Area_result.csv')  # 保存结果
        # print(str(pulse_time) + '_Area_result.csv' + '<<<文件保存完毕!')
        self.csv = dataFrame

    def find_ele_p2p(self, input_path):
        # 列出文件夹下所有的txt文件
        file_names = os.listdir(input_path)

        # 去除描述文件
        file_names_check = []

        for filename in file_names:

            if filename.split('.')[1] == 'txt':
                file_names_check.append(filename)

        #     print('files num: ',len(file_names),'>>> files check num: ',len(file_names_check))

        # 建立空表格
        dataFrame = pd.DataFrame()
        channel1P2P = []
        channel2P2P = []
        VoltNumList = []

        # 增加身体左右, 小鼠品系, 小鼠编号, 记录位点, led号码和其它标记
        trails = []
        leftorright = []
        miceStrain = []
        miceNum = []
        elePosition = []
        ledNum = []
        otherTags = []

        # 遍历filenamesCheck
        clocktoken = 0  # 计数

        for filename in file_names_check:

            clocktoken += 1  # 计数

            #         print(str(clocktoken)+'/'+str(len(file_names_check))+' '+filename+' Start...') # 计数

            txtfilepath = input_path + '/' + filename  # 完整文件路径

            data = pd.read_csv(txtfilepath, sep='\t')  # 读取txt

            light_channel = data.iloc[:, 1]  # 找到lightChannel

            #         print('trigger个数: ',sum(light_channel)) # 输出trigger个数

            # 对两种不同范式分开处理
            if sum(light_channel) != pulse_time:
                continue

            lightPosition = np.where(light_channel == 1)[0]  # 找到给光时间点

            channel2 = np.array(data.iloc[:, 2])
            channel1 = np.array(data.iloc[:, 3])
            # get light pulse times
            pulse_time = sum(np.array(data.iloc[:, 1]))

            volt_box = EMG_database.volt_box_get(self, pulse_time)

            trails_token = 0
            for i in lightPosition:  # 遍历trigger附近的肌电情况并绘图
                token = baseline_check(channel1[i - 150:i + 450])  # 校正基线
                # 计算Pick to Pick 峰峰之间的值
                channel1P2P.append(abs(max(token[160:440 + 150]) - min(token[160:440 + 150])))

                token = baseline_check(channel2[i - 150:i + 450])  # 校正基线
                # 计算Pick to Pick 峰峰之间的值
                channel2P2P.append(abs(max(token[160:440 + 150]) - min(token[160:440 + 150])))

                # 增加电压列
                token = volt_box.pop(0)
                VoltNumList.append(token)

                # 增加其它tag
                trails_token += 1
                if trails_token > 6:
                    trails_token = 1
                trails.append(trails_token)
                leftorright.append(filename.split('-')[0])
                miceStrain.append(filename.split('-')[1].split('_')[0])
                miceNum.append(filename.split('-')[1].split('_')[1])
                elePosition.append(filename.split('-')[1].split('_')[2])
                ledNum.append(filename.split('-')[1].split('_')[3])
                otherTags.append(filename.split('-')[2].split('.')[0])

        dataFrame['Channel1'] = channel1P2P  # 结果赋予表格并按文件名称命名
        dataFrame['Channel2'] = channel2P2P
        dataFrame['VoltNum'] = VoltNumList
        dataFrame['Trails'] = trails
        dataFrame['leftorright'] = leftorright
        dataFrame['miceStrain'] = miceStrain
        dataFrame['miceNum'] = miceNum
        dataFrame['elePosition'] = elePosition
        dataFrame['ledNum'] = ledNum
        dataFrame['otherTags'] = otherTags

        dataFrame.to_csv(str(pulse_time) + '_P2P_result.csv')  # 保存结果
        # print(str(pulse_time) + '_P2P_result.csv' + '<<<文件保存完毕!')
        return ()

    def paint_raw_data(self, input_path, trail_times, bandpass=None):
        print('start: ', input_path.split('/')[-1])
        # 列出文件夹下所有的txt文件
        file_names = os.listdir(input_path)

        # 去除描述文件
        file_names_check = []

        for filename in file_names:

            if filename.split('.')[1] == 'txt':
                file_names_check.append(filename)

        print('files num: ', len(file_names), '>>> files check num: ', len(file_names_check))

        clocktoken = 0  # 计数

        for filename in file_names_check:

            clocktoken += 1  # 计数

            print(str(clocktoken) + '/' + str(len(file_names_check)) + ' ' + filename + ' Start...')  # 计数

            txtfilepath = input_path + '/' + filename  # 完整文件路径

            data = pd.read_csv(txtfilepath, sep='\t')  # 读取txt

            light_channel = data.iloc[:, 1]  # 找到lightChannel

            print('trigger个数: ', sum(light_channel))  # 输出trigger个数

            lightPosition = np.where(light_channel == 1)[0]  # 找到给光时间点

            plt.figure(figsize=(10, 10))

            # get light pulse times
            pulse_time = sum(np.array(data.iloc[:, 1]))

            channel2 = np.array(data.iloc[:, 2])
            channel1 = np.array(data.iloc[:, 3])
            channel1_filter = band_pass(channel1, bandpass_num=bandpass)
            channel2_filter = band_pass(channel2, bandpass_num=bandpass)

            count_token = 0
            for i in lightPosition:  # 遍历trigger附近的肌电情况并绘图
                count_token += 1
                # 设计选择特定电压
                if count_token < 20 or count_token > 24:  # 采用2.9V数据
                    continue

                token_1 = baseline_check(channel1[i - 150:i + 450])  # 校正基线
                token_filter_1 = baseline_check(channel1_filter[i - 150:i + 450])  # 校正基线
                plt.subplot(4, 1, 1)
                plt.plot(token_1, 'k')
                plt.subplot(4, 1, 2)
                plt.plot(token_filter_1, 'r')

                token_2 = baseline_check(channel2[i - 150:i + 450])  # 校正基线
                token_filter_2 = baseline_check(channel2_filter[i - 150:i + 450])  # 校正基线
                plt.subplot(4, 1, 3)
                plt.plot(token_2, 'k')
                plt.subplot(4, 1, 4)
                plt.plot(token_filter_2, 'g')

                # Y_LIM = [-0.3, 0.2]
                # plt.ylim(Y_LIM)

            plt.savefig(filename + '.pdf', dpi=200, bbox_inches='tight')
            print('图像保存完毕')

        #     dataFrame.to_csv(str(modeNum)+'_triggers_result.csv') # 保存结果

        return ()


class structure_change:
    def __init__(self, data):
        self.data = None
        self.structure = 'database'

        self.data = data
        self.data_normalized = None

        structure_change.get_new_frame(self, self.data)
        structure_change.add_muscle_tag(self, self.data)

    def get_new_frame(self, data):
        # 新建空白list
        Area = []
        ChannelNum = []
        VoltNumList = []
        Trails = []
        LeftOrRight = []
        MiceStrain = []
        MiceNum = []
        ElePosition = []
        LedNum = []
        OtherTags = []
        # 分别读取Channel1和Channel2的结果
        for i in range(len(data['Channel1'])):
            Area.append(data['Channel1'][i])
            ChannelNum.append(1)
            VoltNumList.append(data['VoltNum'][i])
            Trails.append(data['Trails'][i])
            LeftOrRight.append(data['leftorright'][i])
            MiceStrain.append(data['miceStrain'][i])
            MiceNum.append(data['miceNum'][i])
            ElePosition.append(data['elePosition'][i])
            LedNum.append(data['ledNum'][i])
            OtherTags.append(data['otherTags'][i])
        for i in range(len(data['Channel2'])):
            Area.append(data['Channel2'][i])
            ChannelNum.append(2)
            VoltNumList.append(data['VoltNum'][i])
            Trails.append(data['Trails'][i])
            LeftOrRight.append(data['leftorright'][i])
            MiceStrain.append(data['miceStrain'][i])
            MiceNum.append(data['miceNum'][i])
            ElePosition.append(data['elePosition'][i])
            LedNum.append(data['ledNum'][i])
            OtherTags.append(data['otherTags'][i])
        # 对新的表格进行赋值
        datareshape = pd.DataFrame()
        datareshape['Area'] = Area
        datareshape['ChannelNum'] = ChannelNum
        datareshape['VoltNumList'] = VoltNumList
        datareshape['Trails'] = Trails
        datareshape['LeftOrRight'] = LeftOrRight
        datareshape['MiceStrain'] = MiceStrain
        datareshape['MiceNum'] = MiceNum
        datareshape['ElePosition'] = ElePosition
        datareshape['LedNum'] = LedNum
        datareshape['OtherTags'] = OtherTags
        self.data = datareshape
        self.structure = self.structure + '--one line area'

    def add_muscle_tag(self, data):

        def muscle_check(MiceNum, OtherTags, ElePosition, ChannelNum):
            '''
            通过获得小鼠编号，othertags，刺激位置以及通道编号，就能获知每组数据对应的肌肉名称是什么

            MiceNum, 小鼠编号，int
            OtherTags, str
            ElePosition, str
            ChannelNum，int
            '''

            target_muscle = 'no muscle'
            try:
                MiceNum = int(MiceNum)
                OtherTags = str(OtherTags)
                ChannelNum = int(ChannelNum)

                if ElePosition == 'C7':
                    if MiceNum <= 4 and MiceNum != 2:
                        if ChannelNum == 1:
                            target_muscle = 'Tricep'
                        if ChannelNum == 2:
                            target_muscle = 'Extensor carpi'
                    if MiceNum == 2:
                        if ChannelNum == 1:
                            target_muscle = 'Artifact'
                        if OtherTags == '1' and ChannelNum != 1:
                            target_muscle = 'Tricep'
                        if OtherTags == '2' and ChannelNum != 1:
                            target_muscle = 'Extensor carpi'
                    if MiceNum >= 5:
                        if OtherTags == '1':
                            if ChannelNum == 1:
                                target_muscle = 'Pectoralis major'
                            if ChannelNum == 2:
                                target_muscle = 'Extensor carpi'
                        if OtherTags == '2':
                            if ChannelNum == 1:
                                target_muscle = 'Tricep'
                            if ChannelNum == 2:
                                target_muscle = 'Extensor digitorum'
                        if OtherTags == '3' and MiceNum == 8:
                            if ChannelNum == 1:
                                target_muscle = 'Tricep'
                            if ChannelNum == 2:
                                target_muscle = 'Wrist Flexors'
                        if OtherTags == '3' and 9 <= MiceNum <= 11:
                            if ChannelNum == 1:
                                target_muscle = 'Wrist Flexors'
                            if ChannelNum == 2:
                                target_muscle = 'Extensor carpi'
                        if OtherTags == '3' and MiceNum >= 12:
                            if ChannelNum == 1:
                                target_muscle = 'Biceps'
                            if ChannelNum == 2:
                                target_muscle = 'Flexor carpi'
                if ElePosition == 'Sc':
                    if MiceNum == 2:
                        if ChannelNum == 1:
                            target_muscle = 'Artifact'
                        else:
                            if OtherTags == '1' or OtherTags == 'jingqian':
                                target_muscle = 'Tibialis anterior muscle'
                            if OtherTags == '2' or OtherTags == 'feichang':
                                target_muscle = 'Gastrocnemius muscle'
                    if MiceNum != 2:
                        if ChannelNum == 1:
                            target_muscle = 'Tibialis anterior muscle'
                        if ChannelNum == 2:
                            target_muscle = 'Gastrocnemius muscle'
            except:
                target_muscle = 'no muscle'
            return (target_muscle)

        muscle_basket = []
        for i in range(len(data)):
            token = data.iloc[i, :]
            # print(token.MiceNum, token.ChannelNum, token.ElePosition, token.OtherTags)
            target_muscle = muscle_check(token.MiceNum, token.OtherTags, token.ElePosition, token.ChannelNum)
            # print(target_muscle)
            muscle_basket.append(target_muscle)
        # print(muscle_basket)
        data['Muscle'] = muscle_basket
        if 'no muscle' in data['Muscle']:
            print('we have "no muscle" in "Muscle" tag')
        self.data = data
        self.structure = self.structure + '--add muscle tag'

    def normalized_old(self, data):
        '''
        检查数据后，对每只小鼠每个LED的每个肌肉做归一化

            因为肌肉之间可能存在电极插入方法角度的变化，使得不同肌肉之间不能一起做归一化
            而不同LED之间做比较，也是说的通的，因为不同LED情况下，
                肌电电极针位置并没有发生变化（变化很微小）
            所以这里采用的是每一块肌肉单独做归一化
        :param data:承接增加了肌肉tag和结构发生变化了的dataframe数据
        :return:对每只小鼠每个LED所有肌肉做归一化的结果
        '''
        # 按顺序读取每列，自动新建有标签的盒子，把Area丢进对应的盒子里，最后再对盒子进行一次计算获得归一化后数值
        # 每一次导入后都用一个新列表装着dict中每个列表的位置信息
        token_dict = {}
        # 先制作有名称的盒子
        for i in range(len(data)):
            token = data.iloc[i, :]
            token_dict[(token.MiceNum, token.OtherTags, token.ElePosition, token.ChannelNum, token.LedNum)] = []
        # 往对应盒子中丢数据
        for i in range(len(data)):
            token = data.iloc[i, :]
            token_dict[(token.MiceNum, token.OtherTags, token.ElePosition, token.ChannelNum, token.LedNum)].append(
                token.Area)
        print('每一个箱子中元素个数：', len(list(token_dict.values())[0]))
        print('箱子总数：', len(token_dict))
        # 矩阵计算归一化后的数值
        # boxes = np.array(list(token_dict.values()))
        # boxes_max = np.max(boxes,axis=1)
        # boxes_normalized = boxes / boxes_max
        boxes = pd.DataFrame(token_dict)
        boxes_max = boxes.max(axis=0)
        boxes_normalized = boxes.div(boxes_max, axis='columns')
        self.data_normalized = boxes_normalized
        print(boxes)
        print(boxes_max)
        print(boxes_normalized)
        # print(np.shape(boxes))
        # print(np.shape(np.max(boxes,axis=1)))
        # print(np.shape(boxes_normalized))
        self.structure = self.structure + '--add normal data'
        pass

    def normalized_new(self, data):
        '''
        检查数据后，对每只小鼠每个LED的每个肌肉做归一化

            因为肌肉之间可能存在电极插入方法角度的变化，使得不同肌肉之间不能一起做归一化
            而不同LED之间做比较，也是说的通的，因为不同LED情况下，
                肌电电极针位置并没有发生变化（变化很微小）
            所以这里采用的是每一块肌肉单独做归一化

        How：
            获得数据中每个tag的非重复列表，对其中特定tag做循环，寻找对应的内容
            相比较于使用dict的数据，使用检索更加的普适性和robust，而不是临时解决问题的方案

        :param data:承接增加了肌肉tag和结构发生变化了的dataframe数据
        :return:对每只小鼠每个LED所有肌肉做归一化的结果
        '''
        _,_,title_dict = get_title_list(data, mode=3)
        # 使用itertool的笛卡尔积来做多重嵌套循环
        # https://www.jianshu.com/p/57a6e1188f88

        box_new = pd.DataFrame()

        for leftorright_item, \
            micenum_item, eleposition_item, \
            lednum_item in product(
                title_dict['LeftOrRight'],
                title_dict['MiceNum'], title_dict['ElePosition'],
                title_dict['LedNum']
            ):
            box_token = data[(data.LeftOrRight==leftorright_item)&
                 (data.MiceNum == micenum_item) &(data.ElePosition==eleposition_item)&
                 (data.LedNum == lednum_item)
            ]
            #  count every dataframe
            box_token_max = box_token['Area'].max()
            boxes_token_normalized = box_token['Area'].div(box_token_max)
            box_token['Area'] = boxes_token_normalized
            box_new = pd.concat([box_new, box_token])
        self.data_normalized = box_new
        self.structure = self.structure + '--normalized'


    # def get_result_at_same_volt(self, csvfilepath):
    #     # 读取数据
    #     data = pd.read_csv(csvfilepath)
    #     # 改变csv结构
    #     datareshape_area = get_new_frame(data)
    #     # 新增肌肉列表
    #     datareshape_area_muscleadded = add_muscle_tag(datareshape_area)
    #     # 对单独一只小鼠建立分析矩阵(列为不同led, 行为不同电压)
    #     datareshape_area_muscleadded = datareshape_area_muscleadded[(datareshape_area_muscleadded.MiceNum == '16') &
    #                                                                 (datareshape_area_muscleadded.ElePosition == 'C7')]
    #
    #     list_token = []
    #     def_token = lambda x: datareshape_area_muscleadded.drop_duplicates(subset=x, keep='first')[x].tolist()
    #     # 通过获得每列不重复的结果来获得有多少muscle
    #     list_token.append(def_token('Muscle'))
    #     # 对no muscle进行筛选
    #     if 'no muscle' in list_token:
    #         print('***find no muscle***')
    #
    #     ############################################################################################################
    #     # for来取数据进行分析
    #     led_box = ['led' + str(i) for i in range(1, 9)]
    #     volt_box = [i / 10 for i in range(26, 33, 1)]
    #     for muscle_item in def_token('Muscle'):
    #         list_different_led_token = []
    #         for led_item in led_box:
    #             list_different_volt_token = []
    #
    #             for volt_item in volt_box:  # 获得不同电压下的area
    #
    #                 # 通过channel num和other tags来确认是什么肌肉, 每块肌肉画一幅图
    #                 data_token = datareshape_area_muscleadded[(datareshape_area_muscleadded.LedNum == led_item) &
    #                                                           (datareshape_area_muscleadded.Muscle == muscle_item) &
    #                                                           (datareshape_area_muscleadded.VoltNumList == volt_item)][
    #                     'Area']
    #                 if len(data_token) != 0:
    #                     data_token_ave = sum(data_token) / len(data_token)
    #                     list_different_volt_token.append(data_token_ave)
    #
    #             if len(list_different_volt_token) != 0:
    #                 list_different_led_token.append(list_different_volt_token)
    #         #     print(len(list_different_led_token))
    #         list_token.append(np.array(list_different_led_token).T)
    #     # matrix_token = np.array(list_token).T
    #     # print(list_token)
    #
    #     print('肌肉个数 = ', len(list_token) - 1)
    #     # 归一化数据结果
    #     '''
    #     对于每一个LED来说, 某一个电压下会对5块肌肉同时产生干预, 那么在每一个电压下这5块肌肉之间可以做归一化来看在这个电压下LED在5块肌肉中干预的偏好是怎样的.
    #     换言之, 我需要对每个LED的每个电压下的5块肌肉都做一下归一化:
    #     - 找到数值最大的肌肉, 同时其他肌肉的数值计算rate
    #     '''
    #     token_voltbox = []
    #     for volt_token in range(np.shape(list_token[1])[0]):
    #         token_ledbox = []
    #         for led_token in range(np.shape(list_token[1])[1]):
    #             try:
    #                 token = []
    #                 for i in range(1, len(list_token) - 1):  # 修正除去了最后一块肌肉
    #                     token.append(list_token[i][volt_token, led_token])
    #                     token_m = np.array(token)
    #                     #             print(len(token))
    #                     #                 print(max(token))
    #                     token_m = token_m / max(token)
    #             #             print(token_m)
    #             except:
    #                 print('有肌肉个数不对')
    #             token_ledbox.append(list(token_m))
    #         token_voltbox.append(token_ledbox)
    #     data_m = np.array(token_voltbox)
    #     print('矩阵维度 = ', np.shape(data_m))
    #     # 绘制热图
    #     print(data_m)
    #     paint_heatmap(data_m, 5)

    def baseline_check(data):
        # 去除数据的漂移(归零)并保留扰动(波)
        baseline = np.mean(data[:30])
        data_baseline_check = data - baseline
        return (data_baseline_check)

    def muscle_check(MiceNum, OtherTags, ElePosition, ChannelNum):
        '''
        通过获得小鼠编号，othertags，刺激位置以及通道编号，就能获知每组数据对应的肌肉名称是什么

        MiceNum, 小鼠编号，int
        OtherTags, str
        ElePosition, str
        ChannelNum，int
        '''

        target_muscle = 'no muscle'
        try:
            MiceNum = int(MiceNum)
            if ElePosition == 'C7':
                if MiceNum <= 4 and MiceNum != 2:
                    if ChannelNum == 1:
                        target_muscle = 'Tricep'
                    if ChannelNum == 2:
                        target_muscle = 'Extensor carpi'
                if MiceNum == 2:
                    if ChannelNum == 1:
                        target_muscle = 'Artifact'
                    if OtherTags == '1' and ChannelNum != 1:
                        target_muscle = 'Tricep'
                    if OtherTags == '2' and ChannelNum != 1:
                        target_muscle = 'Extensor carpi'
                if MiceNum >= 5:
                    if OtherTags == '1':
                        if ChannelNum == 1:
                            target_muscle = 'Pectoralis major'
                        if ChannelNum == 2:
                            target_muscle = 'Extensor carpi'
                    if OtherTags == '2':
                        if ChannelNum == 1:
                            target_muscle = 'Tricep'
                        if ChannelNum == 2:
                            target_muscle = 'Extensor digitorum'
                    if OtherTags == '3' and MiceNum == 8:
                        if ChannelNum == 1:
                            target_muscle = 'Tricep'
                        if ChannelNum == 2:
                            target_muscle = 'Wrist Flexors'
                    if OtherTags == '3' and 9 <= MiceNum <= 11:
                        if ChannelNum == 1:
                            target_muscle = 'Wrist Flexors'
                        if ChannelNum == 2:
                            target_muscle = 'Extensor carpi'
                    if OtherTags == '3' and MiceNum >= 12:
                        if ChannelNum == 1:
                            target_muscle = 'Biceps'
                        if ChannelNum == 2:
                            target_muscle = 'Extensor carpi'
            if ElePosition == 'Sc':
                if MiceNum == 2:
                    if ChannelNum == 1:
                        target_muscle = 'Artifact'
                    else:
                        if OtherTags == '1' or OtherTags == 'jingqian':
                            target_muscle = 'Tibialis anterior muscle'
                        if OtherTags == '2' or OtherTags == 'feichang':
                            target_muscle = 'Gastrocnemius muscle'
                if MiceNum != 2:
                    if ChannelNum == 1:
                        target_muscle = 'Tibialis anterior muscle'
                    if ChannelNum == 2:
                        target_muscle = 'Gastrocnemius muscle'
        except:
            target_muscle = 'no muscle'
        return (target_muscle)

    def ready_4_heat_map(self, data):
        # 获得归一化后的数据结构
        # 结果做成一个字典可能也会不错, 这样绘图的时候能直接索引, 而不是传一个列表过去, 列表的结构也有可能发生变化
        # 这里也可以直接用self.data来进行参数传递
        # x_title = 'LedNum'
        # y_title = 'VoltNum'

        title, title_box, _ = get_title_list(data, mode=3)

        # for title_token in title:
        #     print(title_token)
        # print(title_box)

        # 或者这里也可以设计成除去x和y_title以外的其它的循环, 这样能够复用到其它的数据分析当中
        data_choose_box = []
        data_choose_log = []
        for trail_num, left_or_right, mice_strain, mice_num, ele_position, muscle_name \
                in product(title_box[2], title_box[3], title_box[4], title_box[5], title_box[6], title_box[9]):
            data_choose = self.data[(self.data['Trails'] == trail_num) &
                                    (self.data['LeftOrRight'] == left_or_right) &
                                    (self.data['MiceStrain'] == mice_strain) &
                                    (self.data['MiceNum'] == mice_num) &
                                    (self.data['ElePosition'] == ele_position) &
                                    (self.data['Muscle'] == muscle_name)]

            # 对数据做normalized
            data_choose = data_choose.copy()  # 此方法可规避警告:
            # https://blog.csdn.net/qq_41987033/article/details/81454933

            data_choose['AreaNormalized'] = normalize_data(data_choose['Area'])

            # print(data_choose)
            data_array_list = []
            _ = [
                data_array_list.append(
                    list(data_choose[data_choose['LedNum'] == led_num]['AreaNormalized'].values))
                for led_num in title_box[7]]

            data_array = np.array(data_array_list).T
            data_choose_box.append(data_array)
            data_choose_log.append(str(trail_num) + '-' +
                                   str(left_or_right) + '-' +
                                   str(mice_strain) + '-' +
                                   str(mice_num) + '-' +
                                   str(ele_position) + '-' +
                                   str(muscle_name))
        self.structure = self.structure + '--heat map structure'
        return data_choose_box, data_choose_log


class art_show:
    def __init__(self, data):
        self.data = data
        print('开始作画')

    # def Splt(self, xVal, pltTitle, pltScale=3, hueChoose=['False'],
    #          Y_LIM='False'):  # hueChoose='False',hueT,paletteT="husl"
    #     sns.set(font_scale=pltScale)
    #     sns.set_style('white')
    #     for yVal in ['Area']:
    #         # 'ChewCount','ChewTime','ClimbCount','ClimbTime'
    #         if hueChoose[0] == 'True':
    #             sns.stripplot(data=a, y=yVal, x=xVal, jitter=True, color='.5', hue=hueChoose[1], palette=hueChoose[2])
    #             # split=True
    #         else:
    #             sns.stripplot(data=a, y=yVal, x=xVal, jitter=True, color='.5')
    #         sns.barplot(data=a, y=yVal, x=xVal, color='.8')
    #         if Y_LIM != 'False':
    #             plt.ylim(Y_LIM)
    #         plt.title(pltTitle)
    #         plt.savefig(pltTitle + '.jpg')
    #         plt.show()

    # 可以用selective index来绘制heatmap, 这样能够有更好的视觉效果
    def PTTest(self, SampleA, SampleB, only2Sample='False'):
        # paired ttest
        print(' Two Sample TTest: ', stats.ttest_ind(SampleA, SampleB)[1])
        if only2Sample == 'False':
            SA = np.array(SampleA)
            SB = np.array(SampleB)
            S0 = np.zeros(len(SA))
            SR = SA - SB
            print(' Paired TTest: ', stats.ttest_ind(SR, S0)[1])

    def paint_heatmap(self, data, fig_title, filename):
        plt.figure(figsize=(10, 10 * len(data)))
        sns.set(font_scale=3)
        for i in range(len(data)):
            # print(np.shape(data[i]))
            plt.subplot(len(data), 1, i + 1)
            sns.heatmap(data[i])
            plt.title(fig_title[i])
            # plt.suptitle(fig_title[i])
        plt.savefig(filename)

    def get_colormap_merge(self, data, mode):
        # get colormap
        ncolors = 256
        # color_array = plt.get_cmap('gist_rainbow')(range(ncolors_max))
        color_box = ['Reds', 'Oranges', 'Greens', 'Blues', 'Purples']
        f, ax = plt.subplots()
        for i in range(mode):
            color_choose = color_box[i]
            color_array = plt.get_cmap(color_choose)(range(ncolors))
            # get_cmap取值范围
            # https://blog.csdn.net/yefengzhichen/article/details/52757722

            # change alpha values
            alpha_values_max = 0.9
            alpha_values_min = 0.8
            color_array[:, -1] = np.linspace(alpha_values_max, alpha_values_min, ncolors)

            # create a colormap object
            map_object = LinearSegmentedColormap.from_list(name='rainbow_alpha', colors=color_array)

            # register this new colormap with matplotlib
            plt.register_cmap(cmap=map_object)

            # show some example data
            h = ax.imshow(data[:, :, i], cmap='rainbow_alpha')
            plt.colorbar(mappable=h)
        plt.show()


# 希望尝试的列表
# - [ ] 相当于我对函数做了一个二级分装, 有条理的分装
# - [ ] 找到什么是对状态的获取, 找到什么是功能的延伸


file_path_txt = ''
file_path_csv = '24_Area_result.csv'

data = EMG_database('read csv file', txt_file_path=None, csv_file_path=file_path_csv,
                    paint_raw=None, signal_scope=100,
                    bandpass_num=[50, 300])  # 读取数据 # NOTE: signal_scope=100, bandpass_num=[100, 300]

# 改变数据结构和归一化
data_reshaped = structure_change(data.csv)  # 整理数据结构
data_reshaped.normalized_new(data_reshaped.data)

data_heat_map_list, data_heat_map_log = data_reshaped.ready_4_heat_map(data_reshaped.data_normalized)  # 获得数据内容

# 绘制heatmap
data_painted = art_show(data_heat_map_list)
fig_name = 'test123_norm'
fig_title = data_heat_map_log
data_painted.paint_heatmap(data_painted.data, fig_title, fig_name)

# 结束后打印log
print('Log: ', data_reshaped.structure)
