# coding=utf-8
# @Time    : 2018/7/25 10:58
# @Author  : blank404
# @FileName: 20180716.py
# @Software: PyCharm
# @Blog    : https://blog.csdn.net/sinat_24648637

import requests
from bs4 import BeautifulSoup
import multiprocessing
import time
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

span = 0

def get_proxy_ip():
    """
    获取代理IP
    :return:
        proxy: 代理IP
    """
    proxy = []
    for n in range(1, 40):
        header = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'}
        r = requests.get('http://www.xicidaili.com/nt/1', headers=header)

        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        # print soup
        table = soup.find('table', attrs={'id': 'ip_list'})
        # print table
        tr = table.find_all('tr')[1:]
        # 遍历得到代理IP
        for item in tr:
            temp_dict = {}
            td = item.find_all('td')
            ip = td[1].get_text()
            port = td[2].get_text()
            tp = td[5].get_text().lower()
            if tp == 'http':
                temp_dict['http'] = "http://%s:%s" % (ip, port)
            if tp == 'https':
                temp_dict['https'] = "https://%s:%s" % (ip, port)
            # print temp_dict
            proxy.append(temp_dict)
    return proxy


def brash(proxy_dict,blog):
    """
    访问 CSDN 网站
    :param proxy_dict: 代理IP dictionary
    :return: span: 阅读量
    """
    span = '0：0'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/64.0.3282.140 '
                      'Safari/537.36 '
                      'Edge/17.17134',
        'Referer': 'https://pos.baidu.com/wh/o.htm?ltr='
    }
    try:
        """
        使用代理
        同添加headers方法，代理参数也要是一个dict
        这里使用requests库爬取了IP代理网站的IP与端口和类型
        因为是免费的，使用的代理地址很快就失效了。
        """
        r = requests.get(blog,
                         headers=header,
                         proxies=proxy_dict,
                         timeout=10)
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        # print soup
        span = soup.find('span', attrs={'class': 'read-count'}).get_text()
    except Exception as e:
        print 'Failed'
    else:
        print 'Successful'
    time.sleep(random.random())
    return span


if __name__ == '__main__':
    final = 5
    i = 0
    proxies = get_proxy_ip()  # 代理IP池
    # print proxies
    blogs = [
        "https://blog.csdn.net/sinat_24648637/article/details/80626311",
        "https://blog.csdn.net/sinat_24648637/article/details/80296378",
        "https://blog.csdn.net/sinat_24648637/article/details/80295201",
        "https://blog.csdn.net/sinat_24648637/article/details/80178644",
        "https://blog.csdn.net/sinat_24648637/article/details/80175747",
        "https://blog.csdn.net/sinat_24648637/article/details/79551137",
        "https://blog.csdn.net/sinat_24648637/article/details/79599317",
        "https://blog.csdn.net/sinat_24648637/article/details/79738209"
    ]
    for blog in blogs:
        num = 0
        print blog + ': 开始 '
        while i <= final:
            # 多进程解决问题
            pool = multiprocessing.Pool(processes=32)
            results = []
            for j in range(len(proxies)):
                if num >= random.randint(1216, 1609):
                    i = final+1
                    break
                results.append(pool.apply_async(brash, (proxies[j],blog)))
                res = results[j].get()
                num = int(res.split("：")[1])
            pool.close()
            pool.join()
            time.sleep(random.randint(60, 120))
        print blog + ': 达标 '
