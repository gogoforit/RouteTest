import csv
import time
import os
#打开文件，用with打开可以不用去特意关闭file了，python3不支持file()打开文件，只能用open()
def solve():
    #获取当前路径
    root_cwd = os.getcwd()
    todaytime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    cwd = root_cwd + '/' + str(todaytime)
    os.chdir(cwd)

    class_1 = []
    class_2 = []
    class_3 = []
    class_4 = []
    class_other = []
    class_all = []
    class_all.append(class_1)
    class_all.append(class_2)
    class_all.append(class_3)
    class_all.append(class_4)
    class_all.append(class_other)
    read = []
    with open("qiandao_last_info.csv", "r", encoding="utf-8") as csvfile:
        theread = csv.reader(csvfile)
        for i in theread:
            mytime = i[0].split('/')[0]
            mylist = list(mytime)
            todaylist = list(todaytime)
            if str(mytime) == str(todaytime):
                read.append(i)

    # with open("qiandao_last_info.csv","r",encoding="utf-8") as csvfile:
    #读取csv文件，返回的是迭代类型
        # read = csv.reader(csvfile)
    for i in read:
        # print (i)
        if i[3] == '1':
            class_1.append(i)
        elif i[3] == '2':
            class_2.append(i)
        elif i[3] == '3':
            class_3.append(i)
        elif i[3] == '4':
            class_4.append(i)
        else:
            class_other.append(i)
    for i  in range (0,5):
        thefile = "class_" + str(i+1) + '.csv'

        with open(thefile, "w", newline="") as datacsv:
            # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符

            csvwriter = csv.writer(datacsv, dialect=("excel"))

            # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）

            csvwriter.writerow(["time", "mac", "class_num", "name","studentid"])
            for each in class_all[i]:
                csvwriter.writerow(each)
    os.chdir(root_cwd)

