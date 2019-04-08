import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib


def change_matplot_words():
    # 指定默认字体
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['font.family']='sans-serif'
    # 解决负号'-'显示为方块的问题
    matplotlib.rcParams['axes.unicode_minus'] = False


# 抓取网页
def get_url(url, params=None, proxies=None):
    rsp = requests.get(url, params=params, proxies=proxies)
    rsp.raise_for_status()
    return rsp.text


class fund_manager:
    def __init__(self):

        self.url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx'
        self.code = None
        self.per = None
        self.sdate = None
        self.edate = None
        self.params = None
        self.proxies = None
        self.html = None
        self.soup = None

        self.fund_num = None

        self.pages = None
        self.heads = []
        self.records = []

        self.data = pd.DataFrame()

    def read_csv(self, csv_read_path):
        '''
        输出基金的列表
        :param csv_read_path: 基金存储的csv位置
        :return: 返回基金列表
        '''
        self.fund_num = pd.read_csv(csv_read_path, dtype='str')['MyFund']

    def download(self, code, per, sdate, edate):
        self.code = code
        self.per = per
        self.sdate = sdate
        self.edate = edate
        self.params = {'type': 'lsjz', 'code': code, 'page': 1, 'per': per, 'sdate': sdate, 'edate': edate}
        self.proxies = None
        self.html = get_url(self.url, self.params, self.proxies)
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def get_pages(self):
        pattern = re.compile(r'pages:(.*),')
        result = re.search(pattern, self.html).group(1)
        self.pages = int(result)

    def get_heads(self):
        for head in self.soup.findAll("th"):
            self.heads.append(head.contents[0])

    def get_info_from_pages(self):
        # 从第1页开始抓取所有页面数据
        page = 1
        while page <= self.pages:
            self.params = {'type': 'lsjz', 'code': self.code,
                           'page': page, 'per': self.per,
                           'sdate': self.sdate, 'edate': self.edate}
            self.html = get_url(self.url, self.params, self.proxies)
            self.soup = BeautifulSoup(self.html, 'html.parser')

            # 获取数据
            for row in self.soup.findAll("tbody")[0].findAll("tr"):
                row_records = []
                for record in row.findAll('td'):
                    val = record.contents

                    # 处理空值
                    if not val:
                        row_records.append(np.nan)
                    else:
                        row_records.append(val[0])

                # 记录数据
                self.records.append(row_records)

            # 下一页
            page = page + 1

    def to_dataframe(self):
        # 数据整理到dataframe
        np_records = np.array(self.records)
        for col, col_name in enumerate(self.heads):
            self.data[col_name] = np_records[:, col]

    def to_csv(self):
        pass


dog = fund_manager()
dog.read_csv('/Users/zhenghao/Documents/git/my_python_code/股票投资/myfund.csv')
# print(dog.fund_num)
dog.download(dog.fund_num[0], 49, '2019-01-01', '2019-4-1')
dog.get_pages()
dog.get_heads()
dog.get_info_from_pages()
dog.to_dataframe()
print(dog.data)
