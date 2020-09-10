"""
封装通用的代码逻辑


"""
import random
import requests
from jsonpath import jsonpath

from common.handle_config import conf
from common.handle_db import db


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


def register(user_conf, pwd_conf, params_type=1):
    """注册用户，将用户信息保存至配置文件中的相应位置"""
    register_url = conf.get('env', 'base_url') + '/member/register'
    register_params = {
        "mobile_phone": random_phone(),
        "pwd": "12345678",
        "type": params_type
    }
    headers = eval(conf.get('env', 'headers'))
    # 请求注册接口，注册用户
    response = requests.request(method='post', url=register_url, json=register_params, headers=headers)
    if response.json()['code'] == 0:
        mobile = str(register_params['mobile_phone'])
        pwd = str(register_params['pwd'])

    # 保存到配置文件，调用配置文件类中的写入方法
    conf.write_data(section='test_data', option=user_conf, value=mobile)
    conf.write_data(section='test_data', option=pwd_conf, value=pwd)
    return mobile, pwd


def login(mobile, pwd):
    """登录"""
    login_url = conf.get("env", "base_url") + "/member/login"
    login_params = {"mobile_phone": mobile,
                    "pwd": pwd}
    headers = eval(conf.get("env", "headers"))
    response = requests.request(url=login_url, method="post", json=login_params, headers=headers)
    res = response.json()
    # 提取token
    token = "Bearer" + " " + jsonpath(res, "$..token")[0]
    # 提取用户id
    member_id = jsonpath(res, "$..id")[0]
    return token, member_id


def recharge(token, member_id, money=500000):
    """充值"""
    headers = eval(conf.get("env", "headers"))
    headers["Authorization"] = token
    recharge_url = conf.get("env", "base_url") + "/member/recharge"
    recharge_params = {"member_id": member_id,
                       "amount": money}
    requests.request(url=recharge_url, method="post", json=recharge_params, headers=headers)


def init_env_data():
    """初始化环境数据"""
    # 注册普通用户（借款人），保存到配置文件
    user_info = register(user_conf="mobile", pwd_conf="pwd")
    # 注册普通用户（投资人），保存到配置文件
    user2 = register(user_conf="invest_mobile", pwd_conf="invest_pwd")
    # 注册管理员，保存到配置文件
    register(user_conf="admin_mobile", pwd_conf="admin_pwd", params_type=0)

    # (借款人)登录获取用户id
    token, member_id = login(*user_info)
    # 给用户充值
    recharge(token, member_id)
    recharge(token, member_id)

    # (投资人)登录获取用户id
    token2, member_id2 = login(*user2)
    # 给用户充值
    recharge(token2, member_id2)
    recharge(token2, member_id2)
