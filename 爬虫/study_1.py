from urllib import request
from bs4 import BeautifulSoup
import collections
import re
import os
import time
import sys
import types


"""
类说明:下载《笔趣看》网小说: url:https://www.biqukan.com/
Parameters:
    target - 《笔趣看》网指定的小说目录地址(string)
Returns:
    无
Modify:
    2017-05-06
"""


class download(object):

    def __init__(self, target):
        self.__target_url = target
        self.__head = {'User-Agent':'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19',}

