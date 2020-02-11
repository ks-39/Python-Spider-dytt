import json
from multiprocessing.pool import Pool

import requests
from bs4 import BeautifulSoup

headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
}


def get_page(url):
    html = requests.get(url,headers=headers)
    html.encoding = 'gbk'
    return html

def parse_page(html):
    try:
        soup1 = BeautifulSoup(html.text,'html.parser')    # bs转化html  --- soup = BeautifulSoup(html.text,'html.parser')
        # print(soup)
        data1 = soup1.find_all('a',attrs={'class':'ulink'})   # 提取排行榜里电影的具体页面html
        for i in data1:   # 遍历网址
            detail_html = 'https://www.dytt8.net'+ i.get('href')   # 补全网址
            html2 = requests.get(detail_html,headers=headers)   # 提取html
            html2.encoding = 'gbk'
            soup2 = BeautifulSoup(html2.text,'html.parser')   # 解析html
            for td in soup2.find_all('td',attrs={'style': 'WORD-WRAP: break-word'}):   # 使用soup.find_all 第一次定位 (无法换行查找?)
                for i in td.find_all('a'):      # 第二次定位
                    info = {
                        "ftp" : i['href']  # 提取内容（bs无text（）属性)
                    }
                    print(info)
                    # save_to_file(info)
    except UnicodeEncodeError:
        pass
    except TimeoutError and requests.exceptions.ConnectionError:
        return parse_page(html)

def save_to_file(content):      #不知道为什么没有输出为txt文件。。。
    with open('(电影天堂)requests+bs.txt','a',encoding='utf-8')as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def main(page_number):
    url = "https://www.dytt8.net/html/gndy/dyzz/list_23_" + str(page_number) + ".html"
    html = get_page(url)
    parse_page(html)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i for i in range(0,50)]) #爬取页数：0-50