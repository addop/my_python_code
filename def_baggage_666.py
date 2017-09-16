import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import numpy as np

def painting_trees(list_result,filename):
    plt.figure(figsize=(500,50))
    plt.plot(list_result, 'k')
    plt.savefig(filename, dpi = 100, bbox_inches = 'tight')
    print('图像保存完毕')


# 将列表保存成txt文件
# http://blog.csdn.net/Innovation_Z/article/details/51113664
# 注意是列表
def text_save(content,filename,mode='a'):
    # Try to save a list variable in txt file.
    file = open(filename,mode)
    for i in tqdm(range(len(content))):
        file.write(str(content[i])+'\n')
    file.close()
    print('txt saving good')
    return()

# 将列表保存成csv文件
# https://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html
# 其中将列表转换成了矩阵
def text_save_fnda(content,filename):
    a = np.empty([len(content),2])
    a[:,0] = np.array(range(len(content)))
    a[:,1] = np.array(content)
    np.savetxt(filename, a, delimiter=",")
    print('txt saving good')
    return()

def eye_csv_read(filePath, video_len):
    # 导入csv
    df = pd.read_csv(filePath)
    # 设立空矩阵
    df_nda = np.empty([video_len, 2])
    # 对空矩阵进行设置
    df_nda[:,0] = np.array(range(video_len))
    df_nda[:,1] = 0
    # 将导入的csv数据转化为矩阵
    df_nda_token = np.array(df)
    # 将数据的第一列的值换算成帧
    df_nda_token[:,0] = df_nda_token[:,0] * 25
    # 将数据中的第一列的值与空矩阵的第一列匹配, 并将对应的第二列赋值为1
    for item in df_nda_token[:,0]:
        df_nda[int(item),1] = 1
    # 函数返回矩阵
    return(df_nda)
