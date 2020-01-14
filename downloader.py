import requests
import os
import json
from tools import get_logger

logger = get_logger('downloader')


def get_img_info(url):
    """
    下载指定地址的图片
    :param url:
    :return:
    """
    all = []
    try:
        rt = requests.get(url)
        if rt.status_code == 200:
            data = json.loads(rt.text)['images']
            for text in data:
                if len(set(['url', 'startdate', 'enddate']) - set([_ for _ in text.keys()])) == 0:
                    # 获取相关信息
                    img_info = {
                        'startdate': text['startdate'],
                        'enddate': text['enddate'],
                        'url': text['url'],
                    }
                    if 'copyright' in text.keys():
                        img_info['copyright'] = text['copyright']

                    all.append({'code': 0, 'data': img_info})
                else:
                    all.append({'code': 1, 'msg': '参数缺失:%s' % (str(text))})
        else:
            all.append({'code': 2, 'msg': '连接失败'})
    except BaseException as e:
        logger.error(str(e))
        all.append({'code': 1, 'msg': str(e)})
    return all


def download_img(save_path, url):
    """
    下载图片
    :param save_path:
    :param url:
    :return:
    """
    rt = requests.get(url)
    try:
        if rt.status_code == 200:
            img = rt.content
            with open(save_path, 'wb') as f:
                f.write(img)
            return True
        else:
            return False
    except BaseException as e:
        logger.error(str(e))
        return False


def crawler(save_path, url):
    """
    抓取图片保持在指定位置
    :param save_path: 保持地址
    :param url: 相关参数：访问地址
    :return:
    """
    # 获取相关信息
    all = []
    img_infos = get_img_info(url)
    for img_info in img_infos:
        if img_info['code'] == 0:
            url = img_info['data']['url']
            copyright = img_info['data']['copyright'] if 'copyright' in img_info['data'].keys() else "无名"
            if ' ' in copyright:
                copyright = copyright[:copyright.index(' ')]
            suffix = url[url.rindex("."):len(url)][1:]
            if '&' in suffix:
                suffix = suffix[:suffix.index('&')]
            filename = '%s_%s_%s.%s' % (
            str(img_info['data']['startdate']), str(img_info['data']['enddate']), copyright, suffix)
            filePath = os.path.join(save_path, filename)
            if os.path.exists(filePath):
                all.append({'code': 2, 'img_info': img_info})
                continue
            url = 'https://www.bing.com' + url
            rt = download_img(filePath, url)
            if rt:
                all.append({'code': 0, 'path': os.path.join(save_path, filename)})
            else:
                all.append({'code': 1, 'img_info': img_info})
        else:
            all.append({'code': 1, 'img_info': img_info})
    return all


if __name__ == '__main__':
    text = {'images': [{'startdate': '20200113', 'fullstartdate': '202001131600', 'enddate': '20200114',
                        'url': '/th?id=OHR.MuskOxWinter_ZH-CN2030874541_1920x1080.jpg&rf=LaDigue_1920x1080.jpg&pid=hp',
                        'urlbase': '/th?id=OHR.MuskOxWinter_ZH-CN2030874541',
                        'copyright': '阿拉斯加普拉德霍湾附近的雄性麝牛 (© Oliver Smart/Alamy)',
                        'copyrightlink': '/search?q=%e9%ba%9d%e7%89%9b&form=hpcapt&mkt=zh-cn', 'title': '',
                        'quiz': '/search?q=Bing+homepage+quiz&filters=WQOskey:%22HPQuiz_20200113_MuskOxWinter%22&FORM=HPQUIZ',
                        'wp': True, 'hsh': '04bcc90ad1e543b7a7cf9947da1e06eb', 'drk': 1, 'top': 1, 'bot': 1, 'hs': []}],
            'tooltips': {'loading': '正在加载...', 'previous': '上一个图像', 'next': '下一个图像', 'walle': '此图片不能下载用作壁纸。',
                         'walls': '下载今日美图。仅限用作桌面壁纸。'}}
    need = set(['url', 'startdate', 'enddate'])
    has = set([_ for _ in text.keys()])
    print(len(need - has))
