import datetime
import time

import config
from data_handle import data_manage, output_total
from models.mongodb_conn import MongoPipeline
from wifi_route import get_mac

time_interval = 1
class_id = config.CLASS_NUMBER

conn = MongoPipeline()
conn.open_connection('qiandao')
conn2 = MongoPipeline()
conn2.open_connection('qiandao_mac_name')
conn3 = MongoPipeline()  # conn3对应最后的结果，结果导出到csv文件
conn3.open_connection('qiandao_last_info')
conn4 = MongoPipeline()
conn4.open_connection('web_info',username='pipi',password='123456',
                      ip='192.168.1.128')




while True:

    # 开始前，先把所有班级学生的信息发送到远程
    stu_pri_info = conn2.getIds('info',{'class_num':class_id})
    for each_stu in stu_pri_info:
        name = each_stu['name']
        remote_dic = {}
        remote_dic['name'] = name
        remote_dic['connect_status'] = 0
        remote_dic['mac'] = each_stu['mac']
        remote_dic['class_num'] = class_id
        remote_info = conn4.getIds_one('info',{'name':name})
        if remote_info == None:
            conn4.process_item(remote_dic,'info')



    time.sleep(time_interval)

    macs = None
    macs = get_mac.get()
    if len(macs)==0:
        all_students = conn2.getIds('info',{'class_num':class_id})
        for student in all_students:
            name = student['name']
            conn2.update_item({'name': name},
                              {"$set": {"connect_status": 0}}, 'info')

        remote_stus = conn4.getIds('info',{'class_num':class_id})
        for each_stu in remote_stus:
            mac = each_stu['mac']
            conn4.update_item({'mac':mac},
                              {'$set':{'connect_status':0}},'info')
        continue
    # 用于储存，当前是否连接
    dic_sign = []
    for each in macs: # 把所有现在在线MAC地址都存入数据库中
        dic = {}
        dic['mac'] = each
        dic['class_id'] = class_id
        dic['_id'] = each
        dic['_type'] ='mac'
        dic_sign.append(each)
        mytime  = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # 处理出当天的日期
        the_day = mytime.split(' ')[0]
        dic['time'] = mytime
        dic['date'] = the_day
        # 对时间做处理，判断
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
        dic['_id'] = str(the_day) + '/' + str(class_num) + '/' + dic['_id']


        conn.process_item(dic, 'info')
    # 统计哪些人到了，用mac地址和已经存好的姓名对应起来
    # 用课程来区别，不仅仅是mac地址，因为每次课的mac地址是相同的
    ids = conn.getIds('info', {'class_num': class_num,'date':the_day})

    for _id in ids:
        # 如果没有连接，那么连接时间不会增加
        # 连接状态，1表示连接，0表示未连接
        print(_id,13212312313131)
        if _id['mac'] in dic_sign:
            conn2.update_item({'mac':_id['mac']},
                              {"$set":{"connect_status":1}},'info')
            stu_info = conn2.getIds_one('info',{'mac':_id['mac']})
            stu_name = stu_info['name']
            remote_info = conn4.getIds_one('info',{'mac':_id['mac']})
            if remote_info == None:
                remote_dic = {}
                remote_dic['name'] = stu_name
                remote_dic['connect_status'] = 1
                remote_dic['mac'] = _id['mac']
                print(remote_dic)
                conn4.process_item(remote_dic,'info')
            else:
                conn4.update_item({'mac':_id['mac']},
                                 {"$set":{"connect_status":1}},'info')
            print(stu_info)
        else:

            conn2.update_item({'mac': _id['mac']},
                              {"$set": {"connect_status": 0}}, 'info')
            stu_info = conn2.getIds_one('info', {'mac': _id['mac']})
            if stu_info == None:
                continue
            stu_name = stu_info['name']
            remote_info = conn4.getIds_one('info', {'mac': _id['mac']})
            if remote_info == None:
                remote_dic = {}
                remote_dic['name'] = stu_name
                remote_dic['connect_status'] = 0
                remote_dic['mac'] = _id['mac']
                print(remote_dic)
                conn4.process_item(remote_dic, 'info')
            else:
                conn4.update_item({'mac': _id['mac']},
                                  {"$set": {"connect_status": 0}}, 'info')
            continue
        dic_lastinfo = {}
        mac = _id['mac']
        dic_lastinfo['mac'] = _id['mac']
        dic_lastinfo['time'] = _id['time']
        dic_lastinfo['class_id'] = class_id
        dic_lastinfo['class_num'] = dic['class_num']
        dic_lastinfo['connect_time'] = time_interval / 60

        searchInfo = conn2.getIds('info',{'mac': mac})
        theInfo = next(searchInfo,None)
        dic_lastinfo['date'] = the_day

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


    output_total.output() # 导出csv格式文件
    data_manage.solve()
