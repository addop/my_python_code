# 获取图片矩阵
import cv2
import numpy as np
import def_bag as db

FilePath = '/Users/zhenghao/Desktop/a.tif'
showima = False


image = cv2.imread(FilePath, 0)# load image. NOTE: 这个LoadImage没法用, 只能用imread方案
print(np.shape(image))
db.saveimage(image, 3)
