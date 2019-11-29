import pandas as pd
import numpy as np


class gold_dog:
    def __init__(self):
        self.csv = None
        self.database = None
        self.file_path = None

    def setup(self, filepath):
        self.csv = pd.read_csv(filepath, dtype='str')
        self.clean_blank()
        print(self.csv.columns)

    def clean_blank(self):
        token_size = self.csv.shape # 这里shape不需要加括号
        for i in range(token_size[0]):
            for j in range(token_size[1]):
                token_single = self.csv.iloc[i, j]
                token_word = token_single.replace(' ', '')
                if ' ' in token_word:
                    print('no')
                self.csv.iloc[i, j] = token_word
        if ' ' in self.csv:
            print('focus! It have blank in the sheet. ')

    def read_sheet(self):
        pass


doggy = gold_dog()
doggy.setup(filepath='/Users/zhenghao/Documents/git/my_python_code/finance/finance_token_v1.csv')


