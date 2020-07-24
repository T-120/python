import requests
from requests.packages import urllib3
from urllib.error import HTTPError
import bs4
from bs4 import BeautifulSoup
import re
import xlrd
import xlsxwriter
import time
import random

user_agent = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
    "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
]

# 国内高匿代理IP，返回当前页的所有ip


def get_ip_list():
    # 获取代理IP（取当前页的ip列表，每页100条ip）
    url = "http://www.xicidaili.com/nn"
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip, deflate, sdch",
               "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
               "Referer": "http://www.xicidaili.com",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
               }
    r = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    data = soup.table.find_all("td")
    # 匹配规则需要用浏览器的开发者工具进行查看
    # 匹配IP：<td>61.135.217.7</td>
    ip_compile = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')
    # 匹配端口：<td>80</td>
    port_compile = re.compile(r'<td>(\d+)</td>')
    # 获取所有IP，返回的是数组[]
    ip = re.findall(ip_compile, str(data))
    # 获取所有端口：返回的是数组[]
    port = re.findall(port_compile, str(data))
    # 组合IP+端口，如：61.135.217.7:80
    return [":".join(i) for i in zip(ip, port)]


# 目标网站url
xanbhxUrl = 'https://sou.xanbhx.com/search?siteid=xsla&q='
dingdiannUrl = 'https://www.dingdiann.com/searchbook.php?keyword='
# 书名列表excel 路径
booksExcelUrl = "C:\\Users\\Louis\Desktop\\1.xlsx"

# 结果保存路径
xanbhxExcelUrl = 'C:/Users/Louis/Desktop//xanbhx1.xlsx'
dingdiannExcelUrl = 'C:/Users/Louis/Desktop//dingdiann1.xlsx'

# 获取书籍搜索列表页面


def getSearchHtml(url, bookName, ips=[]):
    try:
        # 随机选取一个ip
        ip = random.choice(ips)
    except:
        print('无法获取代理')

    proxies = {
        "http": ip,
    }

    headers_ = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Referer": "https://best.zhaopin.com/",
        "User-Agent": random.choice(user_agent),
    }

    urllib3.disable_warnings()
    try:
        r = requests.get(url+bookName, headers=headers_,
                         proxies=proxies, verify=False)
    except HTTPError as e:
        return None

    try:
        bsObj = BeautifulSoup(r.text, 'lxml')
    except AttributeError as e:
        return None
    return bsObj


def getBookInfo(url, bookName, prefixId, suffixId, divClassName,ips = []):
    # 调用方法
    html = getSearchHtml(url, bookName,ips)
    if html == None:
        return []
        print('无法访问')
    else:

        # 解析出书籍信息行
        liDiv = html.findAll('div', {'class', divClassName})
        if liDiv == None:
            print('请手动检查'+bookName)
            return []
        elif len(liDiv) <= 0:
            return []

        liList = liDiv[0].findAll('li')
        # 解析书籍id 并放入列表
        booksList = []
        for bookInfo in liList:
            bookNameSpan = bookInfo.findAll('span', {'class': 's2'})
            bookName1 = bookNameSpan[0].find('a')
            if bookName1 == None:
                continue
            bookName2 = bookName1.text.strip()
            bookId = bookName1.attrs['href']
            bookState = bookInfo.findAll('span', {'class': 's7'})[0].text
            bookList = []
            if bookName2 == bookName:
                bookList.append(bookName)
                bookId1 = re.sub(prefixId, '', bookId)
                bookId2 = re.sub(suffixId, '', bookId1)
                bookList.append(bookId2)
                if bookState.strip() == '完成':
                    bookList.append(1)
                elif bookState.strip() == '连载':
                    bookList.append(0)
                if len(bookInfo) > 1:
                    booksList.append(bookList)

        global count
        count += 1
        print(bookName + ' ' + str(count))
        if len(booksList) == 0:
            return [[bookName, '', 0]]
        else:
            return booksList

# 读取Excel文件


def readExcel(url, sheetName):
    # 打开execl
    workbook = xlrd.open_workbook(url)
    # 输出Excel文件中所有sheet的名字
    for sheetName1 in workbook.sheet_names():
        if sheetName1 == sheetName:
            dataList = []
            Data_sheet = workbook.sheet_by_name(sheetName1)
            rowNum = Data_sheet.nrows

            for rowCount in range(rowNum):
                dataList.append(Data_sheet.row_values(rowCount))
            return dataList
        else:
            print("请输入正确的sheet名字！")

# 将结果写入Excel


def saveResult(dataList, fileUrl):
    try:
        workbook = xlsxwriter.Workbook(fileUrl)  # 创建一个Excel文件
        worksheet = workbook.add_worksheet()  # 创建一个sheet
        for i in range(0, len(dataList)):
            worksheet.write_row("A" + str(i + 1), dataList[i])
        workbook.close()
        print("保存成功")
    except:
        print("请检查结果保存路径是否正确！")


def main():

    ips = get_ip_list()

    count = 0

    booksName = readExcel(booksExcelUrl, 'Sheet1')
    dLists = []
    xLists = []
    for book in booksName:
        # 每隔30次重新获取一次最新的代理IP
        count +=1 
        if count % 30 == 0:
            ips.extend(get_ip_list())

        if book[0] == '':
            continue
        dList = getBookInfo(dingdiannUrl, book[0], '/ddk', '/', 'novelslist2',ips)
        dLists = dLists+dList
        xList = getBookInfo(
            xanbhxUrl, book[0], 'https://www.xinxs.la/[0-9]+_', '/', 'search-list',ips)
        xLists = xLists+xList
        # time.sleep(2)
        saveResult(dLists, dingdiannExcelUrl)
        saveResult(xLists, xanbhxExcelUrl)


main()
