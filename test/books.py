import xlrd
import xlwt
from xlrd import xldate_as_tuple
import datetime


class ExcelData:
    def __init__(self, data_path, sheetname):
        self.data_path = data_path
        # 工作表名称
        self.sheetname = sheetname
        # 使用xlrd模块打开excel表读取数据
        self.data = xlrd.open_workbook(self.data_path)
        # 根据工作表的名称获取工作表中的内容（方式①）
        self.table = self.data.sheet_by_name(self.sheetname)
        # 根据工作表的索引获取工作表的内容（方式②）
        # self.table = self.data.sheet_by_name(0)
        # 获取第一行所有内容,如果括号中1就是第二行，这点跟列表索引类似
        self.keys = self.table.row_values(0)
        # 获取工作表的有效行数
        self.rowNum = self.table.nrows
        # 获取工作表的有效列数
        self.colNum = self.table.ncols

    def read_agent_excel(self, row):
        data = []
        for i in range(row, self.rowNum):
            sheet_data = {}
            for j in range(self.colNum):
                c_type = self.table.cell(i, j).ctype
                c_cell = self.table.cell_value(i, j)
                if c_type == 2 and c_cell % 1 == 0:
                    c_cell = int(c_cell)
                elif c_type == 3:
                    date = datetime.datetime(*xldate_as_tuple(c_cell, 0))
                    c_cell = date.strftime('%Y-%d-%m %H:%M:%S')
                elif c_type == 4:
                    c_cell = True if c_cell == 1 else False
                sheet_data[self.keys[j]] = c_cell
            data.append(sheet_data)
        return data, self.keys

    @classmethod
    def write_data(cls, excel_data, p, heads):
        """
        p:一行写入表格的列数
        """
        data_list = []
        for data in excel_data:
            for value in data.values():
                data_list.append(value)
        new_list = [data_list[i:i + p] for i in range(0, len(data_list), p)]
        xls = xlwt.Workbook()
        sheet = xls.add_sheet('Sheet1', cell_overwrite_ok=True)
        style = "pattern: pattern solid, fore_colour red"
        # red_style = xlwt.easyxf(style)
        ls = 0
        # 地址
        # BASE_DIR = "C:\\Users\\Administrator\\Desktop\\"
        a = input("请输入保存Excel表的名称:")
        path = common_path + a
        for head in heads:
            sheet.write(0, ls, head)
            ls += 1
            i = 1
            for list in new_list:
                j = 0
                for data in list:
                    sheet.write(i, j, data)
                    j += 1
                i += 1
            xls.save(path)
        return path


common_path = 'C:\\Users\\Administrator\\Desktop\\对比书单\\'
original = input("请输入正版书单Excel表名:")
bootleg = input("请输入盗版书单Excel表名:")
path1 = common_path + original
path2 = common_path + bootleg
# xl = pandas.ExcelFile(path1)
# sheet_names = xl.sheet_names
get_data = ExcelData(path1, "Sheet1")
data1, keys1 = get_data.read_agent_excel(1)

# xl2 = pandas.ExcelFile(path2)
# sheet_names = xl2.sheet_names
get_data2 = ExcelData(path2, "Sheet1")
data2, keys2 = get_data2.read_agent_excel(1)

click = dict()
for i in data2:
    click[i['文章名']] = i['点击量']
keys = click.keys()
for i in data1:
    if i['文章名'] in keys:
        i['点击量'] = click[i['文章名']]
    else:
        i['点击量'] = " "
book = get_data.write_data(data1, 7, keys1)
