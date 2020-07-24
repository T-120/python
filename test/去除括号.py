from excelUtil import ExcelUtil
import re

if __name__ == "__main__":

    filePath = input('请输入原文件路径：')
    filePath = "C:\\Users\\Administrator\\Desktop\\晋江文学城\\" + filePath
    # filePath = 'E:\\LM工作记录\\工作记录\\内江小说站点击量情况统计\\六个小说站网站下载书单\\采集书单去除括号\\boluoxs.xlsx'
    # savePath = 'C:\\Users\\Louis\\Desktop\\1\\boluoxs.xlsx'
    savePath = input('请输入保存文件路径：')
    savePath = "C:\\Users\\Administrator\\Desktop\\晋江文学城\\" + savePath

    fileData = ExcelUtil(filePath, savePath)
    # 处理之前的数据
    beforeDatas = fileData.readExcelToList()

    pren = '\[.*?\]|\（.*?\）|\【.*?\】|\(.*?\)|\［.*?\］|\[.*?\］|\［.*?\]'

    results = []
    # print(beforeDatas[0])
    for beforeData in beforeDatas:
        # author_id = beforeData[0]
        # article_name_id = beforeData[1]
        a = beforeData[2]
        article_name = str(beforeData[0]).strip()
        author = str(beforeData[1]).strip()
        # article_name = re.sub(pren, '', article_name)
        # author = re.sub(pren, '', author)
        if a == "已签约":
            results.append([article_name, author, a])

    fileData.saveResult(results)
    # print(results)
