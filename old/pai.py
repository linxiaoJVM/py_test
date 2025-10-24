import requests
import os
import time
from lxml import html



i_headers = {
    "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 67.0.3396.99Safari / 537.36"
}
picroot = "d://pics"

def get_page(url):
    '''
    获取页面
    :return:
    '''
    page = requests.get(url, headers=i_headers)
    print(page.status_code)
    if page.status_code == 200:
        page.encoding = 'utf-8'
        print(page.text)
        return page.text
    else:
        return ''

def get_image(page):
    htm = html.fromstring(page)
    print(htm)
    result = htm.xpath('//*[@id="read_tpc"]/img/@src')
    print(result)
    print(len(result))
    urls = []    # img路径
    for img_page in result:
        if img_page[:4] == "http":
            urls.append(img_page)

    return urls

def download_img(urls):
    for url in urls:
        print(url)
        path = url.split("/")
        # print(path)

        filename = picroot + "/" + path[len(path)-2]
        if not os.path.exists(filename):
            os.makedirs(filename)

        filename = filename + "/" + path[len(path)-1]    # 图片名称作为保存文件名
        r = requests.get(url)
        # 检查请求是否成功
        print(r.raise_for_status())
        # wb表示写入二进制文件，使用r.content方式响应二进制内容
        with open(filename, "wb") as img:   # 二进制写文件
            img.write(r.content)
            time.sleep(0.5)
        filename = ''

if __name__ == '__main__':
    url = "http://q1.fnmdsbb.info/pw/html_data/14/1905/4094072.html"
    page = get_page(url)
    urls = get_image(page)
    download_img(urls)
