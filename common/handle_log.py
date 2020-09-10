"""
日志操作类
"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler
from common.handle_config import conf
from common.handle_path import LOG_DIR


class HandleLog:

    @staticmethod
    def create_log():
        # 1、创建日志收集器
        log = logging.getLogger('mylog')
        # 设置日志收集等级
        log.setLevel(conf.get('logging', 'level'))

        # 2、创建日志输出渠道
        # 创建控制台输出渠道
        sh = logging.StreamHandler()
        # 设置控制台的输出日志等级
        sh.setLevel(conf.get('logging', 'sh_level'))
        # 将控制台日志输出渠道与日志收集器进行绑定
        log.addHandler(sh)
        # 创建文件输出渠道
        fh = TimedRotatingFileHandler(filename=os.path.join(LOG_DIR, conf.get('logging', 'log_name')),
                                      when='d',
                                      interval=1,
                                      backupCount=7,
                                      encoding='utf-8')
        # 设置文件输出渠道的日志等级
        fh.setLevel(conf.get('logging', 'fh_level'))
        # 将文件日志输出渠道与日志收集器进行绑定
        log.addHandler(fh)

        # 3、设置日志输出格式
        formatter = '%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
        mat = logging.Formatter(formatter)
        # 设置日志输出渠道的日志显示格式
        fh.setFormatter(mat)
        sh.setFormatter(mat)

        # 4、返回日志收集器
        return log


# 实例化log对象，其他模块在引用时，导入log对象，保存在运行的程序中，只存在一个log对象，避免出现日志重复记录的问题
log = HandleLog.create_log()
