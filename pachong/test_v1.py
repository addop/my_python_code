import re
import requests

s = requests.session()
h = s.get('http://www.zhihu.com/topic/19554091/questions?page=1')
html = h.content
print(html)