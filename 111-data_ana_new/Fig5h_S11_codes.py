#!/usr/bin/env python
# coding: utf-8

# 整理一下师兄MOSD文章中我在Fig5h和S11数据分析中用到的代码
# 
# - 备注：代码还没来得及清理得好看一点；
# - 备注2：是的中间很多步没必要手动做，但是需要强迫自己检查一遍数据有没有哪里代码错漏了特殊情况...所以就保留了几个手动步骤

# In[ ]:


import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt


# 可能需要先把原始数据拼起来嗯

# In[ ]:


#先把数据拼起来
data_22_24 = pd.read_csv("area_22_24_Feb22.csv")
data_25_28 = pd.read_csv("area_25_28_Feb23.csv")

data_merge = data_22_24.append(data_25_28, ignore_index=True)
data_merge.to_csv("area_22_28_toFeb23.csv")


# 将师兄给的原始数据分开channel并添加MuscleName：
# 
#  - 注意！other tags在mouse20开始是整型，之前都是字符串形式，记得改引号！

# In[ ]:


#分开channel1和channel2，去掉噪音对应的channel，并加上对应的肌肉名的 转换格式的代码

def procdf(data_input):
    #data_output = pd.DataFrame(columns=['VoltNum', 'Trial', 'leftorright', 'Strain', 'miceNum', 'elePosition', 'ledNum', 'MuscleName', 'Result'])
    
    # 先建两个dataframe，之后一个存入channel1的数据，一个存入channel2
    data_channel1 = data_input.copy()
    data_channel1["MuscleName"] = ""
    data_channel2 = data_channel1.copy()
    
    # process channel 1
    data_channel1 = data_channel1.drop(columns=['Channel2']) #删掉channel2
    data_channel1 = data_channel1.rename(columns={"Channel1": "Result"})
    data_channel1['ChannelNum'] = 1
    
    ###################other tags在mouse20开始是整型，之前都是字符串形式，记得改引号！
    data_channel1.loc[(data_channel1.elePosition == 'C7') & ((data_channel1.miceNum == 1)|(data_channel1.miceNum == 3)|(data_channel1.miceNum == 4)), 'MuscleName'] = 'tricep'
    data_channel1.loc[(data_channel1.elePosition == 'C7') & (data_channel1.miceNum > 4) & (data_channel1.otherTags == 1), 'MuscleName'] = 'pectoralis'
    data_channel1.loc[(data_channel1.elePosition == 'C7') & (data_channel1.miceNum > 4) & (data_channel1.otherTags == 2), 'MuscleName'] = 'tricep'
    data_channel1.loc[(data_channel1.elePosition == 'C7') & (data_channel1.miceNum == 8)& (data_channel1.otherTags == 3), 'MuscleName'] = 'tricep'
    data_channel1.loc[(data_channel1.elePosition == 'C7') & (data_channel1.miceNum == 9)& (data_channel1.otherTags == 3), 'MuscleName'] = 'flexor carpi'
#     data_channel1.loc[(data_channel1.elePosition == 'Sc') & (data_channel1.miceNum != 2), 'MuscleName'] = 'tibialis anterior'
#     print(data_channel1)
    
    # process channel 2
    data_channel2 = data_channel2.drop(columns=['Channel1'])
    data_channel2 = data_channel2.rename(columns={"Channel2": "Result"}) #index=str, 
    data_channel2['ChannelNum'] = 2
    
    data_channel2.loc[(data_channel2.elePosition == 'C7') & ((data_channel2.miceNum == 1)|(data_channel2.miceNum == 3)|(data_channel2.miceNum == 4)), 'MuscleName'] = 'extensor carpi'
    data_channel2.loc[(data_channel2.elePosition == 'C7') & (data_channel2.miceNum == 2) & (data_channel2.otherTags == 2), 'MuscleName'] = 'extensor carpi'
    data_channel2.loc[(data_channel2.elePosition == 'C7') & (data_channel2.miceNum == 2) & (data_channel2.otherTags == 1), 'MuscleName'] = 'tricep'
    data_channel2.loc[(data_channel2.elePosition == 'C7') & (data_channel2.miceNum > 4) & (data_channel2.otherTags == 1), 'MuscleName'] = 'extensor carpi'
    data_channel2.loc[(data_channel2.elePosition == 'C7') & (data_channel2.miceNum > 4) & (data_channel2.otherTags == 2), 'MuscleName'] = 'digitorum'
    data_channel2.loc[(data_channel2.elePosition == 'C7') & (data_channel2.miceNum == 8) & (data_channel2.otherTags == 3), 'MuscleName'] = 'flexor carpi'
    data_channel2.loc[(data_channel2.elePosition == 'C7') & (data_channel2.miceNum == 9) & (data_channel2.otherTags == 3), 'MuscleName'] = 'extensor carpi'    
    data_channel2.loc[(data_channel2.elePosition == 'C7') & (data_channel2.miceNum > 9) & (data_channel2.otherTags == 3), 'MuscleName'] = 'flexor carpi' # Feb21新增规则：othertags3, channel2都是屈腕肌    
#     data_channel2.loc[(data_channel2.elePosition == 'Sc') & (data_channel2.miceNum == 2) & ((data_channel2.otherTags == 1)|(data_channel2.otherTags == 'jingqian')), 'MuscleName'] = 'tibialis anterior'
#     data_channel2.loc[(data_channel2.elePosition == 'Sc') & (data_channel2.miceNum == 2) & ((data_channel2.otherTags == 2)|(data_channel2.otherTags == 'feichang')), 'MuscleName'] = 'gastrocnemius'
#     data_channel2.loc[(data_channel2.elePosition == 'Sc') & (data_channel2.miceNum != 2), 'MuscleName'] = 'gastrocnemius'
    
    # join rows
    data_output = data_channel1.append(data_channel2, ignore_index=True) #后面一个变量是这样的话排序就是接着排而非直接粘贴原本的从0开始了

    data_output = data_output[data_output.MuscleName != ""] #理论上讲，没有对应肌肉名的都是噪音
        
    return(data_output)


########################### 主代码开始 #########################################

data_input = pd.read_csv("Area_result_all-0220.csv")
# print(data_input.otherTags.unique())

data_1 = procdf(data_input)

data_1.to_csv("Area_result_all-0220_spltchan.csv") #, sep='\t'

#print(datareshape_area)


# 然后加trial平均并做归一化（记得归一化根据想要如何解读结果可能需要改）

# In[ ]:


#关于ledall3: 已经重跑过可以用

data1 = pd.read_csv("area_22_28_spltchan.csv") #这里读进来的csv名字和上一个跑过的.to_csv()里面存储的文件名字一样

#如果跑了ledNum转为数字的代码的话，这里文件名是"Area_result_to_mat.csv"

#清理一下ledall的数据
data1 = data1[(data1.elePosition == "C7") & (data1.ledNum != 'ledall') & (data1.ledNum != 'ledall1') & (data1.ledNum != 'ledall2') & (data1.ledNum != 'led1all3') & (data1.ledNum != 'ledall3')] # 

mouse = data1.miceNum.unique() #这个函数可以不重复地取出某一列里所有可能值
# print(mouse)

muscle = data1.MuscleName.unique()
# print(muscle)

led = data1.ledNum.unique()
# print(led)

volt = data1.VoltNum.unique()

#加上一行Trails=0， 算trial平均值
for m in range(len(mouse)):
    for ms in range(len(muscle)):
        for v in range(len(volt)):
            for l in range(len(led)):
                data_temp = data1[(data1.ledNum == led[l]) & (data1.VoltNum == volt[v]) & (data1.miceNum == mouse[m]) & (data1.MuscleName == muscle[ms])] 
                if data_temp.empty:
                    continue
                new_row = data_temp.loc[data_temp.Trails == 1,:] #随便复制一行过来，为了填充除了Result和Trails以外的那些列的值
                new_row["Trails"] = 0
                new_row["Result"] = data_temp.Result.mean()
                data1 = data1.append(new_row,ignore_index=True)

#下面进行归一化：新建一列
data1["normResponse_eachmouse_muscle"]= 5 # 这个是初始化操作，规定数据类型是int用的；可以随便赋值一个不在[0,1]之间的数，来标示没有进行计算（因为只对平均值做归一化，其它行是不做的）

for m in range(len(mouse)): 
    for ms in range(len(muscle)):
        data_temp = data1[(data1.miceNum == mouse[m]) & (data1.MuscleName == muscle[ms])] # & (data1.Trails == 0) 不需要，因为要看实验中最大激活到什么程度
        max_temp = data_temp.Result.unique().max() #存储这个老鼠、这个肌肉下，所有值中最大的一个，作为归一化的分母
        data1.loc[(data1.miceNum == mouse[m]) & (data1.MuscleName == muscle[ms]), "normResponse_eachmouse_muscle"] = data1.Result/max_temp    
    
#存储数据
data1.to_csv("area_22_28_added_avg_n_norm.csv")


# 算selectivity index（最大-第二大）/(最大+第二大)，算最大与第二大之间的Wilcoxon P值
# 
# （这个应该可以用；不过下面这段代码我做的时候清理过，清理后的暂时找不到了，等找到补上来...）

# In[ ]:


#先加selectivity index最大和第二大的相比的图
data_alltrials = pd.read_csv("area_upto28_added_avg_n_norm.csv") 

#先取出所有不同的值，给循环备用
mouse =data_alltrials.miceNum.unique()
led = data_alltrials.ledNum.unique()
volt = data_alltrials.VoltNum.unique()
muscle = data_alltrials.MuscleName.unique()

# ANOVA结果的初始化
# data_alltrials["one-way ANOVA_1-P"] = -1
# data_alltrials["one-way ANOVA_P"] = -1
# data_alltrials["one-way ANOVA_F"] = -1
# data_alltrials["Kruskal–Wallis test_1-P"] = -1
# data_alltrials["Kruskal–Wallis test_P"] = -1
# data_alltrials["Kruskal–Wallis test_F"] = -1
# data_alltrials["Levene's P"] = -1 #注意这个不是1-P！！！！因为这个是看组间SD差异是否显著的！！！
# data_alltrials["Levene's F"] = -1
data_alltrials["SelectivityIndex_2"] = -1
data_alltrials["wilcoxon_P"] = -1
data_alltrials["wilcoxon_statistic"] = -1
data_alltrials["wilcoxon_1-P"] = -1

#再加一列存入最大值是哪块肌肉；初始化
data_alltrials["optimalMuscle"] = "none"
data_alltrials["secondaryMuscle"] = "none"


for m in range(len(mouse)):
    for l in range(len(led)):
        for v in range(len(volt)):
            data_temp = data_alltrials[(data_alltrials.miceNum == mouse[m]) & (data_alltrials.ledNum == led[l]) & (data_alltrials.VoltNum == volt[v])]
#             if data_temp.empty:
#                 continue
            if (len(data_temp.MuscleName.unique()) != 5):
                continue
            
            #然后随便复制一行，为了填充其它列（也可以手动填，主要是为了循环的那三个量，其它列之后会drop掉）
            new_row = data_temp.loc[((data_temp.Trails == 0)&(data_temp.MuscleName == "tricep")),:]
            new_row["MuscleName"] = "selectivity_2"

#             anova_temp = stats.f_oneway(data_temp[(data_temp['MuscleName'] == muscle[0]) & (data_temp.Trails != 0)].normResponse_eachmouse_muscle.unique(), 
#                                         data_temp[(data_temp['MuscleName'] == muscle[1]) & (data_temp.Trails != 0)].normResponse_eachmouse_muscle.unique(),
#                                         data_temp[(data_temp['MuscleName'] == muscle[2]) & (data_temp.Trails != 0)].normResponse_eachmouse_muscle.unique(),
#                                         data_temp[(data_temp['MuscleName'] == muscle[3]) & (data_temp.Trails != 0)].normResponse_eachmouse_muscle.unique(),
#                                         data_temp[(data_temp['MuscleName'] == muscle[4]) & (data_temp.Trails != 0)].normResponse_eachmouse_muscle.unique())
#             new_row["one-way ANOVA_1-P"] = 1-anova_temp[1]
#             new_row["one-way ANOVA_P"] = anova_temp[1]
#             new_row["one-way ANOVA_F"] = anova_temp[0]
            
#             if (m == 8) & (l=="led1") & (v==3): 
#                 print(data_temp[(data_temp['MuscleName'] == muscle[0]) & (data_temp.Trails != 0)].normResponse_eachmouse_muscle.unique())
#                 print(data_temp["normResponse_eachmouse_muscle"][(data_temp['MuscleName'] == muscle[0]) & (data_temp.Trails != 0)])
            
#             kruskal_temp = stats.kruskal(data_temp['normResponse_eachmouse_muscle'][(data_temp['MuscleName'] == muscle[0]) & (data_temp.Trails != 0)], 
#                                          data_temp['normResponse_eachmouse_muscle'][(data_temp['MuscleName'] == muscle[1]) & (data_temp.Trails != 0)],
#                                          data_temp['normResponse_eachmouse_muscle'][(data_temp['MuscleName'] == muscle[2]) & (data_temp.Trails != 0)],
#                                          data_temp['normResponse_eachmouse_muscle'][(data_temp['MuscleName'] == muscle[3]) & (data_temp.Trails != 0)],
#                                          data_temp['normResponse_eachmouse_muscle'][(data_temp['MuscleName'] == muscle[4]) & (data_temp.Trails != 0)])
#             new_row["Kruskal–Wallis test_1-P"] = 1-kruskal_temp[1]
#             new_row["Kruskal–Wallis test_P"] = kruskal_temp[1]
#             new_row["Kruskal–Wallis test_F"] = kruskal_temp[0]
            
#             levene_temp = stats.levene(data_temp['normResponse_eachmouse_muscle'][(data_temp['MuscleName'] == muscle[0]) & (data_temp.Trails != 0)], 
#                                        data_temp['normResponse_eachmouse_muscle'][(data_temp['MuscleName'] == muscle[1]) & (data_temp.Trails != 0)],
#                                        data_temp['normResponse_eachmouse_muscle'][(data_temp['MuscleName'] == muscle[2]) & (data_temp.Trails != 0)],
#                                        data_temp['normResponse_eachmouse_muscle'][(data_temp['MuscleName'] == muscle[3]) & (data_temp.Trails != 0)],
#                                        data_temp['normResponse_eachmouse_muscle'][(data_temp['MuscleName'] == muscle[4]) & (data_temp.Trails != 0)])
#             new_row["Levene's P"] = levene_temp[1]
#             new_row["Levene's F"] = levene_temp[0]
            
            #取出trial平均的那些行，用来找最大最小的肌肉，并计算类似DSI的selectivity index
            temp_avg = data_temp[(data_temp.Trails == 0)] #不包括new_row因为new_row并没有append到data_temp里面来
            all_temp = np.sort(temp_avg.normResponse_eachmouse_muscle.unique())
            if v==3:
                print(all_temp)
            max_temp = all_temp[4]
#             min_temp = temp_avg.normResponse_eachmouse_muscle.unique().min()
            max2_temp = all_temp[3]
            new_row["SelectivityIndex_2"] = (max_temp - max2_temp)/(max_temp + max2_temp)
            #顺便记下来最大最小对应的肌肉名（这个应该有更好的方法，但反正这个也不是很慢，我就暂时先用这个了）
            temp_max = temp_avg[temp_avg["normResponse_eachmouse_muscle"] == max_temp]
            new_row["optimalMuscle"] = temp_max.MuscleName.unique()[0] #加个[0]是因为可能会有重复行（好像是因为有的othertags不同会分开算）
            temp_max2 = temp_avg[temp_avg["normResponse_eachmouse_muscle"] == max2_temp]
            new_row["secondaryMuscle"] = temp_max2.MuscleName.unique()[0] 
            
            wilcoxon_temp =  stats.ranksums(data_temp[(data_temp['MuscleName'] == temp_max.MuscleName.unique()[0]) & (data_temp.Trails != 0)].normResponse_eachmouse_muscle.unique(), 
                                            data_temp[(data_temp['MuscleName'] == temp_max2.MuscleName.unique()[0]) & (data_temp.Trails != 0)].normResponse_eachmouse_muscle.unique())
        
            new_row["wilcoxon_1-P"] = 1-wilcoxon_temp[1]
            new_row["wilcoxon_P"] = wilcoxon_temp[1]
            new_row["wilcoxon_statistic"] = wilcoxon_temp[0]
            
            data_alltrials = data_alltrials.append(new_row,ignore_index=True)
                
data_anovas1 = data_alltrials[(data_alltrials.MuscleName == "selectivity_2")].copy()
data_anovas = data_anovas1[["miceNum", "ledNum", "VoltNum", "SelectivityIndex_2", "optimalMuscle", "secondaryMuscle", 
                            "wilcoxon_P", "wilcoxon_statistic", "wilcoxon_1-P"]].copy()
#以上两行感觉应该可以合起来，但我直接合起来会报错，所以就先分开写了

data_anovas.to_csv("area_upto28_norm_selectivity2_dsi.csv")

#这个输出的数据我挑了一个手动算过了是对的，不知道为啥打印出来的这么诡异。。
#啊哈！因为v==3不是VoltNum==3


# 顺便看一下所有小鼠所有肌肉所有给光组合的selectivity index的分布情况

# In[ ]:


# 做直方图：
data_hist = pd.read_csv("area_upto28_norm_selectivity2_dsi.csv")

all_si2 = data_hist.SelectivityIndex_2.unique()

all_si2_median = np.median(all_si2)
all_si2_std = np.std(all_si2)
all_si2_mean = np.std(all_si2)

print("median:")
print(all_si2_median)
print("mean:")
print(all_si2_mean)
print("std:")
print(all_si2_std)

cutoff = all_si2_median + 2 * all_si2_std

sns.distplot(all_si2, kde=False, bins=20, fit=stats.expon, norm_hist = True)
plt.axvline(x=cutoff, color = "b")
plt.xlim(0,1)
plt.ylabel("Density")
plt.xlabel("selectivity index = (max-second_max)/(max+second_max)")

print("cutoff = median + 2 * std:")
print(cutoff)

# (mu, sigma) = stats.norm.fit(e_t_hat)
# print "mu={0}, sigma={1}".format(mu, sigma)

plt.savefig("selectivity2_distribution_expon-fitted_median2std.png")
plt.savefig("selectivity2_distribution_expon-fitted_median2std.eps")
plt.show()


# 做Fig 5h的柱状图，顺便算ANOVA

# In[ ]:


# 每块肌肉画一张图！！！

data_grouped = pd.read_csv("selectivity2_groupbyoptmuscle.csv")

f, axarr = plt.subplots(5,1,figsize=(5.5,10)) #顺序：几行，几列，figsize=（总横宽，总纵长）
f.tight_layout() #调节构图不要太挤

muscle = ["pectoralis", "tricep", "extensor carpi", "flexor carpi", "digitorum"]
print(muscle)

#pec:
plt.subplot(5,1,1)
data_pec = data_grouped[(data_grouped.optimalMuscle == "pectoralis")]
sns.barplot(x="MuscleName", y="normResponse_eachmouse_muscle", data=data_pec, ci=68, color="lightcoral",errwidth=2, capsize=.1, order=["pectoralis", "tricep", "extensor carpi", "flexor carpi", "digitorum"]) #ci是error bar的大小，默认值是95%置信区间1000次bootstrapping
sns.stripplot(x="MuscleName", y="normResponse_eachmouse_muscle", data=data_pec, color = "dimgrey", size=3, order=["pectoralis", "tricep", "extensor carpi", "flexor carpi", "digitorum"])
plt.xlabel("pectoralis")
plt.ylabel("normalized area")

#tri:
plt.subplot(5,1,2)
data_tri = data_grouped[(data_grouped.optimalMuscle == "tricep")]
sns.barplot(x="MuscleName", y="normResponse_eachmouse_muscle", data=data_tri, ci=68, color="lightcoral",errwidth=2, capsize=.1, order=["pectoralis", "tricep", "extensor carpi", "flexor carpi", "digitorum"]) #ci是error bar的大小，默认值是95%置信区间1000次bootstrapping
sns.stripplot(x="MuscleName", y="normResponse_eachmouse_muscle", data=data_tri, color = "dimgrey", size=3, order=["pectoralis", "tricep", "extensor carpi", "flexor carpi", "digitorum"])
plt.xlabel("tricep")
plt.ylabel("normalized area")

#excar:
plt.subplot(5,1,3)
data_excar = data_grouped[(data_grouped.optimalMuscle == "extensor carpi")]
sns.barplot(x="MuscleName", y="normResponse_eachmouse_muscle", data=data_excar, ci=68, color="lightcoral",errwidth=2, capsize=.1, order=["pectoralis", "tricep", "extensor carpi", "flexor carpi", "digitorum"]) #ci是error bar的大小，默认值是95%置信区间1000次bootstrapping
sns.stripplot(x="MuscleName", y="normResponse_eachmouse_muscle", data=data_excar, color = "dimgrey", size=3, order=["pectoralis", "tricep", "extensor carpi", "flexor carpi", "digitorum"])
plt.xlabel("extensor carpi")
plt.ylabel("normalized area")

#flcar
plt.subplot(5,1,4)
data_flcar = data_grouped[(data_grouped.optimalMuscle == "flexor carpi")]
sns.barplot(x="MuscleName", y="normResponse_eachmouse_muscle", data=data_flcar, ci=68, color="lightcoral",errwidth=2, capsize=.1, order=["pectoralis", "tricep", "extensor carpi", "flexor carpi", "digitorum"]) #ci是error bar的大小，默认值是95%置信区间1000次bootstrapping
sns.stripplot(x="MuscleName", y="normResponse_eachmouse_muscle", data=data_flcar, color = "dimgrey", size=3, order=["pectoralis", "tricep", "extensor carpi", "flexor carpi", "digitorum"])
plt.xlabel("flexor carpi")
plt.ylabel("normalized area")

#digi:
plt.subplot(5,1,5)
data_digi = data_grouped[(data_grouped.optimalMuscle == "digitorum")]
sns.barplot(x="MuscleName", y="normResponse_eachmouse_muscle", data=data_digi, ci=68, color="lightcoral",errwidth=2, capsize=.1, order=["pectoralis", "tricep", "extensor carpi", "flexor carpi", "digitorum"]) #ci是error bar的大小，默认值是95%置信区间1000次bootstrapping
sns.stripplot(x="MuscleName", y="normResponse_eachmouse_muscle", data=data_digi, color = "dimgrey", size=3, order=["pectoralis", "tricep", "extensor carpi", "flexor carpi", "digitorum"])
plt.xlabel("digitorum")
plt.ylabel("normalized area")

plt.savefig("groupbymuscle.png")
plt.savefig("groupbymuscle.eps")
plt.show()

print(muscle[0])
anova_temp0 = stats.f_oneway(data_pec[(data_pec['MuscleName'] == muscle[0]) & (data_pec.Trails != 0)].normResponse_eachmouse_muscle.unique(), 
                             data_pec[(data_pec['MuscleName'] == muscle[1]) & (data_pec.Trails != 0)].normResponse_eachmouse_muscle.unique(),
                             data_pec[(data_pec['MuscleName'] == muscle[2]) & (data_pec.Trails != 0)].normResponse_eachmouse_muscle.unique(),
                             data_pec[(data_pec['MuscleName'] == muscle[3]) & (data_pec.Trails != 0)].normResponse_eachmouse_muscle.unique(),
                             data_pec[(data_pec['MuscleName'] == muscle[4]) & (data_pec.Trails != 0)].normResponse_eachmouse_muscle.unique())
print(anova_temp0)
# wilcoxon_temp0 = stats.wilcoxon(data_pec[(data_pec['MuscleName'] == muscle[0]) & (data_pec.Trails != 0)].normResponse_eachmouse_muscle.unique(), 
#                                 data_pec[(data_pec['MuscleName'] == muscle[1]) & (data_pec.Trails != 0)].normResponse_eachmouse_muscle.unique(),
#                                 data_pec[(data_pec['MuscleName'] == muscle[2]) & (data_pec.Trails != 0)].normResponse_eachmouse_muscle.unique(),
#                                 data_pec[(data_pec['MuscleName'] == muscle[3]) & (data_pec.Trails != 0)].normResponse_eachmouse_muscle.unique(),
#                                 data_pec[(data_pec['MuscleName'] == muscle[4]) & (data_pec.Trails != 0)].normResponse_eachmouse_muscle.unique())
# print(anova_temp0)

print(muscle[1])
anova_temp1 = stats.f_oneway(data_tri[(data_tri['MuscleName'] == muscle[0]) & (data_tri.Trails != 0)].normResponse_eachmouse_muscle.unique(), 
                             data_tri[(data_tri['MuscleName'] == muscle[1]) & (data_tri.Trails != 0)].normResponse_eachmouse_muscle.unique(),
                             data_tri[(data_tri['MuscleName'] == muscle[2]) & (data_tri.Trails != 0)].normResponse_eachmouse_muscle.unique(),
                             data_tri[(data_tri['MuscleName'] == muscle[3]) & (data_tri.Trails != 0)].normResponse_eachmouse_muscle.unique(),
                             data_tri[(data_tri['MuscleName'] == muscle[4]) & (data_tri.Trails != 0)].normResponse_eachmouse_muscle.unique())
print(anova_temp1)

print(muscle[2])
anova_temp2 = stats.f_oneway(data_excar[(data_excar['MuscleName'] == muscle[0]) & (data_excar.Trails != 0)].normResponse_eachmouse_muscle.unique(), 
                             data_excar[(data_excar['MuscleName'] == muscle[1]) & (data_excar.Trails != 0)].normResponse_eachmouse_muscle.unique(),
                             data_excar[(data_excar['MuscleName'] == muscle[2]) & (data_excar.Trails != 0)].normResponse_eachmouse_muscle.unique(),
                             data_excar[(data_excar['MuscleName'] == muscle[3]) & (data_excar.Trails != 0)].normResponse_eachmouse_muscle.unique(),
                             data_excar[(data_excar['MuscleName'] == muscle[4]) & (data_excar.Trails != 0)].normResponse_eachmouse_muscle.unique())
print(anova_temp2)

print(muscle[3])
anova_temp3 = stats.f_oneway(data_flcar[(data_flcar['MuscleName'] == muscle[0]) & (data_flcar.Trails != 0)].normResponse_eachmouse_muscle.unique(), 
                             data_flcar[(data_flcar['MuscleName'] == muscle[1]) & (data_flcar.Trails != 0)].normResponse_eachmouse_muscle.unique(),
                             data_flcar[(data_flcar['MuscleName'] == muscle[2]) & (data_flcar.Trails != 0)].normResponse_eachmouse_muscle.unique(),
                             data_flcar[(data_flcar['MuscleName'] == muscle[3]) & (data_flcar.Trails != 0)].normResponse_eachmouse_muscle.unique(),
                             data_flcar[(data_flcar['MuscleName'] == muscle[4]) & (data_flcar.Trails != 0)].normResponse_eachmouse_muscle.unique())
print(anova_temp3)

print(muscle[4])
anova_temp4 = stats.f_oneway(data_digi[(data_digi['MuscleName'] == muscle[0]) & (data_digi.Trails != 0)].normResponse_eachmouse_muscle.unique(), 
                             data_digi[(data_digi['MuscleName'] == muscle[1]) & (data_digi.Trails != 0)].normResponse_eachmouse_muscle.unique(),
                             data_digi[(data_digi['MuscleName'] == muscle[2]) & (data_digi.Trails != 0)].normResponse_eachmouse_muscle.unique(),
                             data_digi[(data_digi['MuscleName'] == muscle[3]) & (data_digi.Trails != 0)].normResponse_eachmouse_muscle.unique(),
                             data_digi[(data_digi['MuscleName'] == muscle[4]) & (data_digi.Trails != 0)].normResponse_eachmouse_muscle.unique())
print(anova_temp4)

