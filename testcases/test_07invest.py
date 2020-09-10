"""
测试投资接口的测试用例类

投资：
    前置：需要有一个状态处于竞标中的项目（登录-->添加项目--->审核通过）
        登录--->投资

    借款人：添加项目
    管理员：审核项目
    投资人：投资
    普通用户：既可以借款，又可以投资


用户登录：setupclass:
添加项目：setupclass:
审核项目：setupclass:

用例逻辑中：投资


用例执行完之后，如果数据库中涉及到多张表的数据变动，如何去进行校验
那些表，那字段发送了变化
1、投资表中新增一条数据？--->用例执行前后 根据用户和标id查询投资记录的条数
2、用户表中可用余额减少？--->用例执行前后查数据库中的余额进行比对？
3、流水记录表中新增一条数据？  --->用例执行前后 根据用户id查询流水记录的条数

"""
import os
import unittest
import requests
from common import myddt
from common.handle_excel import Excel
from common.handle_path import DATA_DIR
from common.handle_config import conf
from common.handle_data import replace_data
from common.handle_log import log
from tools import fixture
from common.handle_db import db


@myddt.ddt
class TestInvest(unittest.TestCase):
    excel = Excel(file_name=os.path.join(DATA_DIR, 'cases.xlsx'), sheet_name='invest')
    cases = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        # 借款人登录
        fixture.setup_login(TestInvest)
        # 投资人登录
        fixture.setup_login_invest(TestInvest)
        # 管理员登录
        fixture.setup_login_admin(TestInvest)
        # 添加项目
        fixture.setup_add(TestInvest)
        # 审核项目
        fixture.set_up_audit(TestInvest)

    @myddt.data(*cases)
    def test_invest(self, item):
        # 请求数据准备
        url = conf.get('env', 'base_url') + item['url']
        headers = eval(conf.get('env', 'headers'))
        headers['Authorization'] = self.invest_token
        params = eval(replace_data(item['data'], TestInvest))
        method = item['method']
        # 预计结果
        expected = eval(item['expected'])

        # 数据库判断逻辑（请求接口之前）
        if item['check_sql']:
            # 查询投资表记录
            sql1 = "SELECT * FROM futureloan.invest WHERE member_id={} and loan_id={}".format(self.invest_member_id,
                                                                                              self.loan_id)
            # 查询用户余额
            sql2 = "SELECT leave_amount FROM futureloan.member where id={}".format(self.invest_member_id)
            # 查询流水记录
            sql3 = "SELECT * FROM futureloan.financelog WHERE pay_member_id={}".format(self.invest_member_id)
            # 用例执行之前投资记录的条数
            s_invest = len(db.find_data(sql1))
            # 用例执行之前投资用户的余额
            s_amount = db.find_data(sql2)[0]['leave_amount']
            # 用例执行之前流水记录表用户的流水记录条数
            s_financelog = len(db.find_data(sql3))

        # 实际结果
        response = requests.request(method=method, url=url, json=params, headers=headers)
        res = response.json()
        print('请求参数', params)
        print('预期结果：', expected)
        print('实际结果：', res)

        # 断言
        try:
            self.assertEqual(res['code'], expected['code'])
            self.assertEqual(res['code'], expected['code'])

            # 数据库判断逻辑（请求接口之后）
            if item['check_sql']:
                # 查询投资表记录
                sql1 = "SELECT * FROM futureloan.invest WHERE member_id={} and loan_id={}".format(self.invest_member_id,
                                                                                                  self.loan_id)
                # 查询用户余额
                sql2 = "SELECT leave_amount FROM futureloan.member where id={}".format(self.invest_member_id)
                # 查询流水记录
                sql3 = "SELECT * FROM futureloan.financelog WHERE pay_member_id={}".format(self.invest_member_id)
                # 用例执行之后投资记录的条数
                e_invest = len(db.find_data(sql1))
                # 用例执行之后投资用户的余额
                e_amount = db.find_data(sql2)[0]["leave_amount"]
                # 用例执行之后流水记录表用户的的流水记录条数
                e_financelog = len(db.find_data(sql3))

                # 断言判断
                # 1、对比执行前后投资表记录数量是否+1
                self.assertEqual(1, e_invest-s_invest)
                # 2、对比用户余额
                self.assertEqual(params['amount'], s_amount-e_amount)
                # 3、对比执行前后流水记录表记录数量是否+1
                self.assertEqual(1, e_financelog-s_financelog)

        except AssertionError as e:
            log.error('用例{}，执行失败'.format(item['title']))
            log.exception(e)
            self.excel.write_excel(row=item['case_id'] + 1, column=8, value='未通过')
            raise e
        else:
            log.info('用例{}，执行成功'.format(item['title']))
            self.excel.write_excel(row=item['case_id'] + 1, column=8, value='通过')
