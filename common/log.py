import logging  # 导入日志模块
import sys  # 导入系统模块

def _reset_logger(log):
    """
    重置日志记录器的函数。
    清除所有现有的日志处理器并添加新的控制台和文件处理器。
    """
    for handler in log.handlers:  # 遍历现有的日志处理器
        handler.close()  # 关闭处理器
        log.removeHandler(handler)  # 从记录器中移除处理器
        del handler  # 删除处理器对象
    log.handlers.clear()  # 清空处理器列表
    log.propagate = False  # 禁止日志传播到根记录器

    # 创建控制台处理器，输出日志到标准输出
    console_handle = logging.StreamHandler(sys.stdout)
    console_handle.setFormatter(
        logging.Formatter(
            "[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s",  # 设置日志格式
            datefmt="%Y-%m-%d %H:%M:%S",  # 设置时间格式
        )
    )

    # 创建文件处理器，输出日志到文件
    file_handle = logging.FileHandler("run.log", encoding="utf-8")
    file_handle.setFormatter(
        logging.Formatter(
            "[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s",  # 设置日志格式
            datefmt="%Y-%m-%d %H:%M:%S",  # 设置时间格式
        )
    )

    log.addHandler(file_handle)  # 将文件处理器添加到日志记录器
    log.addHandler(console_handle)  # 将控制台处理器添加到日志记录器

def _get_logger():
    """
    获取日志记录器的函数。
    创建并返回一个已配置的日志记录器。
    """
    log = logging.getLogger("log")  # 获取名为 "log" 的日志记录器
    _reset_logger(log)  # 重置日志记录器
    log.setLevel(logging.INFO)  # 设置日志记录器的级别为 INFO
    return log  

# 日志句柄
logger = _get_logger()  #
