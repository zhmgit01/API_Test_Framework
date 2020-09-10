"""
替换参数化的数据
"""
import re
from common.handle_config import conf


def replace_data(data, cls):
    """替换用例参数"""
    # re.search("#(.+?)#", data) 无与此匹配的的内容，则返回 None
    while re.search("#(.+?)#", data):
        item = re.search("#(.+?)#", data)
        # 需要替换的数据
        # 返回一个包含所有小组字符串的元组，从 1 到 所含的小组号。
        rep_data = item.group()
        # 要替换的属性
        # 获得组内的匹配项
        key = item.group(1)
        try:
            value = conf.get('test_data', key)
        except:
            value = getattr(cls, key)
        data = data.replace(rep_data, str(value))
    return data


class EnvDate:
    member_id = 123
    user = "musen"
    loan = 31


if __name__ == '__main__':
    data = '{"member_id":"#member_id#","pwd":"#pwd#","user":"#user#","loan_id":"#loan#"}'
    res = replace_data(data, EnvDate)
    print(res)
