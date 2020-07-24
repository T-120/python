import xlrd
import xlsxwriter
import os
from multiprocessing.dummy import Pool as ThreadPool  # 线程池
from functools import partial

# 获取批量盗版文件的名称


def getDaoBanFilesName(filePath):
    for root, dirs, files in os.walk(filePath):
        return files

# 对比方法


def duibi(daoBanFileName, daoBanDataList, zhengBanDataList, daoBanColEntry, zhengBanColEntry):
    print(daoBanFileName + "开始对比")
    # # 列表去重
    # newDaoBanDataList = []
    # for i in daoBanDataList:
    #     if i not in newDaoBanDataList:
    #         newDaoBanDataList.append(i)
    resultList = []
    newDaoBanDataList = daoBanDataList

    if len(newDaoBanDataList) > 0 and len(zhengBanDataList) > 0:

        pool = ThreadPool(50)  # 创建一个线程池
        partial_bookDuibi = partial(bookDuibi, daoBanColEntry=daoBanColEntry,
                                    zhengBanDataList=zhengBanDataList, zhengBanColEntry=zhengBanColEntry)  # 提取x作为partial函数的输入变量
        resultList = pool.map(partial_bookDuibi,
                              (daoBanData for daoBanData in newDaoBanDataList))  # 往线程池中填线程
        pool.close()  # 关闭线程池，不再接受线程
        pool.join()  # 等待线程池中线程全部执行完

        # print(a)
        # # count = 0
        # for i in range(0, len(newDaoBanDataList)):
        #     for j in range(0, len(zhengBanDataList)):
        #         if newDaoBanDataList[i][daoBanColEntry - 1] == zhengBanDataList[j][zhengBanColEntry - 1] and newDaoBanDataList[i][daoBanColEntry] == zhengBanDataList[j][zhengBanColEntry]:
        #             resultList.append(newDaoBanDataList[i])
        # count += 1
        # jindu = count / len(newDaoBanDataList)
        # for x in range(1,jindu*100):
        # print()
        # print("完成：" + str(jindu * 100) + "%")
        resultList = list(filter(None, resultList))
        return resultList
    else:
        print('正版书单或盗版书单为空')
        return []


def bookDuibi(daoBanData, daoBanColEntry, zhengBanDataList, zhengBanColEntry):
    # print(daoBanData)
    # print(zhengBanDataList)
    flag = False
    for j in range(0, len(zhengBanDataList)):
        if daoBanData[daoBanColEntry - 1] == zhengBanDataList[j][zhengBanColEntry - 1]and daoBanData[daoBanColEntry] == zhengBanDataList[j][zhengBanColEntry]:
            flag = True

    if flag == False:
        return daoBanData
    # else:
    #     return ['a', 'a', 'a']


# 读取Excel文件
def readExcel(url, sheetName, hasHeader):
    # 打开execl
    workbook = xlrd.open_workbook(url)
    # 输出Excel文件中所有sheet的名字
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
            print("错误", "请输入正确的sheet名字！")


# 将结果写入Excel
def saveResult(dataList, saveFileUrl):
    if saveFileUrl == None:
        print("错误", "请选择结果保存路径！")
    else:
        print(saveFileUrl)
        try:
            print(saveFileUrl)
            workbook = xlsxwriter.Workbook(saveFileUrl)  # 创建一个Excel文件
            worksheet = workbook.add_worksheet()  # 创建一个sheet
            for i in range(0, len(dataList)):
                worksheet.write_row("A" + str(i + 1), dataList[i])

            workbook.close()
            print("保存成功！")

            return True
        except:
            print("错误", "请检查结果保存路径是否正确！")

            return False


def main():

    filePath = "Y:"

    # 文件地址全局变量
    daoBanFilesUrl = getDaoBanFilesName(filePath)
    if len(daoBanFilesUrl) <= 0:
        print("没有盗版书需要对比！")
        return None

    zhengBanFileUrl = filePath+"\\正版去除\\1.xlsx"
    zhengBanDataList = readExcel(zhengBanFileUrl, "Sheet1", False)

    for daoBanFileUrl in daoBanFilesUrl:
        saveFileUrl = filePath+"\\重点侵权书单\\" + \
            str(daoBanFileUrl)

        daoBanDataList = readExcel(
            str(filePath+"\\"+daoBanFileUrl), "Sheet1", False)

        result = duibi(daoBanFileUrl,
                       daoBanDataList, zhengBanDataList, 1, 1)

        # print(result)
        saveResult(result, saveFileUrl)
    # filePath = ''
    # while filePath == '':
    #     filePath = input("请输入盗版文件路径：")

    # daoBanDataList = readExcel(filePath, "Sheet1", False)
    # if len(daoBanDataList) <= 0:
    #     print("没有正版书需要对比！")
    #     return None

    # zhengBanFileUrl = ''
    # while zhengBanFileUrl == '':
    #     zhengBanFileUrl = input("请输入正版文件路径：")

    # zhengBanDataList = readExcel(zhengBanFileUrl, "Sheet1", False)
    # if len(zhengBanDataList) <= 0:
    #     print("没有正版书需要对比！")
    #     return None

    # saveFileUrl = ''
    # while saveFileUrl == '':
    #     saveFileUrl = input("请输入保存文件夹路径：")

    # result = duibi(filePath,
    #                daoBanDataList, zhengBanDataList, 1, 1)

    # # print(result)
    # saveResult(result, saveFileUrl)


main()
