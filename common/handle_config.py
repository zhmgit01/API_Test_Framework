"""
配置文件类
"""

from configparser import ConfigParser
import os
from common.handle_path import CONF_DIR


class Config(ConfigParser):
    """封装操作配置文件的类"""

    def __init__(self, file_name, encoding='utf-8'):
        # 重写父类的 __init__ 方法
        super().__init__()
        self.filename = file_name
        self.encoding = encoding
        # 读取配置文件的内容
        self.read(filenames=file_name, encoding=encoding)

    def write_data(self, section, option, value):
        """将数据写入配置文件中"""
        self.set(section, option, value)
        self.write(fp=open(self.filename, 'w', encoding=self.encoding))


# 实例化配置类对象
conf = Config(os.path.join(CONF_DIR, 'config.ini'))

if __name__ == '__main__':
    cfg = Config(os.path.join(CONF_DIR, 'config.ini'))
    res = cfg.get('logging', 'level')
    print(res)
