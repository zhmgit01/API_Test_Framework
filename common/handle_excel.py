"""
操作excel文件类
"""

import openpyxl


class Excel:

    def __init__(self, file_name, sheet_name):
        self.file_name = file_name
        self.sheet_name = sheet_name

    def open(self):
        # 打开文件
        self.wb = openpyxl.load_workbook(self.file_name)
        self.sh = self.wb[self.sheet_name]

    # 读取excel文件
    def read_excel(self):
        # 打开文件
        self.open()
        # 读取文件内容，转换为 list 类型
        res = list(self.sh.rows)
        # 获取文件第一行的数据，拼接为 title 列表
        title = [c.value for c in res[0]]
        # 获取文件内容，拼接为测试数据
        cases_data = []
        for c in res[1:]:
            case_data = [i.value for i in c]
            cases_data.append(dict(zip(title, case_data)))
        return cases_data

    # 写入excel文件
    def write_excel(self, row, column, value):
        # 打开文件
        self.open()
        # 写入数据
        self.sh.cell(row=row, column=column, value=value)
        # 保存数据
        self.wb.save(self.file_name)


if __name__ == '__main__':
    excel = Excel(file_name='E:\practice\py31\project01\data\cases.xlsx', sheet_name='register')
    res = excel.read_excel()
    print(res)
