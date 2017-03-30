import datetime
dic = {}
mytime = '2017-03-28 00:38:28'
dic['time'] = mytime
#对时间做处理，判断
classtime = mytime.split(' ')
classtime_hms = classtime[1]
classtime_hms = classtime_hms.split(':')
classtime_hour = classtime_hms[0]
classtime_min = classtime_hms[1]
classtime_sec = classtime_hms[2]
# print (classtime_sec)
nowtime = datetime.time(int(classtime_hour),int(classtime_min),int(classtime_sec))
print (nowtime)
class_time_start_1 = datetime.time(8,0,0)
print (class_time_start_1)
class_time_end_1 = datetime.time(10,5,0)
class_time_start_2 = datetime.time(10,20,0)

print (class_time_start_2)
class_time_end_2 = datetime.time(12,0,0)
print (class_time_end_2)
class_time_start_3 = datetime.time(14,0,0)
class_time_end_3 = datetime.time(15,30,0)
class_time_start_4 = datetime.time(15,50,0)
class_time_end_4 = datetime.time(17,30,0)
class_time_test = datetime.time(18,0,0)
class_num = None
print (nowtime > class_time_start_2 and nowtime < class_time_end_2)
if nowtime > class_time_start_1 and nowtime < class_time_end_1:
    class_num = 1
    dic['class_num'] = class_num
elif nowtime > class_time_start_2 and nowtime < class_time_end_2:
    class_num = 2
    dic['class_num'] = class_num
elif nowtime > class_time_start_3 and nowtime < class_time_end_3:
    class_num = 3
    dic['class_num'] = class_num
elif nowtime > class_time_start_4 and nowtime < class_time_end_4:
    class_num = 4
    dic['class_num'] = class_num
else:
    class_num = 5
    dic['class_num'] = class_num

print (dic)