import json
import re,requests
from multiprocessing.pool import Pool

headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
}


def get_page(url):
    html = requests.get(url,headers=headers)  # 获取主排行的html文件
    html.encoding = 'gbk'   #　解码方式
    return html

def parse_page(html):
    try:
        detail_page = re.findall('<a href="(.*?)"\sclass="ulink".*?</a>',html.text)  # 提取每一个电影页面的html
        for i in detail_page:
            detail_url = 'https://www.dytt8.net'+ i     #　补全电影详细页面的ｈｔｍｌ
            html2 = requests.get(detail_url,headers=headers)   #　获取电影详细页面的ｈｔｍｌ数据
            html2.encoding = 'gbk'
            ftp = re.compile('<tbody.*?<a href.*?>(.*?)</a>',re.S)  # 提取电影页面的下载链接（使用compile）
            download_ftp = re.findall(ftp,html2.text)
            for j in download_ftp:    #　遍历下载链接
                download_url = {
                    "下载链接":download_ftp[0]
                }
                print(download_url)
                save_to_file(download_url)
    except UnicodeEncodeError:
        pass
    except TimeoutError and requests.exceptions.ConnectionError:
        return parse_page(html)

def save_to_file(content):
    with open('(电影天堂)requests+re.txt','a',encoding='utf-8')as f:
        f.write(json.dumps(content,ensure_ascii=False)+ '\n')
        f.close()

def main(page_number):
    url ="https://www.dytt8.net/html/gndy/dyzz/list_23_" + str(page_number) + ".html"
    html = get_page(url)
    parse_page(html)
    print("正在爬取第{}页".format(page_number))  #  .format(var)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main ,[i for i in range(0,50)])