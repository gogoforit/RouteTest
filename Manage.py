
import requests
import json
import re
from MongodbConn import MongoPipeline
import time
import OutputCsvTotal
import datetime
import DateManage
import GetMac
import GetWlan0Pid

# last_time = time.time()
# now_time = None
# sum_time = 0

# 每次扫描的时间间隔
time_interval = 1

while True:
    time.sleep(time_interval)
    # now_time = time.time()
    # sub_time = now_time - last_time

    macs = None
    macs = GetMac.get()
    # macs = re.findall('"mac": "(.*?)"',info,re.S)
    if len(macs)==0:
        continue
    #存入数据库
    conn = MongoPipeline()
    conn.open_connection('qiandao')
    #用于储存，当前是否连接
    dic_sign = {}
    for each in macs: #把所有现在在线MAC地址都存入数据库中
        # print(each)
        dic = {}
        dic['mac'] = each
        dic['_id'] = each
        dic['_type'] ='mac'
        dic_sign[each] = '1'
        mytime  = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        #处理出当天的日期
        the_day = mytime.split(' ')[0]
        dic['time'] = mytime
        dic['date'] = the_day
        #对时间做处理，判断
        classtime = mytime.split(' ')
        classtime_hms = classtime[1]
        classtime_hms = classtime_hms.split(':')
        classtime_hour = classtime_hms[0]
        classtime_min = classtime_hms[1]
        classtime_sec = classtime_hms[2]
        nowtime = datetime.time(int(classtime_hour),int(classtime_min),int(classtime_sec))
        class_time_start_1 = datetime.time(8,0,0)
        class_time_end_1 = datetime.time(10, 0, 0)
        class_time_start_2 = datetime.time(10, 5, 0)
        class_time_end_2 = datetime.time(12, 0, 0)
        class_time_start_3 = datetime.time(14,30, 0)
        class_time_end_3 = datetime.time(16, 0, 0)
        class_time_start_4 = datetime.time(16,0,0)
        class_time_end_4 = datetime.time(18, 0, 0)
        class_time_test = datetime.time(18,0,0)
        class_num = None
        dic['class_num'] = 66
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
        else :
            class_num = 5
            dic['class_num'] = class_num
        # ids = conn.getIds('info', {'_id': str(class_num) + ':' +each})
        # id = next(ids, None)
        dic['_id'] = str(the_day) + '/' + str(class_num) + '/' + dic['_id']
        # if id!=None:
        #     conn.update_item({'_id': each}, {"$set": {"num": id['num']+1}}, 'info')
        #     continue
        # else:
        #     dic['num'] = 1

        conn.process_item(dic, 'info')
    #print(dic)
    #统计哪些人到了，用mac地址和已经存好的姓名对应起来
    conn = MongoPipeline()
    conn.open_connection('qiandao')
    #用课程来区别，不仅仅是mac地址，因为每次课的mac地址是
    ids = conn.getIds('info', {'class_num': class_num,'date':the_day})
    _id = next(ids, None)
    while _id:
        # 如果没有连接，那么连接时间不会增加
        if _id['mac'] in dic_sign:
            pass
        else:
            _id = next(ids, None)
            continue
        dic_lastinfo = {}
        mac = _id['mac']
        dic_lastinfo['mac'] = _id['mac']
        dic_lastinfo['time'] = _id['time']
        dic_lastinfo['class_num'] = dic['class_num']
        dic_lastinfo['connect_time'] = time_interval / 60
        conn2 = MongoPipeline()
        conn2.open_connection('qiandao_mac_name') #conn2储存的mac地址和对应的名字
        searchInfo = conn2.getIds('info',{'mac': mac})
        theInfo = next(searchInfo,None)
        # print(theInfo)
        # print(123)
        dic_lastinfo['date'] = the_day
        conn3 = MongoPipeline()#conn3对应最后的结果，结果导出到csv文件
        conn3.open_connection('qiandao_last_info')
        if theInfo!=None:
            dic_lastinfo['name'] = theInfo['name']
            dic_lastinfo['_id'] = str(the_day) + '/' + str(dic['class_num']) + '/' + theInfo['name']
            #计算每节课的连接时间
            judge_insert_update = conn3.getIds('info',{'_id':dic_lastinfo['_id']})
            result_insert_update = next(judge_insert_update,None)
            ans_time = 2.0 
            if result_insert_update == None:

                try:
                     dic_lastinfo['studentid'] = theInfo['studentid']
                except :
                    pass
                conn3.process_item(dic_lastinfo, 'info')
            else:
                conn3.update_item({'_id': dic_lastinfo['_id']},
                                  {"$set": {"connect_time": result_insert_update['connect_time'] + (ans_time) / 60}},
                                  'info')
        _id = next(ids, None)



    OutputCsvTotal.output() #导出csv格式文件
    DateManage.solve()
#
# print(hostinfo)
# print(nexturl)
# print(stok)
# print(html)
