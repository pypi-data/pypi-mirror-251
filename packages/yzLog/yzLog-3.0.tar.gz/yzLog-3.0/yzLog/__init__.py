# encoding=utf-8
import logging, time, os
from logging.handlers import RotatingFileHandler

"""
亮黑色：\u001b[30;1m
亮红色：\u001b[31;1m
亮绿色：\u001b[32;1m
亮黄色：\u001b[33;1m
亮蓝色：\u001b[34;1m
亮洋红色：\u001b[35;1m
亮青色：\u001b[36;1m
亮白色：\u001b[37;1m
"""


# 根据日志级别添加不同的颜色
def addColor(record):
    if record.levelname == 'DEBUG':
        record.msg = f"\u001b[34;1m{record.msg}\u001b[0m"
        record.levelname = f"\u001b[34;1m{record.levelname}\u001b[0m"
    elif record.levelname == 'INFO':
        record.msg = f"\u001b[32;1m{record.msg}\u001b[0m"
        record.levelname = f"\u001b[32;1m{record.levelname}\u001b[0m"
    elif record.levelname == 'WARNING':
        record.msg = f"\u001b[33;1m{record.msg}\u001b[0m"
        record.levelname = f"\u001b[33;1m{record.levelname}\u001b[0m"
    elif record.levelname == 'ERROR':
        record.msg = f"\u001b[31;1m{record.msg}\u001b[0m"
        record.levelname = f"\u001b[31;1m{record.levelname}\u001b[0m"
    else:
        record.msg = f"\u001b[36;1m{record.msg}\u001b[0m"
        record.levelname = f"\u001b[36;1m{record.levelname}\u001b[0m"
    return record


# 日志部分
def getLog(file_name=None, root=None, date_suffix=False, max_bytes=None, back_count=5, output_window=True,
           output_file=True):
    """
    :param file_name: 日志名称(相对路径或绝对路径) 不含后缀
    :param root: 使用者
    :param date_suffix: 是否加日期
    :param max_bytes: 使用滚动日志
    :param back_count: 滚动日志的最大数量
    :param output_window: 是否输出到控制台
    :param output_file: 是否输出到文件
    :return:
    """
    file_name = file_name or "default"
    path, name = os.path.split(file_name)
    if path and not os.path.isdir(path):
        os.makedirs(path)
    if date_suffix:
        file_name += time.strftime("%Y%m%d")
    file_name += ".log"
    # 自定义的日志格式 "|" => \u001b[35;1m|\u001b[0m
    formatter = logging.Formatter(
        fmt='\u001b[36;1m%(asctime)s \u001b[35;1m| %(levelname)s  \t\u001b[35;1m| \u001b[36;1m%(module)s\u001b[37;1m[%(lineno)d] \u001b[35;1m--> %(message)s \u001b[0m',
        datefmt='%Y-%m-%d %H:%M:%S')
    formatter2 = logging.Formatter(
        fmt='%(asctime)s | %(levelname)s  \t| %(module)s[%(lineno)d] --> %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    # 控制台处理器
    logger = logging.getLogger(root)
    logger.setLevel(logging.DEBUG)
    # 文件处理器
    if output_file:
        if max_bytes:  # 滚动日志
            file_handler = RotatingFileHandler(filename=file_name, encoding="utf-8",
                                               maxBytes=max_bytes * 1024, backupCount=back_count)
        else:
            file_handler = logging.FileHandler(filename=file_name, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter2)
        logger.addHandler(file_handler)
    # 控制台处理器
    if output_window:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        stream_handler.addFilter(addColor)
        logger.addHandler(stream_handler)

    logger.warn = logger.warning
    return logger


if __name__ == '__main__':
    log = getLog(output_window=True,output_file=False)
    log.debug(f"测试输出...")
    log.info(f"测试输出...")
    log.warning(f"测试输出...")
    log.warn(f"测试输出...")
    log.error(f"测试输出...")
