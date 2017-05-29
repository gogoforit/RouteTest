import csv
import os
import time

import config
from models.mongodb_conn import MongoPipeline


def solve():
    # 获取当前路径
    class_number = config.CLASS_NUMBER
    root_cwd = os.getcwd()
    todaytime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    cwd = root_cwd + '/' + str(todaytime)
    os.chdir(cwd)

    student_list = {}
    conn = MongoPipeline()
    conn.open_connection('qiandao_mac_name')
    # 用课程来区别，不仅仅是mac地址，因为每次课的mac地址是
    ids = conn.getIds('info', {'class_num': class_number})
    _id = next(ids, None)
    student_num = 0

    while _id:
        # 统计每个班总的人数
        student_num += 1
        student_name = _id['name']
        student_list[student_name] = 0
        _id = next(ids, None)

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

    for i in read:
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
        student_list_basic = student_list
        with open(thefile, "w", newline="") as datacsv:

            csvwriter = csv.writer(datacsv, dialect=("excel"))

            # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）

            csvwriter.writerow(["time", "mac", "class_num", "name","studentid","connect_time"])
            for each in class_all[i]:
                every_stu = []
                every_stu.append(each[1])
                every_stu.append(each[2])
                every_stu.append(each[3])
                every_stu.append(each[4])
                every_stu.append(each[5])
                every_stu.append(each[6])
                student_list_basic[each[4]] = 1
                csvwriter.writerow(every_stu)

    # 处理出没有来签到的同学的名单
        student_unsigh = []
        for each in student_list_basic:
            if student_list_basic[each] == 0:
                student_unsigh.append(each)

        if len(student_unsigh) != 0 and len(student_unsigh) != student_num:
            student_unsigh_filename =  "class_" + str(i+1) + '_unsign' +'.csv'
            with open(student_unsigh_filename, "w", newline="") as datacsv:
                csvwriter = csv.writer(datacsv, dialect=("excel"))
                for each in student_unsigh:
                    if each == '姓名':
                        continue
                    every_stu = []
                    every_stu.append(each)
                    csvwriter.writerow(every_stu)
    os.chdir(root_cwd)

