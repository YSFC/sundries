import requests,re
import os
import pickle
import sys
from lxml import etree
from os.path import *

URL = 'https://www.pixiv.net/ranking.php?mode=daily_r18&content=illust'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
         'referer': 'https://www.pixiv.net/'}
proxy = {'http':'socks5h://127.0.0.1:1080','https':'socks5h://127.0.0.1:1080'}
SS = requests.Session()
loginUrl = r'https://accounts.pixiv.net/login'
loginPostUrl = r'https://accounts.pixiv.net/api/login?lang=zh'

if not exists(join(split(sys.argv[0])[0],'cookies.data')):    
    loginGet = SS.get(loginUrl, headers = headers, proxies = proxy)
    keyTree = etree.HTML(loginGet.text)
    post_key = keyTree.xpath("//*[@name='post_key']")[0].attrib['value']
    postData = {                
                'pixiv_id':input('ID:'),
                'password':input('PW:'),
                'post_key':post_key,
                'return_to':'https://www.pixiv.net/'
                }
    SS.post(loginUrl, data = postData, headers = headers, proxies = proxy)
    with open('cookies.data','wb') as A:
        myCookies = pickle.dump(SS.cookies,A)
else:
    with open('cookies.data','rb') as A:
        myCookies = pickle.load(A)
    SS.cookies = myCookies

    
def get_url():
    global SS
    urlList = []
    res = SS.get(URL, headers = headers, proxies = proxy)
    selector = etree.HTML(res.text)    
    for i in range(1,51):
        #print(selector.xpath('//*[@id={}]/div[2]/a/@href'.format(i))[0])
        urlList.append(selector.xpath('//*[@id={}]/div[2]/a/@href'.format(i))[0])
    return urlList

def get_data(urls):
    global SS
    urlHead = 'https://www.pixiv.net'
    for url in urls:
        res = SS.get(urlHead+url, headers = headers, proxies = proxy)
        #with open('2.html','wb') as A:
            #A.write(res.content)
        imgUrl = re.findall(r'"original":"(http.+?img-original/img/20[^\.]+?\...g)"',res.text.replace(r'\/','/'))
        if imgUrl == []:
            print("Error:{}".format(url))
            continue
        imgPage = re.findall(r'"pageCount":(\d+),',res.text)[-1]        
        for I in range(int(imgPage)):
            imgUrl_T = imgUrl[0].replace('_p0','_p{}'.format(I))
            saveName = imgUrl_T.split('/')[-1]
            getPic = SS.get(imgUrl_T, headers = headers, proxies = proxy)
            with open(join(split(sys.argv[0])[0],saveName),'wb') as A:
                A.write(getPic.content)
            
        print('已获取文件：{}'.format(saveName))

def main():
    urlList = get_url()
    get_data(urlList)

if __name__=='__main__':
    main()





