"""
封装操作数据库的类
"""
import pymysql
from common.handle_config import conf


class HandleDB:
    """封装数据库操作类"""

    def __init__(self, host, user, password, port, charset):
        """初始化数据库"""
        # 1、创建数据库连接
        self.con = pymysql.connect(host=host,
                                   user=user,
                                   password=password,
                                   port=port,
                                   # database='futureloan',
                                   charset=charset,
                                   cursorclass=pymysql.cursors.DictCursor
                                   )
        # 2、创建游标
        self.cur = self.con.cursor()

    def find_data(self, sql):
        """查询数据"""
        # 提交事务，同步数据库的状态
        self.con.commit()
        # 使用execute()方法执行SQL语句
        self.cur.execute(sql)
        res = self.cur.fetchall()
        return res


db = HandleDB(host=conf.get('database', 'host'),
              user=conf.get('database', 'user'),
              password=conf.get('database', 'password'),
              port=conf.getint('database', 'port'),
              charset=conf.get('database', 'charset'))
#
# res = db.find_data('select * from futureloan.member')
# print(res)

# #
# # 3、执行sql语句
# sql = 'select * from futureloan.member'
# res = cur.execute(sql)  # 执行查询数据的sql，结果为sql查询的所有结果条数
#
# # 4、取得结果集的下一行
# data = cur.fetchone()
#
# # 5、取得结果集的所有内容
# data_all = cur.fetchall()
# print(data)
