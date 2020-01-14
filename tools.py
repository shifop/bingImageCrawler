import logging
import os

def get_logger(name, log_level=logging.DEBUG, file_name="log.txt"):
    # 日志配置
    logger = logging.getLogger(name)
    logger.setLevel(level=log_level)
    handler = logging.FileHandler(file_name)
    handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(log_level)

    logger.addHandler(handler)
    logger.addHandler(console)

    # 打印测试
    logger.info("==========INFO===========")
    logger.debug("==========DEBUG===========")
    logger.warning("==========WARNING===========")
    return logger


def get_root_path(folderName):
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("bingImageCrawler") + len("bingImageCrawler")]  # 获取myProject，也就是项目的根路径
    folderPath = os.path.join(rootPath,folderName)
    return folderPath

if __name__=='__main__':
    path = get_root_path('save_img')
    print(path)