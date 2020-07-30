import xlrd
import re
import datetime
from urllib import request
from concurrent.futures import ThreadPoolExecutor


a = input(r"请输入Excel表的路径:")  # eg: C:\Users\Administrator\Desktop\小说.xls(xlsx)   d:\py\story\wap.faloo.com.xlsx
excel_path = xlrd.open_workbook(a)  # 打开excle文件读取数据
sheet = excel_path.sheets()[0]  # 按索引读取第一个表
urls = sheet.col_values(1)  # 读取第1列的url网址并保存为一个列表
save_way = input(r"请输入保存的路径:")  # eg: C:\Users\Administrator\Desktop\


def spider(save_way, file, name, *args, **kwargs):  # 将爬虫方法打包成一个函数
    try:
        data = file.read()  # 读取整个页面
        with open(save_way + name, "wb") as f:  # with open()方法打开该文件，“wb”以二进制写入形式打开，name为文件名
            f.write(data)  # 将data数据写入到创建的文件里
            print(name + "保存成功")
        f.close()  # 写完数据之后将文件关闭
    except Exception as e:  # 捕获错误并保留进日志中
        # now_time = datetime.datetime.now().strftime('%Y-%m-%d')  # 获取当前时间
        log = 'log.txt'  # 定义日志文件名
        with open(log, 'a', encoding="utf-8") as f:  # with open()方法打开日志文件，如果没有就新生成一个文件，a追加内容
            f.write(str(e) + '\n')  # 将错误写入日志文件


def scrapy_webpage(urls):
    for url in urls:  # 遍历urls列表
        # print("url:"+str(url))
        name = url + '.html'  # 拼接要保存的文件名 url + .html
        name = re.sub(r'/|\\|:|\?| |"|<|>|\|', '', name)  # 将name中的非法字符全部替换为空
        try:  # 防止一些网址不能访问导致程序直接停止
            file = request.urlopen(url, timeout=10)  # 爬取网页
        except:  # 访问失败进行的操作
            try:  # 重新访问一遍url
                file = request.urlopen(url, timeout=10)  # 爬取网页
            except Exception as e:  # 两次都无法访问时，捕获错误并保留进日志中
                now_time = datetime.datetime.now().strftime('%Y-%m-%d')  # 获取当前时间
                log = now_time + 'log.txt'  # 定义日志文件名
                with open(log, 'a', encoding="utf-8") as f:  # with open()方法打开日志文件，如果没有就新生成一个文件，a追加内容
                    f.write(url + '，网站打开失败,抛出异常：' + str(e) + '\n')  # 将错误写入日志文件
            else:  # 第二次try成功时会调用
                spider(save_way, file, name)  # 调用爬虫函数
        else:  # 第一次try成功时会调用
            spider(save_way, file, name)  # 调用爬虫函数


if __name__ == '__main__':
    time1 = datetime.datetime.now()

    with ThreadPoolExecutor(max_workers=16) as pool:  # 创建线程池就是把现成的开启和释放变成借和换,减少开销
        future = pool.submit(scrapy_webpage, urls)  # future将来时对象

    time2 = datetime.datetime.now()
    print(time2 - time1)
