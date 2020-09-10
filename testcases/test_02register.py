"""
测试注册的测试用例类
"""
import unittest
import os
import requests
import random
from common import myddt
from common.handle_excel import Excel
from common.handle_path import DATA_DIR
from common.handle_config import conf
from common.handle_log import log
from common.handle_db import db


@myddt.ddt
class TestRegister(unittest.TestCase):
    excel = Excel(file_name=os.path.join(DATA_DIR, 'cases.xlsx'), sheet_name='register')
    case_data = excel.read_excel()

    @myddt.data(*case_data)
    def test_register(self, item):
        """测试注册的测试用例方法"""
        # 请求数据

        """参数化开始"""
        # 判断请求参数中是否有手机号，需要替换
        if "*phone*" in item['data']:
            phone = self.random_phone()
            # 将参数中的*phone*替换为随机生成的手机号
            item['data'] = item['data'].replace('*phone*', phone)
        """参数化结束"""

        params = eval(item['data'])
        # 请求头
        headers = eval(conf.get('env', 'headers'))
        # 请求接口
        register_url = conf.get('env', 'base_url') + item['url']
        # 预期结果
        expected = eval(item['expected'])
        # 请求方式
        method = item['method']
        # 实际结果
        response = requests.request(method=method, json=params, url=register_url, headers=headers)
        res = response.json()

        print('预期结果：', expected)
        print('请求参数：', params)
        print('实际结果：', res)
        # 断言判断
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])

            # 获取测试数据中的 check_sql 判断注册的信息在数据库中是否存在
            check_sql = item['check_sql']
            if check_sql:
                # params['mobile_phone'] 请求参数中的 mobile_phone 的值
                res = db.find_data(check_sql.format(params['mobile_phone']))
                # 判断res结果是否为空，为空则断言失败，用例执行不通过
                self.assertTrue(res)

        except AssertionError as e:
            log.exception(e)
            log.error('用例{},测试未通过'.format(item['title']))
            self.excel.write_excel(row=(item['case_id'] + 1), column=8, value='未通过')
            raise e
        else:
            log.info('用例{},测试通过'.format(item['title']))
            self.excel.write_excel(row=(item['case_id'] + 1), column=8, value='通过')

    @staticmethod
    def random_phone():
        """随机生成一个为被注册的手机号码"""
        while True:
            phone = '131'
            for i in range(8):
                a = random.randint(0, 9)
                phone += str(a)
            # 查询数据库中 该手机号是否被注册
            res = db.find_data('select * from futureloan.member t where t.mobile_phone = {}'.format(phone))
            if not res:
                return phone
