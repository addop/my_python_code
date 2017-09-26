# eye movement
# -*- coding:utf-8 -*-
import cv2
import numpy as np

input_path ='/Users/zhenghao/Desktop/a.mov'
rectangleCols = 30

camera = cv2.VideoCapture()
camera.open(input_path)
n_frames = int(camera.get(cv2.CAP_PROP_FRAME_COUNT))
print('Frame: ', n_frames)
nap,frame = camera.read()
print(np.shape(frame))

for i in tqdm(range(int(n_frames))):
    nap,frame = camera.read()
    if nap == True:
        


camera.release()
cv2.destroyAllWindows()
