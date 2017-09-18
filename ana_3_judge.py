# NB 对大家的csv数据进行分析
import numpy as np
import def_baggage_666 as db6
import main_function as mf

filePath_target = '/Users/zhenghao/Documents/pythonfile/my_python_code/result.csv'
filePath_bkg = '/Users/zhenghao/Documents/pythonfile/my_python_code/result_bkg.csv'
mf.record_ana(filePath_target, filePath_bkg, mode = 'real_time', threshold_condition = 0.95)
