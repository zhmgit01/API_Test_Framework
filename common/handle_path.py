"""
项目路径处理
"""
import os

# 获取项目的根路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 测试用例的目录路径
CASE_DIR = os.path.join(BASE_DIR, 'testcases')

# 测试报告的目录路径
REPORT_DIR = os.path.join(BASE_DIR, 'reports')

# 日志目录的项目路径
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# 用例数据的项目路径
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 配置文件的项目路径
CONF_DIR = os.path.join(BASE_DIR, 'conf')

if __name__ == '__main__':
    print(BASE_DIR)
    print(CASE_DIR)
    print(REPORT_DIR)
    print(LOG_DIR)
    print(DATA_DIR)
    print(CONF_DIR)
