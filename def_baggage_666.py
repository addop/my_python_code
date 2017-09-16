import matplotlib.pyplot as plt
from tqdm import tqdm

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
    import numpy as np
    a = np.empty([len(content),2])
    a[:,0] = np.array(range(len(content)))
    a[:,1] = np.array(content)
    np.savetxt(filename, a, delimiter=",")
    print('txt saving good')
    return()
