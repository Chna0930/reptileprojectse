import requests
from bs4 import BeautifulSoup
import json
from lxml import etree
import os
import datetime
# id获取
def getMusicId():
    url = 'https://music.163.com/discover'
    headers = {
    'Cookie': '_iuqxldmzr_=32; _ntes_nnid=7eb51552d5d4478669c6c5ec6f12dfff,1621428628585; _ntes_nuid=7eb51552d5d4478669c6c5ec6f12dfff; NMTID=00On2_Ho1af1EoCUkYhkbLrH1zSPMMAAAF5hK1rbw; WEVNSM=1.0.0; WM_TID=AFs65iudA4JBVFVQAUc%2Fw8UliPI5vssq; JSESSIONID-WYYY=t93PiQv9bfQOwYSSSGeeKO45tPi0lVlsBvPgd6ol0QR8VISe7uGRvB6bRKb33rapggo1Tfv9wjq36jlYui9i02E%2Bsz9dSXyKgvYTAFljJJTJ%5CsaXvQNcm5TToVBMAdHmOgq2%2Fn8ogBOjnaZ3pjFeFFrCsme89otbw%2Bv4iIDUPGEnxdxH%3A1622982313933; WNMCID=zzcmaq.1622980514474.01.0; WM_NI=eNTwP1i3Cpx1XXPuRw20m%2BvZpgPt453OmGlHTjLHuWP1OvzER0VsiQz38aOXVSjdTzU209BEdoJ5HO1sc4XICH8xrGyF7TaTVOpbEM5uSqP9fRi4Nh25pNu1jdr%2FkZjbaVg%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea3f269aa8d8287d443b78e8eb3d45e839b8fbaaa3beda999b4ca46ab8db6a3f62af0fea7c3b92aa7929c98d33babed8d91fb3b9c88a096d17df2f0a3ccf552b4b9a095b73ff191a3a8ef4498b684a9f85d94ef8197f94f92f09a94ec5bbaedf882ce54968da685d77297ee00dac14fa8b186d6cb45f3adadd5db438198f899f14dbb9af9b5e4609691c083c847f7ab9d92d333a68ea7d5cd64f2ebc0aff83baabcbed0ea52aabeafb7e637e2a3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }
    mainPage = requests.get(url=url,headers=headers).text
    tree = etree.HTML(mainPage)
    tree_list = tree.xpath('//div[@id="top-flag"]/dl/dd/ol/li')
    musicUpList = []
    for tr in tree_list:
        musicId =  tr.xpath('.//a/@href')[0][9:]
        musicName =  str(tr.xpath('.//a/@title')[0])
        musicInfo = []
        musicInfo.append(musicId)
        musicInfo.append(musicName)
        musicUpList.append(musicInfo)
    return musicUpList

def dealUpMusic(musicUpList):
    #---------------文件创建---------
    if not os.path.exists('./爬虫项目/comment/Up/'):
        os.mkdir('./爬虫项目/comment/Up/')
    if not os.path.exists('./爬虫项目/comment/New/'):
        os.mkdir('./爬虫项目/comment/New/')
    if not os.path.exists('./爬虫项目/comment/Original/'):
        os.mkdir('./爬虫项目/comment/Original/')
    #---------------评论收集--------
    url = "http://music.163.com/api/v1/resource/comments/R_SO_4_"
    # 飙升榜
    for i in range(0,9):
        commentlist = []
        musicId = musicUpList[i][0]
        path    = './爬虫项目/comment/Up/'+musicUpList[i][1]+'.txt'
        commentGet(musicId,url,commentlist)
        save(commentlist,path)
    print("飙升榜打印完毕")
     # 新歌榜
    for i in range(10,19):
        commentlist = []
        musicId = musicUpList[i][0]
        path    = './爬虫项目/comment/New/'+musicUpList[i][1]+'.txt'
        commentGet(musicId,url,commentlist)
        save(commentlist,path)
    print("新歌榜打印完毕")  
    # 原创榜
    for i in range(20,29):
        commentlist = []
        musicId = musicUpList[i][0]
        path    = './爬虫项目/comment/Original/'+musicUpList[i][1]+'.txt'
        commentGet(musicId,url,commentlist)
        save(commentlist,path)
    print("原创榜打印完毕")
# 获取评论页面内容
def getText(url):
    try:
        kv = {"user-agent":"Mozilla/5.0"}
        r = requests.get(url,headers = kv)
        r.raise_for_status()
        return r.text
    except:
        print("获取页面失败")
        return ""
# 获取评论
def commentGet(musicId,url,commentlist):
    for i in range(12):
        new_url = url + "{0}?limit=100&offset={1}".format(musicId,100*i)
        html = getText(new_url)
        json_dict = json.loads(html)        #利用json方法把json类型转成dict
        comments = json_dict['comments']
        for item in comments:
            try:
                times     = datetime.datetime.fromtimestamp(int(str(item['time'])[0:-3]))
                commetTime = times.strftime("%Y-%m-%d %H:%M:%S")
                commentlist.append([item['user']['nickname'],item['content'],commetTime])
                print("时间"+commetTime+":"+item['user']['nickname'] + "评论了：" + item['content'])
            except:
                print("特殊字符打印失败！！！")
                continue
# 保存评论到文件中
def save(commentlist,path):
    with open (path,'a',encoding = 'utf-8') as f:
        for comment in commentlist:
            f.write("时间"+comment[2]+comment[0] + "评论了: " + comment[1] + "\n")
    f.close()

def main():
    dealUpMusic(getMusicId())
    
main()
