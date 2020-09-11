"""
测试更新用户昵称的接口
"""
import unittest
import os
import requests
from common import myddt
from common.handle_path import DATA_DIR
from common.handle_excel import Excel
from common.handle_config import conf
from common.handle_log import log
from tools import fixture
from tools.handle_sign import HandleSign


@myddt.ddt
class TestUpdateV3(unittest.TestCase):
    excel = Excel(file_name=os.path.join(DATA_DIR, 'cases.xlsx'), sheet_name='update')
    cases = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        fixture.setup_login(TestUpdateV3)

    @myddt.data(*cases)
    def test_update(self, item):
        # 获取请求接口
        url = conf.get('env', 'base_url') + item['url']
        # 获取请求数据
        params = eval(item['data'])

        # 请求参数添加timestamp和sign
        crypt_info = HandleSign.generate_sign(self.token_value)
        params['timestamp'] = crypt_info['timestamp']
        params['sign'] = crypt_info['sign']

        # 获取请求方法
        method = item['method']
        # 获取请求头v2
        # headers = eval(conf.get('env', 'headers'))

        # 请求头 v3
        headers = eval(conf.get('env', 'headers'))
        headers['Authorization'] = self.token

        # 预计结果
        expected = eval(item['expected'])
        # 请求接口获得实际结果
        response = requests.request(method=method, url=url, json=params, headers=headers)
        res = response.json()

        print('预计结果：', expected)
        print('实际结果：', res)

        # 断言判断
        try:
            self.assertEqual(res['code'], expected['code'])
            self.assertEqual(res['msg'], expected['msg'])
        except AssertionError as e:
            log.error("用例{},执行失败".format(item['title']))
            log.exception(e)
            self.excel.write_excel(row=item['case_id']+1,column=8, value='未通过')
            raise e
        else:
            log.info("用例{},执行成功".format(item['title']))
            self.excel.write_excel(row=item['case_id'] + 1, column=8, value='通过')
