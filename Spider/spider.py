import xlrd
import re
import time
import datetime
from urllib import request

a = input("请输入Excel表的路径:")  # eg: C:\Users\Administrator\Desktop\小说.xls(xlsx)
excel_path = xlrd.open_workbook('{}'.format(a))  # 打开excle文件读取数据
sheet = excel_path.sheets()[0]  # 按索引读取第一个表
urls = sheet.col_values(1)  # 读取第1列的网址并保存为一个列表
keywords = sheet.col_values(0)  # 读取第0列的关键词也保存为一个列表
b = input("请输入要保存的路径")  # eg: C:\Users\Administrator\Desktop\
# d1 = datetime.datetime.now()
for i, url in enumerate(urls):  # 带下标的遍历urls列表
    name = keywords[i] + url.split("/")[4] + '.html'  # 拼接要保存的文件名 关键词+url中的序号+.html
    name = re.sub(r'/|\\|:|\?| |"|<|>|\|', '', name)  # 将name中的非法字符全部替换为空
    try:  # 防止一些网址不能访问，程序直接停止
        # time.sleep(0.1)  # 每爬完一个网页程序停止0.1秒
        file = request.urlopen(url)  # 爬取网页
        data = file.read()  # 读取整个页面
        with open(b + name, "wb") as f:  # 通过open()函数打开该文件，“wb”以二进制写入形式打开，name为文件名
            f.write(data)  # 将data数据写入到创建的文件里
            print(name + "保存成功")
        f.close()  # 写完数据之后将文件关闭
    except Exception as e:  # 捕获无法爬取的错误
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')  # 获取当前时间
        log = now_time + 'log.txt'  # 定义日志文件名
        with open(log, 'a', encoding="utf-8") as f:  # with open()方法打开日志文件，如果没有就新生成一个文件，a追加内容
            f.write(url + '，网站打开失败,抛出异常：' + str(e) + '\n')  # 将错误写入日志文件
# d2 = datetime.datetime.now()
# d3 = d2 - d1
# print(d3)
