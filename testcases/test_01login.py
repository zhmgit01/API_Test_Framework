"""
测试登录接口
"""
import unittest
import os
import requests
from common.handle_excel import Excel
from common.handle_path import DATA_DIR
from common import myddt
from common.handle_log import log
from common.handle_config import conf


@myddt.ddt
class TestLogin(unittest.TestCase):
    excel = Excel(os.path.join(DATA_DIR, 'cases.xlsx'), 'login')
    case_data = excel.read_excel()

    @myddt.data(*case_data)
    def test_login(self, item):
        """测试登录的测试用例方法"""
        # 测试数据
        params = eval(item['data'])
        method = item['method']
        # 预期结果
        expected = eval(item['expected'])
        # 请求头
        headers = eval(conf.get('env', 'headers'))
        # 接口地址
        login_url = conf.get('env', 'base_url') + item['url']
        # 实际结果
        response = requests.request(url=login_url, json=params, method=method, headers=headers)
        res = response.json()

        # 随机生成的手机号，代替用例数据中的 *phone*

        print('预期结果：', expected)
        print('实际结果：', res)

        # 断言判断
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
        except AssertionError as e:
            log.error('用例{},执行未通过'.format(item['title']))
            self.excel.write_excel(row=(item['case_id'] + 1), column=8, value='未通过')
            log.exception(e)
            raise e
        else:
            log.info('用例{},执行通过'.format(item['title']))
            self.excel.write_excel(row=(item['case_id'] + 1), column=8, value='通过')
