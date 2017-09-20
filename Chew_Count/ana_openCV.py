# 分析后能够保存judge后的每一帧的图片
import cv2
import os
import sys
import numpy as np
from tqdm import tqdm
import copy
import pandas as pd
import random

import def_baggage_666 as db6


def pixel_record_2(input_path, r_s, LED_scope = [0,2,0,2], video_form = 'mov', figure_condition_save ='False', mode = 'real_time', bolt = 25, threshold_condition = 0.8, video_mode = 'NaN', skip_frame = 1):# 这里斜杠可以起到换行的作用
    if figure_condition_save == 'true' or figure_condition_save == 'false':
        print('傻逼你的True or False首字母忘记大写了!')
        return()
    print('视频对识别小鼠吃东西经过特别优化')
    # 列出文件夹下所有的视频文件
    filenames = os.listdir(input_path)
    # 获取文件夹名称
    video_prefix = input_path.split(os.sep)[-1]
    # 建立一个新的文件夹，名称为原文件夹名称后加上_frames
    frame_path = '{}_frames'.format(input_path)
    if not os.path.exists(frame_path):
        os.mkdir(frame_path)
    # 建立一个新的文件夹, 用来装漏网之鱼
    frame_path_escaped = '{}_escaped'.format(input_path)
    if not os.path.exists(frame_path_escaped):
        os.mkdir(frame_path_escaped)
    # 初始化一个VideoCapture对象
    cap = cv2.VideoCapture()
    # 遍历所有文件
    for filename in tqdm(filenames):
        print('正在分析的 filename is: ', filename)
        if filename == '.DS_Store':# 果然是.DS_Store的锅, 现在内存也不爆了
            continue
        #REVIEW [X]尝试对Segmentation fault进行解决: 使用一个if
        if filename.split('.')[1] == video_form:
            filepath = os.sep.join([input_path, filename])
            # VideoCapture::open函数可以从文件获取视频
            cap.open(filepath)
            # 获取视频帧数
            n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            print('Frame: ', n_frames)
            # 同样为了避免视频头几帧质量低下，黑屏或者无关等, 可用以下代码改变参数'42', 跳过这几帧
            # for i in range(42):
            #     cap.read()
            # 调用第一帧, 获取视频基本信息

            # 选择要跳过的帧数
            print('正在跳过前', skip_frame, '帧, 以解决水管移动问题')
            for item in tqdm(range(skip_frame)):
                nap,frame = cap.read()
            print('已经跳过',skip_frame, '帧数')
            nap,frame = cap.read()
            if nap == True:
                print('Video matrix shape: ', np.shape(frame))
                # 保存第一帧的图片
                imagename = '{}_{}_start.jpg'.format(video_prefix, filename.split('.')[0])
                imagepath = os.sep.join([frame_path, imagename])
                print('exported {}!'.format(imagepath))
                frame[r_s[0]:r_s[1],r_s[2]:r_s[3],:] = 255
                print('蓝色区域为bkg')
                frame[(r_s[0]):(r_s[1]),(r_s[2]-100):(r_s[3]-100),0] = 255
                frame[(r_s[0]):(r_s[1]),(r_s[2]-100):(r_s[3]-100),1:3] = 0
                cv2.imwrite(imagepath, frame)
                # 获得frame的shape
                shape_frames = np.shape(frame)
                # 确定需要分析的范围
            else:
                print('视频信息获取失败')
                return('代码运行错误')
            # 新建存储列表
            patch_trees = []
            patch_trees_bkg = []
            patch_LED_list = [] # LED 存储list
            patch_grating_list = [] # grating list
            # 开始分析
            for i in tqdm(range(int(n_frames-skip_frame-1))): # REVIEW 如果n_frame-25能否去除内存bug, 如果能解决, 那就是else写入255的锅. 不能解决, 应该是最后release的锅
                # 按帧读取每一帧的RGB
                # 例子:
                # >>> np.shape(frame)
                # >>> (1920,1080,3)
                nap, frame = cap.read()
                # 一定要加上这句话, 否则会报错: 'Segmentation fault: 11'
                if nap == True:
                    # 获取需要分析的位置范围
                    patch_tree_target = frame[r_s[0]:r_s[1],r_s[2]:r_s[3],:]
                    # 获取分析位点下15个像素点作为参考
                    patch_tree_bkg = frame[(r_s[0]):(r_s[1]),(r_s[2]-100):(r_s[3]-100),:]
                    # 获取光栅分析位点
                    patch_grating = frame[(r_s[0]-140):(r_s[1]-140),(r_s[2]+560):(r_s[3]+560),:]
                    # 获取LED分析区域
                    patch_LED = frame[LED_scope[0]:LED_scope[1],LED_scope[2]:LED_scope[3],:]
                    # 对目标范围内求平均灰度, 获得一个数
                    patch_tree_ave = np.mean(patch_tree_target)
                    # 对参考范围求平均灰度, 获得一个数
                    patch_tree_bkg_ave = np.mean(patch_tree_bkg)
                    # LED分析区域求平均灰度
                    patch_LED_ave = np.mean(patch_LED)
                    # 光栅分析区域求平均灰度
                    patch_grating_ave = np.mean(patch_grating)

                    if figure_condition_save == 'True':
                        # REVIEW 判断是否小于threshold, 保存所有小于threshold的图片
                        if patch_tree_ave < patch_tree_bkg_ave * threshold_condition:
                            imagename = '{}_{}_{:0>6d}.jpg'.format(video_prefix, filename.split('.')[0], i)
                            imagepath = os.sep.join([frame_path, imagename])
                            cv2.imwrite(imagepath, frame[(r_s[0]-100):(r_s[1]+100),(r_s[2]-100):(r_s[3]+100),:])# 修改导出视频的范围, 以加快速度
                        else:
                            imagename = '{}_{}_{:0>6d}.jpg'.format(video_prefix, filename.split('.')[0], i)
                            imagepath = os.sep.join([frame_path_escaped, imagename])
                            cv2.imwrite(imagepath, frame[(r_s[0]-100):(r_s[1]+100),(r_s[2]-100):(r_s[3]+100),:])# 修改导出视频的范围, 以加快速度
                    # 递交结果
                    patch_trees.append(patch_tree_ave)
                    patch_trees_bkg.append(patch_tree_bkg_ave)
                    patch_LED_list.append(patch_LED_ave)
                    patch_grating_list.append(patch_grating_ave)
                else:
                    # 将假帧补为255 使得最终结果长度与视频总帧数一致
                    patch_trees.append(255)
                    patch_trees_bkg.append(255)
                    patch_LED_list.append(0)
        print('patch_trees的长度为: ', len(patch_trees))
        csv_name_token = '{}_{}_result.csv'.format(video_prefix, filename.split('.')[0])
        db6.text_save_fnda(patch_trees, csv_name_token)
        eps_name_token = '{}_{}_result.eps'.format(video_prefix, filename.split('.')[0])
        db6.painting_trees(patch_trees, eps_name_token)
        csv_name_token = '{}_{}_result_bkg.csv'.format(video_prefix, filename.split('.')[0])
        db6.text_save_fnda(patch_trees_bkg, csv_name_token)
        eps_name_token = '{}_{}_result_bkg.eps'.format(video_prefix, filename.split('.')[0])
        db6.painting_trees(patch_trees_bkg, eps_name_token)



        #NB 开始分析
        target_a = np.array(patch_trees) #NOTE
        bkg_a = np.array(patch_trees_bkg)
        # 获得grating的变化情况并导出csv, 不用理会命名, 这段懒得改了
        if video_mode == 'CED':
            bkg_nda = np.array(patch_grating_list)
            bkg_judge = bkg_nda < 70 # 120是从图片中找到的, 与上面的选择尺寸相关联
            # NB: 上排, +是或, *是和

            # 变量声明
            count_grating = 0
            grating_onoff = []
            state_3 = 0
            state_4 = 0
            for num in range(len(bkg_judge)-1):
                token = bkg_judge[num + 1:num + bolt + 1] == 1
                if bkg_judge[num] == False and bkg_judge[num+1] == True:
                    if state_3 == 0:
                        token_on = num+1
                    state_3 = 1
                if bkg_judge[num] == True and True not in token:
                    token_off = num
                    state_4 = 1
                if state_3 == 1 and state_4 == 1 and token_off - token_on > 1: # NOTE 增加对光栅段的长度的判定, off要大于on 6帧
                    grating_onoff.append([token_on, token_off])
                    state_3 = 0
                    state_4 = 0
                    count_grating = count_grating + 1
            print('光栅被检测到的次数为: ', count_grating)
            # 将grating_onoff time结果保存
            csv_name_token = '{}_{}_grating_onoff_list.csv'.format(video_prefix, filename.split('.')[0])
            db6.text_save_fnda(grating_onoff, csv_name_token)
        # threshold判断
        if mode == 'Normal':
            threshold = np.min(bkg_a)*threshold_condition
            target_a_judge = target_a < threshold
        elif mode == 'Cut':
            target_a_token = target_a - bkg_a
            threshold = np.min(bkg_a) * threshold_condition
            target_a_judge = target_a_token < threshold
        elif mode == 'real_time':
            target_a_judge = target_a < (bkg_a * threshold_condition)
        # 新建变量
        count_True = 0
        count_drink_start = 0
        count_drink_end = 0
        count_drink_list = []
        count_drink = 0
        state_1 = 0
        state_2 = 0
        for num in range(len(target_a_judge)-1):
            token = target_a_judge[num + 1:num + bolt + 1] == 1
            if target_a_judge[num] == True:
                count_True = count_True + 1
            if target_a_judge[num] == False and target_a_judge[num+1] == True:
                if state_1 == 0:
                    count_drink_start = num+1
                state_1 = 1
            if target_a_judge[num] == True and True not in token:
                count_drink_end = num
                state_2 = 1
            if state_1 == 1 and state_2 == 1:
                # talk_list = ['我找到一对甩舌头啦!!!!', '又找到一个', '好爽, 又找到一个']
                # print(talk_list[random.randint(0,2)])
                count_drink_list.append([count_drink_start, count_drink_end])
                state_1 = 0
                state_2 = 0
                count_drink = count_drink + 1
        print('Drink behavior count: ',count_drink)
        print('True count: ', count_True)
        # 将judge结果保存
        csv_name_token = '{}_{}_result_judge.csv'.format(video_prefix, filename.split('.')[0])
        db6.text_save_fnda(target_a_judge, csv_name_token)
        eps_name_token = '{}_{}_result_judge.eps'.format(video_prefix, filename.split('.')[0])
        db6.painting_trees(target_a_judge, eps_name_token)
        # 将count结果保存
        csv_name_token = '{}_{}_count_drink_list.csv'.format(video_prefix, filename.split('.')[0])
        db6.text_save_fnda(count_drink_list, csv_name_token)
        print('程序运行完毕')
        cap.release()# 释放内存, 在for循环内释放, 这样应该能够避免释放后被修改的bug
    return()


def ana_subsection():
    pass
    return()
