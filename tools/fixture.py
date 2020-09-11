"""
测试夹具封装逻辑
"""
import requests
from jsonpath import jsonpath
from common.handle_config import conf


def setup_login(cls):
    """
    普通用户登录（投资接口中的借款人）
    :param cls: 测试用例类
    :return:
    """
    """写该用例类执行之前的前置
    登录，获取token，和用户id
    """
    login_url = conf.get("env", "base_url") + "/member/login"
    params = {
        "mobile_phone": conf.get("test_data", "mobile"),
        "pwd": conf.get("test_data", "pwd")
    }
    header = eval(conf.get("env", "headers"))
    response = requests.request(url=login_url, method="post", json=params, headers=header)
    res = response.json()
    # 提取token
    token = jsonpath(res, "$..token")[0]
    cls.token_value = token
    cls.token = "Bearer" + " " + token
    # 提取用户id
    cls.member_id = jsonpath(res, "$..id")[0]


def setup_login_invest(cls):
    """
    普通用户登录（投资接口中的投资人）
    :param cls: 测试用例类
    :return:
    """
    """写该用例类执行之前的前置
    登录，获取token，和用户id
    """
    login_url = conf.get("env", "base_url") + "/member/login"
    params = {
        "mobile_phone": conf.get("test_data", "invest_mobile"),
        "pwd": conf.get("test_data", "invest_pwd")
    }
    header = eval(conf.get("env", "headers"))
    response = requests.request(url=login_url, method="post", json=params, headers=header)
    res = response.json()
    # 提取token
    token = jsonpath(res, "$..token")[0]
    cls.invest_token_value = token
    cls.invest_token = "Bearer" + " " + token
    # 提取用户id
    cls.invest_member_id = jsonpath(res, "$..id")[0]


def setup_login_admin(cls):
    """管理员登录"""
    login_url = conf.get("env", "base_url") + "/member/login"
    params = {
        "mobile_phone": conf.get("test_data", "admin_mobile"),
        "pwd": conf.get("test_data", "admin_pwd")
    }
    header = eval(conf.get("env", "headers"))
    response = requests.request(url=login_url, method="post", json=params, headers=header)
    res = response.json()
    # 提取token
    cls.admin_token = "Bearer" + " " + jsonpath(res, "$..token")[0]
    cls.admin_token_value = jsonpath(res, '$..token')[0]


def setup_add(cls):
    """添加项目的前置"""
    url = conf.get("env", "base_url") + "/loan/add"
    params = {"member_id": cls.member_id,
              "title": "借钱",
              "amount": 2000,
              "loan_rate": 12.0,
              "loan_term": 3,
              "loan_date_type": 1,
              "bidding_days": 5}
    headers = eval(conf.get("env", "headers"))
    headers["Authorization"] = cls.token
    response = requests.request(url=url, method="post", json=params, headers=headers)
    res = response.json()
    # 将项目id保存为类属性
    cls.loan_id = jsonpath(res, "$..id")[0]


def set_up_audit(cls):
    """审核项目"""
    audit_url = conf.get('env', 'base_url') + '/loan/audit'
    audit_params = {
        "loan_id": cls.loan_id,
        "approved_or_not": True
    }
    audit_headers = eval(conf.get('env', 'headers'))
    audit_headers['Authorization'] = cls.admin_token
    requests.request(method='patch', url=audit_url, json=audit_params, headers=audit_headers)
