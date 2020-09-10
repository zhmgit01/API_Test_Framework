"""
测试用例
    组装测试套件，执行测试用例
"""
import unittest
from unittestreport import TestRunner
from common.handle_path import CASE_DIR, REPORT_DIR
from common.handle_config import conf
from tools.tools import init_env_data

# 加载测试套件
suite = unittest.defaultTestLoader.discover(CASE_DIR)

# 测试数据准备
init_env_data()

# 执行测试用例
runner = TestRunner(suite,
                    filename=conf.get('report', 'filename'),
                    title='测试报告',
                    report_dir=REPORT_DIR,
                    tester='zhm',
                    desc='执行测试用例生成的测试报告',
                    templates=1)
runner.run()

# 发送报告到邮箱
runner.send_email(host="smtp.163.com",
                  port=465,
                  user='XXXXXXX',
                  password='XXXXXXXXXX',
                  to_addrs=['XXXXXXXXXX'])
