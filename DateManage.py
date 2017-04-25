import csv
import time
import os
import Config
from MongodbConn import MongoPipeline
#打开文件，用with打开可以不用去特意关闭file了，python3不支持file()打开文件，只能用open()
def solve():
    #获取当前路径
    class_number = Config.CLASS_NUMBER
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
        #统计每个班总的人数
        student_num += 1
        # print(_id)
        student_name = _id['name']
        print(student_name)
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
                every_stu = []
                every_stu.append(each[1])
                every_stu.append(each[2])
                every_stu.append(each[3])
                every_stu.append(each[4])
                every_stu.append(each[5])
                # print(each[4])
                student_list[each[4]] = 1

               # print(every_stu)
                csvwriter.writerow(every_stu)
    #处理出没有来签到的同学的名单
        student_unsigh = []
        for each in student_list:
            if student_list[each] == 0:
                student_unsigh.append(each)

        if len(student_unsigh) != 0 and len(student_unsigh) != student_num:
            print(student_unsigh)
            student_unsigh_filename =  "class_" + str(i+1) + '_unsign' +'.csv'
            with open(student_unsigh_filename, "w", newline="") as datacsv:
                csvwriter = csv.writer(datacsv, dialect=("excel"))
                for each in student_unsigh:
                    csvwriter.writerow(each)
    os.chdir(root_cwd)

