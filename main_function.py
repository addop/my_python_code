import cv2
import os
import sys
import numpy as np
from tqdm import tqdm
import copy
import pandas as pd

import def_baggage_666 as db6

# 视频分析V1
def pixel_record_666(input_path, r_s, mode = False, frame_interval = 25):
    # 列出文件夹下所有的视频文件
    filenames = os.listdir(input_path)

    # 获取文件夹名称
    video_prefix = input_path.split(os.sep)[-1]

    # # 建立一个新的文件夹，名称为原文件夹名称后加上_frames
    # if mode = True:
    #     frame_path = '{}_frames'.format(input_path)
    #     if not os.path.exists(frame_path):
    #         os.mkdir(frame_path)

    # 初始化一个VideoCapture对象
    cap = cv2.VideoCapture()

    # 遍历所有文件
    for filename in filenames:
        filepath = os.sep.join([input_path, filename])

        # VideoCapture::open函数可以从文件获取视频
        cap.open(filepath)

        # 获取视频帧数
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print('视频帧数为: ', n_frames)
        # 同样为了避免视频头几帧质量低下，黑屏或者无关等, 可用以下代码改变参数'42', 跳过这几帧
        # for i in range(42):
        #     cap.read()

        # 调用第一帧, 获取视频基本信息
        nap,frame = cap.read()
        if nap == True:
            print('获得视频nda基本信息: ', np.shape(frame))

            # 获得frame的shape
            shape_frames = np.shape(frame)

            # 确定需要分析的范围
        else:
            print('视频信息获取失败')
            return('代码运行错误')

        # 新建存储列表
        patch_trees = []
        patch_trees_bkg = []

        for i in tqdm(range(int(n_frames))):

            # 按帧读取每一帧的RGB
            # 例子:
            # >>> np.shape(frame)
            # >>> (1920,1080,3)
            nap, frame = cap.read()

            # 一定要加上这句话, 否则会报错: 'Segmentation fault: 11'
            if nap == True:

                # 获取需要分析的位置范围
                patch_tree_target = frame[r_s[0]:r_s[1],r_s[2]:r_s[3],:]

                # 获取分析位点下30个像素点作为参考
                patch_tree_bkg = frame[(r_s[0]+15):(r_s[1]+15),r_s[2]:r_s[3],:]



                # # 每隔frame_interval帧进行一次截屏操作, 并保存到新的文件夹中
                # if mode = True:
                #     if i % frame_interval == 0:
                #         imagename = '{}_{}_{:0>6d}.jpg'.format(video_prefix, filename.split('.')[0], i)
                #         imagepath = os.sep.join([frame_path, imagename])
                #         print('exported {}!'.format(imagepath))
                #         cv2.imwrite(imagepath, frame)

                # 对目标范围内求平均灰度, 获得一个数
                patch_tree_ave = np.mean(patch_tree_target)

                # 对参考范围求平均灰度, 获得一个数
                patch_tree_bkg_ave = np.mean(patch_tree_bkg)

                # 递交结果
                patch_trees.append(patch_tree_ave)
                patch_trees_bkg.append(patch_tree_bkg_ave)
            else:
                # 将假帧补为255 使得最终结果长度与视频总帧数一致
                patch_trees.append(255)
                patch_trees_bkg.append(255)

    print('patch_trees的长度为: ', len(patch_trees))

    # 调用def_baggage_666中的函数, 将列表存为csv文件
    db6.text_save_fnda(patch_trees, 'result.csv')
    db6.text_save_fnda(patch_trees_bkg, 'result_bkg.csv')

    # 调用def_baggage_666中的函数, 绘制图片并保存指定格式和文件名
    # 可用格式为:
    # eps, pdf, pgf, png, ps, raw, rgba, svg, svgz
    db6.painting_trees(patch_trees,'result.eps')
    db6.painting_trees(patch_trees_bkg,'result_bkg.eps')

    # 执行结束释放资源
    # 这一步依旧会报错: 'Segmentation fault: 11'
    # 但不管了反正东西都拿到了
    cap.release()

    # 返回帧数供日后调用
    return(n_frames)

# 视频分析V2
# NB 改进区域:
# - 使得每次分析时能够导出一张图片, 图片中分析区域用红色覆盖, 以确保分析区域正确
def pixel_record_1(input_path, r_s, mode = False, frame_interval = 25):
    # 列出文件夹下所有的视频文件
    filenames = os.listdir(input_path)

    # 获取文件夹名称
    video_prefix = input_path.split(os.sep)[-1]

    # 建立一个新的文件夹，名称为原文件夹名称后加上_frames
    if mode == True:
        frame_path = '{}_frames'.format(input_path)
        if not os.path.exists(frame_path):
            os.mkdir(frame_path)

    # 初始化一个VideoCapture对象
    cap = cv2.VideoCapture()

    # 遍历所有文件
    for filename in filenames:
        filepath = os.sep.join([input_path, filename])

        # VideoCapture::open函数可以从文件获取视频
        cap.open(filepath)

        # 获取视频帧数
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print('视频帧数为: ', n_frames)
        # 同样为了避免视频头几帧质量低下，黑屏或者无关等, 可用以下代码改变参数'42', 跳过这几帧
        # for i in range(42):
        #     cap.read()

        # 调用第一帧, 获取视频基本信息
        nap,frame = cap.read()
        if nap == True:
            print('获得视频nda基本信息: ', np.shape(frame))
            imagename = 'start.jpg'.format(video_prefix, filename.split('.')[0])
            imagepath = os.sep.join([frame_path, imagename])
            print('exported {}!'.format(imagepath))
            frame[r_s[0]:r_s[1],r_s[2]:r_s[3],:] = 255
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

        for i in tqdm(range(int(n_frames))):

            # 按帧读取每一帧的RGB
            # 例子:
            # >>> np.shape(frame)
            # >>> (1920,1080,3)
            nap, frame = cap.read()

            # 一定要加上这句话, 否则会报错: 'Segmentation fault: 11'
            if nap == True:

                # 获取需要分析的位置范围
                patch_tree_target = frame[r_s[0]:r_s[1],r_s[2]:r_s[3],:]

                # 获取分析位点下30个像素点作为参考
                patch_tree_bkg = frame[(r_s[0]+15):(r_s[1]+15),r_s[2]:r_s[3],:]


                # # 每隔frame_interval帧进行一次截屏操作, 并保存到新的文件夹中
                # if mode = True:
                #     if i % frame_interval == 0:
                        # imagename = '{}_{}_{:0>6d}.jpg'.format(video_prefix, filename.split('.')[0], i)
                        # imagepath = os.sep.join([frame_path, imagename])
                        # print('exported {}!'.format(imagepath))
                        # cv2.imwrite(imagepath, frame)

                # 对目标范围内求平均灰度, 获得一个数
                patch_tree_ave = np.mean(patch_tree_target)

                # 对参考范围求平均灰度, 获得一个数
                patch_tree_bkg_ave = np.mean(patch_tree_bkg)

                # 递交结果
                patch_trees.append(patch_tree_ave)
                patch_trees_bkg.append(patch_tree_bkg_ave)
            else:
                # 将假帧补为255 使得最终结果长度与视频总帧数一致
                patch_trees.append(255)
                patch_trees_bkg.append(255)

    print('patch_trees的长度为: ', len(patch_trees))

    # 调用def_baggage_666中的函数, 将列表存为csv文件
    db6.text_save_fnda(patch_trees, 'result.csv')
    db6.text_save_fnda(patch_trees_bkg, 'result_bkg.csv')

    # 调用def_baggage_666中的函数, 绘制图片并保存指定格式和文件名
    # 可用格式为:
    # eps, pdf, pgf, png, ps, raw, rgba, svg, svgz
    db6.painting_trees(patch_trees,'result.eps')
    db6.painting_trees(patch_trees_bkg,'result_bkg.eps')

    # 执行结束释放资源
    # 这一步依旧会报错: 'Segmentation fault: 11'
    # 但不管了反正东西都拿到了
    cap.release()

    # 返回帧数供日后调用
    return(n_frames)

# 对pixel_record_666的进一步分析
def record_ana(filePath_target, filePath_bkg, mode = 'Normal'):

    target_pd = pd.read_csv(filePath_target)
    bkg_pd = pd.read_csv(filePath_bkg)

    target_a = np.array(target_pd)
    bkg_a = np.array(bkg_pd)

    if mode == 'Normal':
        # 获取用来判断是否甩舌头的threshold, 设为bkg的最小值的0.9倍
        threshold = np.min(bkg_a[:,1])
        # 对patch_trees_nda做矩阵判断, 获得bool值矩阵
        target_a_judge = target_a[:,1] < threshold

    elif mode == 'Cut':
        target_a_token = target_a[:,1] - bkg_a[:,1]
        threshold = np.min(bkg_a[:,1])*0.95 # 这里0.95是我拍脑袋想出来的
        target_a_judge = target_a_token < threshold

    # NB: 获得True的段数, 并打印出来
    count_True_a = 0
    count_True_b = 0
    for num in range(len(target_a_judge)-1):
        if target_a_judge[num] == False and target_a_judge[num+1] == True:
            count_True_b = count_True_b + 1
        if target_a_judge[num] == True:
            count_True_a = count_True_a + 1
    print('True的段数为: ',count_True_b)
    print('低于阈值的信号点次数为: ', count_True_a)

    # 调用def_baggage_666中的函数, 将列表存为csv文件
    db6.text_save_fnda(target_a_judge, 'result_judge.csv')

    # 调用def_baggage_666中的函数, 绘制图片并保存指定格式和文件名
    # 可用格式为:
    # eps, pdf, pgf, png, ps, raw, rgba, svg, svgz
    db6.painting_trees(target_a_judge,'result_judge.eps')
    return()

# 分析后能够保存judge后的每一帧的图片
def pixel_record_2(input_path, r_s):
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
    for filename in filenames:
        filepath = os.sep.join([input_path, filename])

        # VideoCapture::open函数可以从文件获取视频
        cap.open(filepath)

        # 获取视频帧数
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print('视频帧数为: ', n_frames)
        # 同样为了避免视频头几帧质量低下，黑屏或者无关等, 可用以下代码改变参数'42', 跳过这几帧
        # for i in range(42):
        #     cap.read()

        # 调用第一帧, 获取视频基本信息
        nap,frame = cap.read()
        if nap == True:
            print('获得视频nda基本信息: ', np.shape(frame))
            # 保存第一帧的图片
            imagename = 'start.jpg'.format(video_prefix, filename.split('.')[0])
            imagepath = os.sep.join([frame_path, imagename])
            print('exported {}!'.format(imagepath))
            frame[r_s[0]:r_s[1],r_s[2]:r_s[3],:] = 255
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

        # 开始分析
        for i in tqdm(range(int(n_frames))):

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
                patch_tree_bkg = frame[(r_s[0]+15):(r_s[1]+15),r_s[2]:r_s[3],:]

                # 对目标范围内求平均灰度, 获得一个数
                patch_tree_ave = np.mean(patch_tree_target)

                # 对参考范围求平均灰度, 获得一个数
                patch_tree_bkg_ave = np.mean(patch_tree_bkg)

                # REVIEW 判断是否小于threshold, 保存所有小于threshold的图片
                if patch_tree_ave < patch_tree_bkg_ave * 0.95:
                    imagename = '{}_{}_{:0>6d}.jpg'.format(video_prefix, filename.split('.')[0], i)
                    imagepath = os.sep.join([frame_path, imagename])
                    print('exported {}!'.format(imagepath))
                    cv2.imwrite(imagepath, frame)
                else:
                    imagename = '{}_{}_{:0>6d}.jpg'.format(video_prefix, filename.split('.')[0], i)
                    imagepath = os.sep.join([frame_path_escaped, imagename])
                    print('exported {}!'.format(imagepath))
                    cv2.imwrite(imagepath, frame)

                # 递交结果
                patch_trees.append(patch_tree_ave)
                patch_trees_bkg.append(patch_tree_bkg_ave)
            else:
                # 将假帧补为255 使得最终结果长度与视频总帧数一致
                patch_trees.append(255)
                patch_trees_bkg.append(255)

    print('patch_trees的长度为: ', len(patch_trees))

    # 调用def_baggage_666中的函数, 将列表存为csv文件
    db6.text_save_fnda(patch_trees, 'result.csv')
    db6.text_save_fnda(patch_trees_bkg, 'result_bkg.csv')

    # 调用def_baggage_666中的函数, 绘制图片并保存指定格式和文件名
    # 可用格式为:
    # eps, pdf, pgf, png, ps, raw, rgba, svg, svgz
    db6.painting_trees(patch_trees,'result.eps')
    db6.painting_trees(patch_trees_bkg,'result_bkg.eps')

    # 执行结束释放资源
    # 这一步依旧会报错: 'Segmentation fault: 11'
    # 但不管了反正东西都拿到了
    cap.release()

    # 返回帧数供日后调用
    return(n_frames)
