import os
import threading
import requests
from bs4 import BeautifulSoup

urls_list = ['upbeat', 'epic', 'horror', 'romantic',
             'comedy', 'world', 'scoring', 'electronic', 'misc']


def find(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield f


def main():
    x = []
    base = './'
    for i in find(base):
        x.append(i)
    return x


def get_list(url):
    music_url = []
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        res.encoding = 'utf-8'
        for i in soup.select('.downloadButton'):
            music_url.append('https://freepd.com' + i.get('href'))
    except requests.exceptions.ConnectionError:
        print(url + '页面下载列表获取失败')

    return music_url


def get_list2(url):
    music_url = []
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        res.encoding = 'utf-8'
        for i in soup.select('table a'):
            music_url.append('https://freepd.com/Page2/' + i.get('href'))
    except requests.exceptions.ConnectionError:
        print('page2页面下载列表获取失败')

    return music_url


def down_music(url, p):
    file_name = str(url.split('/')[-1])
    if file_name in f_list:
        pass
    else:
        headers = {'Referer': 'https://freepd.com/'}
        try:
            print(file_name+"开始下载")
            music = requests.get(url, headers=headers, stream=True)
            with open("./" + p + "/" + file_name, 'wb') as f:
                for chunk in music.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(file_name + '下载完成')
        except requests.exceptions.ConnectionError:
            print(file_name + '下载失败')


if __name__ == "__main__":
    f_list = main()
    for n in urls_list:
        isExists = os.path.exists("./" + n)
        if not isExists:
            os.mkdir(n)
    isExists = os.path.exists("./Page2")
    if not isExists:
        os.mkdir("Page2")
    pd = 'https://freepd.com/{}.php'
    for n in urls_list:
        down_url = get_list(pd.format(n))
        for x in down_url:
            ding = threading.Thread(target=down_music, args=(x, n))
            ding.start()

    down_url = get_list2("https://freepd.com/Page2/")
    for x in down_url:
        ding = threading.Thread(target=down_music, args=(x, 'Page2'))
        ding.start()
