#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import requests
import time
from lxml import etree
import os
from concurrent import futures

global next_link
url = 'https://tieba.baidu.com/p/4183563666?pn=1'
headers = {
    'Referer': url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 Edg/80.0.361.66',
}


def download_img(src, dirname):
    filename = src.split('/')[-1]
    dirnames = 'imgs/{}'.format(dirname)
    if not os.path.exists(dirnames):
        os.makedirs(dirnames)
    img = requests.get(src, headers=headers)
    with open('{}/{}'.format(dirnames, filename), 'wb') as file :
        file.write(img.content)


def get_page(urls):
    resp = requests.get(urls, headers=headers)
    dirname = urls.split('pn=')[-1]
    print(resp, urls,"正在下载！")
    html = etree.HTML(resp.text)
    srcs = html.xpath('.//img[@class="BDE_Image"]/@src')

    # 多线程 使用
    ex = futures.ThreadPoolExecutor(max_workers=60)
    for src in srcs:
        ex.submit(download_img, src, dirname)

    # for src in srcs:
    #     download_img(src,dirname)
    # 下一页链接
    next_page = html.xpath('.//li[@class="l_pager pager_theme_5 pb_list_pager"]/a/@href')[-2]
    # 当前所属页数
    span = html.xpath('.//span[@class="tP"]/text()')[0]
    # 最大页数
    ng = html.xpath('.//li[@class="l_pager pager_theme_5 pb_list_pager"]/a/@href')[-1]
    ng = ng.split('pn=')[-1]
    # print(next_page,span,ng)
    return next_page,span,ng


def page(next_link):
    if next_link:
        next_page = "https://tieba.baidu.com" + next_link
        return next_page

def main():
    next_link,_,_ = get_page(url)
    # print(next_link)
    while True:
        next_page = page(next_link)
        next_link,span,ng = get_page(next_page)
        # print(next_link,span)
        if span==ng:
            break


if __name__ == "__main__":
    main()
