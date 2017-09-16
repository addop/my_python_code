import matplotlib.pyplot as plt
from tqdm import tqdm

a = 


plt.figure(figsize=(500,50))
plt.plot(list_result, 'k')
plt.savefig(filename, dpi = 100, bbox_inches = 'tight')
print('图像保存完毕')
