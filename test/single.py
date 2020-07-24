import xlrd
import xlsxwriter
import os
import re
from multiprocessing.dummy import Pool as ThreadPool  # 线程池
from functools import partial


# 获取批量盗版文件的名称
def getDaoBanFilesName(filePath):
    for root, dirs, files in os.walk(filePath):
        return files


# 对比方法
def duibi(daoBanFileName, daoBanDataList, zhengBanDataList, daoBanColEntry, zhengBanColEntry):
    print(daoBanFileName + "开始对比")
    # 列表去重
    newDaoBanDataList = []
    for i in daoBanDataList:
        if i not in newDaoBanDataList:
            newDaoBanDataList.append(i)

    if len(newDaoBanDataList) > 0 and len(zhengBanDataList) > 0:

        pool = ThreadPool(50)  # 创建一个线程池
        partial_bookDuibi = partial(bookDuibi, daoBanColEntry=daoBanColEntry,
                                    zhengBanDataList=zhengBanDataList,
                                    zhengBanColEntry=zhengBanColEntry)  # 提取x作为partial函数的输入变量,固定bookDuibi的三个参数
        a = pool.map(partial_bookDuibi,
                     (daoBanData for daoBanData in newDaoBanDataList))  # 往线程池中填线程,将参数daoBanData传入bookDuibi函数
        pool.close()  # 关闭线程池，不再接受线程
        pool.join()  # 等待线程池中线程全部执行完
        # print(a)
        resultList = []
        result_tortlist = []

        for a1 in a:
            if len(a1[1]) != 0:
                resultList.append(a1[0])
                result_tortlist.extend(a1[1])
        # resultList = list(filter(None, a[0]))
        # result_tortlist = list(filter(None, a[1]))

        # 列表去重
        newResultList = []
        for i in resultList:
            if i not in newResultList:
                newResultList.append(i)

        return (resultList, result_tortlist)
    else:
        print('正版书单或盗版书单为空')
        return []


def bookDuibi(daoBanData, daoBanColEntry, zhengBanDataList, zhengBanColEntry):
    tort_list = []
    value = daoBanData[daoBanColEntry - 1]
    # print(value)
    pattern = '.*' + value + '.*'
    for j in range(0, len(zhengBanDataList)):
        wordkey = zhengBanDataList[j][zhengBanColEntry - 1]
        obj = re.findall(pattern, wordkey)
        if obj:
            tort_list.append(zhengBanDataList[j])

    # print(tort_list)
    a = (daoBanData, tort_list)

    return a


# 读取Excel文件
def readExcel(url, sheetName, hasHeader):  # 打开execl
    workbook = xlrd.open_workbook(url)  # 输出Excel文件中所有sheet的名字
    for sheetName1 in workbook.sheet_names():
        if sheetName1 == sheetName:
            dataList = []
            Data_sheet = workbook.sheet_by_name(sheetName1)
            rowNum = Data_sheet.nrows
            if hasHeader:
                for rowCount in range(rowNum):
                    if rowCount != 0:
                        dataList.append(Data_sheet.row_values(rowCount))
            else:
                for rowCount in range(rowNum):
                    dataList.append(Data_sheet.row_values(rowCount))
            return dataList
        else:
            print("error", "请输入正确的sheet名字！")


# 将结果写入Excel
def saveResult(dataList, saveFileUrl, saveResultName):
    if saveFileUrl == None:
        print("error", "请选择结果保存路径！")
    else:
        print(saveFileUrl)
        try:
            workbook = xlsxwriter.Workbook(saveFileUrl)  # 创建一个Excel文件
            worksheet = workbook.add_worksheet()  # 创建一个sheet
            for i in range(0, len(dataList)):
                for j in range(0, len(dataList[i])):
                    worksheet.write_string(i, j, str(dataList[i][j]))

            workbook.close()
            print(saveResultName + "保存成功！")
            return True
        except:
            print("error: 保存失败！")
            return False


def main():
    filePath = ''
    while filePath == '':
        filePath = input("请输入盗版文件路径：")

    daoBanDataList = readExcel(filePath, "Sheet1", False)
    if len(daoBanDataList) <= 0:
        print("没有盗版书需要对比！")
        return None

    zhengBanFileUrl = ''
    while zhengBanFileUrl == '':
        zhengBanFileUrl = input("请输入正版文件路径：")

    zhengBanDataList = readExcel(zhengBanFileUrl, "Sheet1", False)
    if len(zhengBanDataList) <= 0:
        print("没有正版书需要对比！")
        return None

    saveFileUrl = ''
    while saveFileUrl == '':
        saveFileUrl = input("请输入对比书单保存文件夹路径：")

    saveFileUrl2 = ''
    while saveFileUrl2 == '':
        saveFileUrl2 = input("请输入侵权书单保存文件夹路径：")

    result, result_tort = duibi(filePath,
                                daoBanDataList, zhengBanDataList, 1, 1)

    saveResult(result, saveFileUrl, filePath[0])
    saveResult(result_tort, saveFileUrl2, filePath[0])
    # print(result)
    # print('==========================================================================')
    # print(result_tort)


main()
