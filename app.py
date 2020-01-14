# -*- coding: utf-8 -*-
from threading import Thread
import schedule
from downloader import crawler
import time
import os
from tools import get_root_path


def download_imge(save_path, url):
    print('开始下载图片')
    rt = crawler(save_path, url)
    print(rt)


def run_job(fn1, save_path, url):
    fn1(save_path, url)
    schedule.every(12).hours.do(fn1, (save_path, url))
    while True:
        schedule.run_pending()
        print('一次')
        time.sleep(60*60)


if __name__ == '__main__':
    save_path = get_root_path('save_img')
    url = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1501558320736&pid=hp'
    print('开启定时任务模块')
    Thread(target=run_job, args=(download_imge, save_path, url)).start()
