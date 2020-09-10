"""
新增项目测试用例类


"""
import os
import unittest
import requests
from jsonpath import jsonpath

from common.handle_db import db
from common.handle_excel import Excel
from common.handle_path import DATA_DIR
from common import myddt
from common.handle_config import conf
from common.handle_data import replace_data
from common.handle_log import log
from tools import fixture


@myddt.ddt
class TestAdd(unittest.TestCase):
    """新增项目的测试用例类"""

    @classmethod
    def setUpClass(cls):
        """请求登录接口获取token和member_id"""
        fixture.setup_login(TestAdd)

    excel = Excel(file_name=os.path.join(DATA_DIR, 'cases.xlsx'), sheet_name='add')
    case = excel.read_excel()

    @myddt.data(*case)
    def test_add(self, item):
        # 请求接口的url
        url = conf.get('env', 'base_url') + item['url']
        # 请求参数
        params = eval(replace_data(item['data'], TestAdd))
        # 请求头
        headers = eval(conf.get('env', 'headers'))
        headers['Authorization'] = self.token
        # 请求方法
        method = item['method']
        # 预期结果
        expected = eval(item['expected'])
        # 请求接口获得请求结果
        response = requests.request(method=method, url=url, json=params, headers=headers)
        res = response.json()
        print('预期结果：', expected)
        print('实际结果：', res)
        # 断言
        try:
            self.assertEqual(res['code'], expected['code'])
            self.assertEqual(res['code'], expected['code'])
            if item['check_sql']:
                result = db.find_data((item['check_sql']).format(jsonpath(res, '$..id')[0]))
                self.assertTrue(result)
        except AssertionError as e:
            log.error('用例{}，执行失败'.format(item['title']))
            log.exception(e)
            self.excel.write_excel(row=item['case_id'] + 1, column=8, value='未通过')
            raise e
        else:
            log.info('用例{}，执行成功'.format(item['title']))
            self.excel.write_excel(row=item['case_id'] + 1, column=8, value='通过')
