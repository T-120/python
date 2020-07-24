import re


def fuzzyMatch():
    value = '西西'
    list = ['大海西西的', '大家西西', '打架', '西都好快', '西西大化']
    tempList = []
    pattern = '.*' + value + '.*'
    for s in list:
        obj = re.findall(pattern, s)

        if len(obj) > 0:
            tempList.extend(obj)
    print(tempList)


fuzzyMatch()
