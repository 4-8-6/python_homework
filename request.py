import requests
import os
import re
import time
import random
import json
from PIL import Image
from train import resize

#定义一个爬虫类
class crawler():
    #爬虫项目初始化
    #tex:表示项目的名字
    #dic一个字典保存键值对（英文单词：中文单词）
    #num表示准备爬取的数量
    def __init__(self,name:str,dic:dict,num=150):
        self.name = name
        self.dic = dic
        self.num = num
        if not os.path.exists('projects'):
            os.mkdir('projects')
        if os.path.exists(os.path.join('projects',self.name)):
            self.ch = False
        else:
            self.ch = True
            os.mkdir(os.path.join('projects',self.name))
            oth = {}
            for i in sorted(dic.keys()):
                oth[i] = len(oth)
            f = open(os.path.join('projects',self.name,'config.json'),'w',encoding='utf-8')
            json.dump(oth,f)
            f.close()
            for k in dic.keys():
                os.mkdir(os.path.join('projects',self.name,k))

    #开始爬取内容
    #从百度之中爬取文件，一页会有30张对应的照片
    #对字典的内容
    def craw(self,size=64):
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0',
          'Referer':'https://www.baidu.com',}
        step = self.num/4
        for k,v in self.dic.items():
            num = 0   #保存爬取的照片爬取的数量，当爬取到足够数量停止爬虫
            offset = 0
            url = 'https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&dyTabStr=MCwzLDYsMSw0LDUsOCw3LDIsOQ%3D%3D&word='
            while True:
                offset += random.randint(2,5) * 30
                url_use = url + v + '&pn=' + str(offset)
                req = requests.get(url_use,headers=header)
                assert req.status_code == 200
                text = req.text
                url_re = re.compile('"thumbURL":"(.*?)","adType"')
                url_list = url_re.findall(text)
                for url_found in url_list:
                    try:
                        img_req = requests.get(url_found,headers=header,timeout=30)
                        img_req.raise_for_status()
                    except:
                        continue
                    time.sleep(random.random()/2)
                    if img_req.status_code != 200:
                        continue
                    else:
                        num += 1
                        s = str(num) + '.jpg'
                        file_name = os.path.join('projects',self.name,k,s)
                        with open(file_name,'wb') as f:
                            f.write(img_req.content)
                    if num % step == 0:
                        print('{}:{}/{}'.format(k,num,self.num))
                    if num == self.num:
                        break
                if num == self.num:
                    #将图形进行压缩
                    for name in os.listdir(os.path.join('projects',self.name,k)):
                        file_name = os.path.join('projects', self.name, k, name)
                        img = Image.open(file_name)
                        img = img.convert('RGB')
                        img = img.resize((resize,resize))
                        img.save(file_name)
                    print("{}:capture has complete".format(k))
                    break
        print("craw complete")



    def check(self):
        return self.ch

def main():
    craw1 = crawler('first',{'cat':'一只猫','dog':'一只狗','chicken':'一只鸡'})
    craw1.craw()
if __name__ == '__main__':
    main()