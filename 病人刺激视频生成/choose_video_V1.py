import cv2
import os
import random
import time


input_path = '/Volumes/HaoZHD4/病人刺激视频/实验视频/SEEG_stim_video'
# 列出文件夹下所有的视频文件
filenames = os.listdir(input_path)
# 获取文件夹名称
video_prefix = input_path.split(os.sep)[-1]
# 建立一个新的文件夹，名称为原文件夹名称后加上_frames
frame_path = '{}_stim'.format(input_path)

# 总数
# 筛选filenames
filenames_video = []
for filename in filenames:
    if filename.split('.')[-1] == 'mp4' and len(filename.split('.')) == 2:
        filenames_video.append(filename)
video_pool_num = len(filenames_video)
print('池子中总共',video_pool_num,'个视频')

# 生成随机数
fishes = []
for i in range(40):
    fishes.append(random.randint(0, video_pool_num-1))
print('fishes len',len(fishes))
# 按随机数获取列表
fishes_catch = []
for fish in fishes:
    fishes_catch.append(filenames_video[fish])

# 将取出的视频做成一个完整的视频
# 初始化一个VideoCapture对象
cap = cv2.VideoCapture()

# 初始化视频
fourcc = cv2.VideoWriter_fourcc(*'XVID')
savename_main = input_path.split('/')[-1]
# 获取时间
TAG = time.localtime()
time_val = str(TAG.tm_year)+str(TAG.tm_mon)+str(TAG.tm_mday)+'-'+str(TAG.tm_hour)+'H'+str(TAG.tm_min)+'M'
savename = savename_main + '_mix_'+time_val+'.mov'
out = cv2.VideoWriter(savename,fourcc, 25.0, (960,540)) # 帧数可调, 注意后面的尺寸大小要一致

file = open('video_name_'+savename+'.txt','w');file.write(str(fishes_catch));file.close();


for fish_catch in fishes_catch:
    # 导入灰色背景和光栅提醒
    cap.open('SEEG_stim_video/光栅/光栅.mp4')
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('光栅>>>Frame:', n_frames)
    for n_frame in range(n_frames):
        if n_frame <1:
            continue
        nap, frame = cap.read()
        out.write(frame)

    # VideoCapture::open函数可以从文件获取视频
    cap.open('SEEG_stim_video/'+fish_catch)
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(fish_catch,'>>>Frame:', n_frames)

    for n_frame in range(n_frames):
        if n_frame >= 75:
            continue
        # if n_frame < 25:
        #     continue
        nap, frame = cap.read()
        # frame_cut = frame[540:,:]
        # print(np.shape(frame_cut))
        out.write(frame)

out.release()# 导出视频时释放
