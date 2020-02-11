import json
from multiprocessing.pool import Pool

import requests
from lxml import etree

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
        data1 =etree.HTML(html)   # xpath解析html --- (var) = etree.HTML(html)
        result1 =data1.xpath('//b//a/@href')    # 提取 ：（‘//tag/tag/text（）’：相对路径、‘/tag/tag’：绝对路径、
        for i in result1:   # 遍历提取到的信息
            detail_url = 'https://www.dytt8.net' + i   # 补全电影详细页面的url
            html2 = requests.get(detail_url,headers=headers)   # 解析电影详细页面html
            html2.encoding = 'gbk'
            data2 = etree.HTML(html2.text)
            result12 = data2.xpath('//tbody/tr/td/a/@href')   # xpath解析方式(此处采用（相对路径）方式)
                                  #   亦可：('//tbody/tr/td/a/text()')
            for j in result12:
                info = {
                    "ftp":j
                }
                print(info)
                save_to_file(info)
    except UnicodeEncodeError:
        pass
    except TimeoutError and requests.exceptions.ConnectionError:
        return parse_page(html)

def save_to_file(content):
    with open('(电影天堂)requests+xpath.txt','a',encoding='utf-8')as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')

def main(page_number):
    url = "https://www.dytt8.net/html/gndy/dyzz/list_23_" + str(page_number) + ".html"
    html = get_page(url)
    parse_page(html)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i for i in range(0,50)])