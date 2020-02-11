import json
from multiprocessing.pool import Pool

import requests
from pyquery import PyQuery as pq

headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
}


def get_page(url):
    html = requests.get(url,headers=headers)
    html.encoding = 'gbk'
    return html.text

def parse_page(html):
    try:
        doc1 = pq(html)   # pyquery解析方式：doc = pq(html)
        for i in doc1('b a'):   # 1、遍历定位到标签
            i = doc1(i).attr('href')  # 2、查找属性为'href'的元素，即电影详细页面的url
            detail_html = 'https://www.dytt8.net' + str(i)   # 补全电影详细页面的html

            html2 = requests.get(detail_html,headers=headers)
            html2.encoding = 'gbk'
            doc2 = pq(html2.text)   # 解析电影详细页面的html

            data = doc2('#Zoom a:contains("ftp")').text()   # id为Zoom 标签为a 包含‘ftp’的内容。.text()打印出内容
            print("url:",data)
            save_to_file(data)
    except UnicodeEncodeError:
        pass
    except TimeoutError and requests.exceptions.ConnectionError:
        return parse_page(html)

def save_to_file(content):
    with open('(电影天堂)requests+pyquery.txt','a',encoding='utf-8')as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def main(page_number):
    url = "https://www.dytt8.net/html/gndy/dyzz/list_23_" + str(page_number) + ".html"
    html = get_page(url)
    parse_page(html)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i for i in range(0,50)])
