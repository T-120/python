import xlrd
import xlsxwriter


class ExcelUtil:
    def __init__(self, readUrl='', writeUrl='', sheetName='Sheet1'):
        self.readUrl = readUrl
        self.writeUrl = writeUrl
        self.sheetName = sheetName

    # 解决使用xlrd读取excel数据时，整数变小数的解决办法
    def changeCellToInt(self, sheet, rows, cols):
        dataList = []
        for i in range(rows):
            row = []
            for j in range(cols):
                ctype = sheet.cell(i, j).ctype  # 表格的数据类型
                cell = sheet.cell_value(i, j)

                if ctype == 2 and cell % 1 == 0.0:  # ctype为2且为浮点
                    cell = int(cell)  # 浮点转成整型
                row.append(cell)

            dataList.append(row)
        return dataList

    # 读取Excel文件

    def readExcelToList(self):
        # 打开execl
        workbook = xlrd.open_workbook(self.readUrl)
        # 输出Excel文件中所有sheet的名字
        for sheetName1 in workbook.sheet_names():
            if sheetName1 == self.sheetName:
                dataList = []
                Data_sheet = workbook.sheet_by_name(sheetName1)
                dataList = self.changeCellToInt(
                    Data_sheet, Data_sheet.nrows, Data_sheet.ncols)
                return dataList
            else:
                print("请输入正确的sheet名字！")

    # 将结果写入Excel
    def writeExcelWithList(self, dataList):
        try:
            workbook = xlsxwriter.Workbook(self.writeUrl)  # 创建一个Excel文件
            worksheet = workbook.add_worksheet()  # 创建一个sheet
            print('正在保存结果...')
            for i in range(0, len(dataList)):
                worksheet.write_row("A" + str(i + 1), dataList[i])

            workbook.close()
            print("保存成功")
        except:
            print("请检查结果保存路径是否正确！")

    def saveResult(self, dataList):
        if self.writeUrl == None:
            print("错误", "请选择结果保存路径！")
        else:
            print("开始保存")
            try:
                workbook = xlsxwriter.Workbook(self.writeUrl)  # 创建一个Excel文件
                worksheet = workbook.add_worksheet()  # 创建一个sheet
                for i in range(0, len(dataList)):
                    for j in range(0, len(dataList[i])):
                        worksheet.write_string(i, j, str(dataList[i][j]))

                workbook.close()
                print("保存成功！")

                return True
            except Exception:
                print("error: 保存失败！")
                return False
