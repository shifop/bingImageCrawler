# -*- coding: utf-8 -*-
from threading import Thread
import schedule
from downloader import crawler
import time
import datetime
from tools import get_root_path, get_logger

logger = get_logger('app')


def download_imge(save_path, url):
    print('开始下载图片')
    rt = crawler(save_path, url)
    length = len(rt)
    time_info = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info('下载结束，当前时间：%s，总计处理图片数量：%d' % (time_info, length))
    logger.info('信息情况如下：')
    for x in rt:
        logger.info('rt:%s' % (x))


def run_job(fn1, save_path, url):
    fn1(save_path, url)
    schedule.every(1).hour.do(fn1, save_path, url)
    while True:
        schedule.run_pending()
        logger.info('===============!!!!=================')
        time.sleep(60)


if __name__ == '__main__':
    save_path = get_root_path('save_img')
    url = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1501558320736&pid=hp'
    print('开启定时任务模块')
    Thread(target=run_job, args=(download_imge, save_path, url)).start()
    # while True:
    #     time.sleep(60)
