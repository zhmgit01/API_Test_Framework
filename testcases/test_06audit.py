"""
审核项目接口测试用例类
"""
import os
import unittest

import requests
from jsonpath import jsonpath

from common.handle_config import conf
from common.handle_data import replace_data
from common.handle_excel import Excel
from common.handle_log import log
from common.handle_path import DATA_DIR
from common import myddt
from tools import fixture


@myddt.ddt
class TestAudit(unittest.TestCase):
    excel = Excel(os.path.join(DATA_DIR, "cases.xlsx"), "audit")
    cases = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        """获取token，和member_id"""
        # ----------------普通用户登录----------------
        fixture.setup_login(TestAudit)
        # ----------------管理员用户登录-------------------------
        fixture.setup_login_admin(TestAudit)

    def setUp(self):
        """新增一个待审核的项目，以便审核"""
        fixture.setup_add(TestAudit)

    @myddt.data(*cases)
    def test_audit(self, item):
        # 第一步：准备用例数据
        url = conf.get("env", "base_url") + item["url"]
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = self.admin_token
        # 替换用例参数
        item["data"] = replace_data(item["data"], TestAudit)
        params = eval(item["data"])
        # 请求方法
        method = item["method"]
        # 预期结果
        expected = eval(item["expected"])
        # 第二步：请求接口，获取实际返回的结果
        response = requests.request(url=url, method=method, json=params, headers=headers)
        res = response.json()
        # 第三步：断言
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            if item["title"] == "审核通过":
                TestAudit.pass_loan_id = params["loan_id"]
        except AssertionError as e:
            log.error("用例{}，执行未通过".format(item["title"]))
            log.exception(e)
            self.excel.write_excel(row=item['case_id'] + 1, column=8, value='未通过')
            raise e
        else:
            log.info("用例{}，执行通过".format(item["title"]))
            self.excel.write_excel(row=item['case_id'] + 1, column=8, value='通过')
