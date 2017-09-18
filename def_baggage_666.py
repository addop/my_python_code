import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import numpy as np

def painting_trees(list_result,filename):
    plt.figure(figsize=(30,3))# figsize不能过大, 想要清楚就去改dpi
    plt.plot(list_result, 'k')
    plt.savefig(filename, dpi = 300, bbox_inches = 'tight')
    print('exported: ', filename)


# 将列表保存成txt文件
# http://blog.csdn.net/Innovation_Z/article/details/51113664
# 注意是列表
def text_save(content,filename,mode='a'):
    # Try to save a list variable in txt file.
    file = open(filename,mode)
    for i in tqdm(range(len(content))):
        file.write(str(content[i])+'\n')
    file.close()
    print('exported: ',filename)
    return()

# 将列表保存成csv文件
# https://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html
# 其中将列表转换成了矩阵
def text_save_fnda(content,filename):
    token = np.array(content)
    size_token = np.shape(token)
    if len(size_token) == 1:
        a = np.empty([len(content), 2])
        a[:,0] = np.array(range(len(content)))
        a[:,1] = np.array(content)
    else:
        a = np.empty([size_token[0], size_token[1]+1])
        a[:,0] = np.array(range(len(content)))
        a[:,1:] = np.array(content)
    np.savetxt(filename, a, delimiter=",")
    print('exported: ', filename)
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

def second2minsec(nda):
    import time
    if len(np.shape(nda)) == 1:
        a = []
        for index in range(len(nda)):
            a.append(time.strftime('%H:%M:%S', time.gmtime(nda[index])))
        print('时间转换完毕, 请将结果转换为list保存成csv')
    else:
        print('提供给 second2minsec 的矩阵只能是一维, 请更改后使用')
    return(a)
