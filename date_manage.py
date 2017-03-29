import csv
#打开文件，用with打开可以不用去特意关闭file了，python3不支持file()打开文件，只能用open()
def solve():
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
    with open("qiandao_last_info.csv","r",encoding="utf-8") as csvfile:
    #读取csv文件，返回的是迭代类型
        read = csv.reader(csvfile)
        for i in read:
            # print (i)
            if i[2] == 1:
                class_1.append(i)
            elif i[2] == 2:
                class_2.append(i)
            elif i[2] == 3:
                class_3.append(i)
            elif i[2] == 4:
                class_4.append(i)
            else:
                class_other.append(i)
    for i  in range (0,5):
        thefile = "class_" + str(i+1) + '.csv'

        with open(thefile, "w", newline="") as datacsv:
            # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符

            csvwriter = csv.writer(datacsv, dialect=("excel"))

            # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）

            csvwriter.writerow(["A", "B", "C", "D"])
            for each in class_all[i]:
                csvwriter.writerow(each)

