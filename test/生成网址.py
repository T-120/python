data = []
for n in range(1, 144606):
    a = n // 1000
    url = 'http://www.paoshu8.com/' + str(a) + '_' + str(n) + '/'
    data.append(url)


def text_save(data):
    with open('./1.txt', 'a') as f:
        for i in range(len(data)):
            s = str(data[i]).replace('[', '').replace(']', '')
            s = s.replace("'", '').replace(',', '') + '\n'
            f.write(s)
    print("保存文件成功")


a = text_save(data)
