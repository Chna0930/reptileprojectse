import requests
from lxml import etree
import requests
headers={
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
}
fp = open("ipPool.txt",'w',encoding='utf-8')
for i in range(1,2001):
    url = 'http://www.xiladaili.com/gaoni/'+str(i)+'/'
    respones = requests.get(url=url,headers=headers).text
    tree = etree.HTML(respones)
    tree_list_gao_ni = tree.xpath('//tbody/tr/td[1]/text()')
    for i in range(0,len(tree_list_gao_ni)):
        fp.write(tree_list_gao_ni[i]+'\n')
        print(tree_list_gao_ni[i])
fp.close()