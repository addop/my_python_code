import urllib
import urllib.request
import gzip

def pachong1(keyword,filepath):
    data={}
    data['word']=keyword

    url_values=urllib.parse.urlencode(data)
    url="https://www.google.com.hk/search?"
    full_url=url+url_values

    data=urllib.request.urlopen(full_url).read()

    # data=data.decode('UTF-8')
    # data=data.decode('ASCII')
    print(data)

    # open(filepath,'w').write(data)

def searchGoogle(word,filepath):
    #设置url
    url="https://www.google.com/search?"
    #伪装浏览器环境
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers={'User-Agent':user_agent}

    #传入关键词,百度的关键词标签是wd
    values={'q':word}
    #转码
    urlf=url+urllib.parse.urlencode(values)
    #print urlf

    #取结果
    response=urllib.request.urlopen(urlf)
    html=response.read()

    #保存文件
    open(filepath,'w').write(html)

pachong1('张姝','/Users/zhenghao/Desktop/test.txt')
