# -*- Coding: utf-8 -*-
# Author: Yu
# todo: 日志配置，便于后面直接调用生成日志

import logging
from logging.handlers import RotatingFileHandler
import time
from Common import dir_path


# 设置全局获取日志函数，后面直接调用
def globale_logInfo(name='root'):

    # 定义日志输出格式
    cur_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())  # 设置时间格式
    fmt = "%(asctime)s-%(levelname)s-%(filename)s: %(funcName)s [ line:%(lineno)d ] %(message)s"  # 设置日志内容格式
    formatter = logging.Formatter(fmt)

    # 定义日志在控制台输出
    handler_console = logging.StreamHandler()  # 给logging增加处理器handler，stream输入输出

    # 定义日志在文件中输出
    handler_info = RotatingFileHandler(dir_path.logs_path + "/info_logs/UI_Auto{0}.log".format(cur_time),
                                       backupCount=30,
                                       encoding='utf-8')  # 日志轮转，一共只会存在20个日志文件，按照时间存放
    handler_error = RotatingFileHandler(dir_path.logs_path + "/warning_logs/UI_Auto{0}.log".format(cur_time),
                                        backupCount=30,
                                        encoding="utf-8")

    # 设置过滤条件
    info_filter = logging.Filter()
    info_filter.filter = lambda record: record.levelno < logging.WARNING  # 设置过滤等级
    err_filter = logging.Filter()
    err_filter.filter = lambda record: record.levelno >= logging.WARNING

    # 给handler处理器添加过滤器
    handler_info.addFilter(info_filter)
    handler_error.addFilter(err_filter)

    # 设置日志输出格式
    handler_console.setFormatter(formatter)
    handler_info.setFormatter(formatter)
    handler_error.setFormatter(formatter)

    # 给logger添加handler日志处理器
    log = logging.getLogger(name)  # logger获取名字
    log.setLevel(logging.INFO)  # 设置logger日志级别
    log.addHandler(handler_console)
    log.addHandler(handler_info)
    log.addHandler(handler_error)
    return log

# # 单元测试代码
# if __name__ == "__main__":
#     logger = globale_logInfo()
#     logger.info("this my bug__info")
#     logger.warning("this my bug__warning")
#     logger.error("this is my error")
