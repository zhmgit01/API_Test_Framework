"""
用户信息接口测试用例类
"""
import unittest
import os
import requests
from common import myddt
from common.handle_excel import Excel
from common.handle_path import DATA_DIR
from common.handle_config import conf
from common.handle_data import replace_data
from common.handle_log import log
from tools import fixture


@myddt.ddt
class TestInfoV3(unittest.TestCase):
    excel = Excel(file_name=os.path.join(DATA_DIR, 'cases.xlsx'), sheet_name='info')
    cases = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        fixture.setup_login(TestInfoV3)

    @myddt.data(*cases)
    def test_info(self, item):
        # 请求接口
        url = conf.get('env', 'base_url') + replace_data(item['url'], TestInfoV3)
        # 请求方法
        method = item['method']
        # 请求头v2
        # headers = eval(conf.get('env', 'headers'))

        # 请求头v3
        headers = eval(conf.get('env', 'headersV3'))
        headers['Authorization'] = self.token
        # 预期结果
        expected = eval(item['expected'])
        # 请求接口获得实际结果
        response = requests.request(method=method, url=url, headers=headers)
        res = response.json()

        print('预计结果：', expected)
        print('实际结果：', res)

        # 断言
        try:
            self.assertEqual(res['code'], expected['code'])
            self.assertEqual(res['code'], expected['code'])
        except AssertionError as e:
            log.exception(e)
            log.error('用例{}，执行未通过'.format(item['title']))
            self.excel.write_excel(row=item['case_id'] + 1, column=8, value='未通过')
            raise e
        else:
            log.info('用例{}，执行通过'.format(item['title']))
            self.excel.write_excel(row=item['case_id'] + 1, column=8, value='通过')
