"""
测试充值接口的测试用例类
"""

import unittest
import os
import requests
from common import myddt
from jsonpath import jsonpath
from common.handle_excel import Excel
from common.handle_path import DATA_DIR
from common.handle_config import conf
from common.handle_log import log
from common.handle_db import db
from common.handle_data import replace_data
from tools import fixture


@myddt.ddt
class TestRecharge(unittest.TestCase):
    excel = Excel(file_name=os.path.join(DATA_DIR, 'cases.xlsx'), sheet_name='recharge')
    case_data = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        """用例类执行前需要执行内容"""
        fixture.setup_login(TestRecharge)

    @myddt.data(*case_data)
    def test_recharge(self, item):
        """充值接口测试用例方法"""

        # 请求参数
        """参数化 member_id 开始"""
        # if '#member_id#' in item['data']:
        #     # 将替换 #member_id# self.member_id
        #     item['data'] = item['data'].replace('#member_id#', str(self.member_id))
        # params = eval(item['data'])
        params = eval(replace_data(item['data'], TestRecharge))
        """参数化 member_id 结束"""

        # 请求头(配置文件中获取的为str类型)
        headers = eval(conf.get('env', 'headers'))
        # 将 token 字段添加到请求头中
        headers["Authorization"] = self.token

        # 请求方法
        method = item['method']
        # 请求接口
        recharge_url = conf.get('env', 'base_url') + item['url']
        # 预期结果
        expected = eval(item['expected'])

        # 获取充值前数据库中的金额
        sql = item['check_sql']
        if sql:
            start_amount = db.find_data(sql.format(self.member_id))[0]['leave_amount']

        # 实际结果
        response = requests.request(method=method, url=recharge_url, json=params, headers=headers)
        res = response.json()

        print('预期结果：', expected)
        print('实际结果：', res)

        try:
            # 将充值前后的金额之差，与充值的金额比较，相等则通过，不等则失败
            if sql:
                # 获取充值后数据库中的金额
                end_amount = db.find_data(sql.format(self.member_id))[0]['leave_amount']
                # 断言前后数据库中数值的变化和实际传入参数的大小是否一致
                self.assertEqual(float(end_amount - start_amount), eval(item['data'])['amount'])

            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])

        except AssertionError as e:
            log.error("用例{}，执行未通过".format(item["title"]))
            self.excel.write_excel(row=(item['case_id'] + 1), column=8, value='未通过')
            log.exception(e)
            raise e
        else:
            log.info("用例{}，执行通过".format(item["title"]))
            self.excel.write_excel(row=(item['case_id'] + 1), column=8, value='通过')
