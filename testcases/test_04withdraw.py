"""
测试提现接口的测试用例类
"""
import os
import unittest
import requests
from jsonpath import jsonpath
from common.handle_excel import Excel
from common import myddt
from common.handle_path import DATA_DIR
from common.handle_config import conf
from common.handle_log import log
from common.handle_db import db
from common.handle_data import replace_data
from tools import fixture


@myddt.ddt
class TestWithdraw(unittest.TestCase):
    """测试提现接口的测试用例类"""
    excel = Excel(file_name=os.path.join(DATA_DIR, 'cases.xlsx'), sheet_name='withdraw')
    case = excel.read_excel()
    print()

    @classmethod
    def setUpClass(cls):
        """测试用例类执行"""
        fixture.setup_login(TestWithdraw)

    @myddt.data(*case)
    def test_withdraw(self, item):
        """测试提现接口的方法"""
        # 请求接口
        url = conf.get('env', 'base_url') + item['url']
        # 请求参数
        # if '#member_id#' in item['data']:
        #     item['data'] = item['data'].replace('#member_id#', str(self.member_id))
        # params = eval(item['data'])
        params = eval(replace_data(item['data'], TestWithdraw))
        # 请求头
        headers = eval(conf.get('env', 'headers'))
        headers['Authorization'] = self.token
        method = item['method']

        # 获取数据库中的提现之前的余额
        sql = item['check_sql']
        if sql:
            s_amount = db.find_data(sql.format(self.member_id))[0]['leave_amount']

        # 预期结果
        expected = eval(item['expected'])

        # 请求参数获得实际结果
        response = requests.request(method=method, url=url, headers=headers, json=params)
        res = response.json()
        print('预期结果：', expected)
        print('实际结果：', res)

        # 断言结果
        try:
            if sql:
                e_amount = db.find_data(sql.format(self.member_id))[0]['leave_amount']
                self.assertTrue(float(s_amount - e_amount), jsonpath(res, '$..leave_amount')[0])
            self.assertEqual(jsonpath(res, '$.code')[0], expected['code'])
            self.assertEqual(jsonpath(res, '$.msg')[0], expected['msg'])
        except AssertionError as e:
            log.error('用例{}：执行失败'.format(item['title']))
            log.exception(e)
            self.excel.write_excel(row=item['case_id'] + 1, column=8, value='未通过')
            raise e
        else:
            log.info('用例{}：执行通过'.format(item['title']))
            self.excel.write_excel(row=item['case_id'] + 1, column=8, value='通过')
