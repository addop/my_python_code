import cv2
import os
import sys
import numpy as np
from tqdm import tqdm
import copy

import def_baggage_666 as db6

# 视频分析
def pixel_record_666(input_path, r_s, bkg, mode = False, frame_interval = 25):
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

        for i in tqdm(range(int(n_frames))):

            # 按帧读取每一帧的RGB
            # 例子:
            # >>> np.shape(frame)
            # >>> (1920,1080,3)
            nap, frame = cap.read()

            # 一定要加上这句话, 否则会报错: 'Segmentation fault: 11'
            if nap == True:

                # 获取需要分析的位置范围和需要剪去的噪音
                patch_tree_target = frame[r_s[0]:r_s[1],r_s[2]:r_s[3],:]
                patch_tree_bkg = frame[bkg[0]:bkg[1],bkg[2]:bkg[3],:]



                # # 每隔frame_interval帧进行一次截屏操作, 并保存到新的文件夹中
                # if mode = True:
                #     if i % frame_interval == 0:
                #         imagename = '{}_{}_{:0>6d}.jpg'.format(video_prefix, filename.split('.')[0], i)
                #         imagepath = os.sep.join([frame_path, imagename])
                #         print('exported {}!'.format(imagepath))
                #         cv2.imwrite(imagepath, frame)

                # 对范围内求平均灰度, 获得一个数
                patch_tree_ave = np.mean(patch_tree_target)
                patch_tree_bkg_ave = np.mean(patch_tree_bkg)

                # 将ave和bkg的值相减, 以去掉背景噪音的影响
                patch_tree_ave_r = patch_tree_ave - patch_tree_bkg_ave

                # 递交结果
                patch_trees.append(patch_tree_ave_r)


    print('patch_trees的长度为: ', len(patch_trees))


    # 调用def_baggage_666中的函数, 将列表存为txt文件
    # db6.text_save(patch_trees, 'result.txt')
    db6.text_save_fnda(patch_trees, 'result.csv')

    # 调用def_baggage_666中的函数, 绘制图片并保存指定格式和文件名
    # 可用格式为:
    # eps, pdf, pgf, png, ps, raw, rgba, svg, svgz
    db6.painting_trees(patch_trees,'result.eps')

    # 执行结束释放资源
    # 这一步依旧会报错: 'Segmentation fault: 11'
    # 但不管了反正东西都拿到了
    cap.release()
