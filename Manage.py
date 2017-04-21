#路由器重新开机以后必须要先连一下网才可以进入后台
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
while True:

    # s = requests.session()
    # #登陆路由器后台要post出去的数据
    # data = {
    #     'login':{'password':"WlD8wX02ceefbwK"}
    # ,
    # 'method':"do"
    # }
    # #头标签
    # header = {
    # "Host":"192.168.1.1",
    # "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv,:52.0) Gecko/20100101 Firefox/52.0",
    # "Accept":"application/json, text/javascript, */*; q=0.01",
    # "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    # "Accept-Encoding":"gzip, deflate",
    # "Content-Type":"application/json; charset=UTF-8",
    # "X-Requested-With":"XMLHttpRequest",
    # "Referer":"http://192.168.1.1/",
    # "Content-Length":"54",
    # "Connection":"keep-alive",
    # }
    # #post数据，登陆路由器后台控制界面
    # html = s.post('http://192.168.1.1/',data=json.dumps(data),headers = header).json()
    #
    # #post获取在线的设备MAC地址等信息的包
    # datahost = {
    # 'hosts_info':{'table':"online_host"},
    # 'method':"get"
    # }
    # stok = html['stok']
    # nexturl = 'http://192.168.1.1/stok=' + stok + '/ds'
    # # nexturl = 'http://192.168.1.1/stok=7%5BuVF%7CF%24v6W3HvDXpeiKr%2Bc%2BsoSrHPA%3E/ds'
    # #获取在线设备等的MAC地址
    # hostinfo = s.post(nexturl,data=json.dumps(datahost)).json()
    # info = json.dumps(hostinfo)
    #正则匹配出所有的MAC地址
    macs = None
    macs = GetMac.get()
    # macs = re.findall('"mac": "(.*?)"',info,re.S)

    #存入数据库
    conn = MongoPipeline()
    conn.open_connection('qiandao')
    for each in macs: #把所有现在在线MAC地址都存入数据库中
        # print(each)
        dic = {}
        dic['mac'] = each
        dic['_id'] = each
        dic['_type'] ='mac'
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
        class_time_end_1 = datetime.time(9,0,0)
        class_time_start_2 = datetime.time(10,0,0)
        class_time_end_2 = datetime.time(11,0,0)
        class_time_start_3 = datetime.time(13,30,0)
        class_time_end_3 = datetime.time(14,30,0)
        class_time_start_4 = datetime.time(15,35,0)
        class_time_end_4 = datetime.time(16,30,0)
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
        ids = conn.getIds('info', {'_id': str(class_num) + ':' +each})
        id = next(ids, None)
        dic['_id'] = str(the_day) + '/' + str(class_num) + '/' + dic['_id']
        if id!=None:
            conn.update_item({'_id': each}, {"$set": {"num": id['num']+1}}, 'info')
            continue
        else:
            dic['num'] = 1
            conn.process_item(dic, 'info')
    print(dic)
    #统计哪些人到了，用mac地址和已经存好的姓名对应起来
    conn = MongoPipeline()
    conn.open_connection('qiandao')
    #用课程来区别，不仅仅是mac地址，因为每次课的mac地址是
    ids = conn.getIds('info', {'class_num': class_num,'date':the_day})
    _id = next(ids, None)
    while _id:
        # print(_id)
        dic_lastinfo = {}
        mac = _id['mac']
        dic_lastinfo['mac'] = _id['mac']
        dic_lastinfo['time'] = _id['time']
        dic_lastinfo['class_num'] = dic['class_num']
        conn2 = MongoPipeline()
        conn2.open_connection('qiandao_mac_name') #conn2储存的mac地址和对应的名字
        searchInfo = conn2.getIds('info',{'mac': mac})
        theInfo = next(searchInfo,None)
        # print(theInfo)
        # print(123)
        conn3 = MongoPipeline()#conn3对应最后的结果，结果导出到csv文件
        conn3.open_connection('qiandao_last_info')
        if theInfo!=None:
            dic_lastinfo['name'] = theInfo['name']
            dic_lastinfo['_id'] = str(the_day) + '/' + str(dic['class_num']) + '/' + theInfo['name']

            try:
                 dic_lastinfo['studentid'] = theInfo['studentid']
            except :
                pass
            conn3.process_item(dic_lastinfo, 'info')
        _id = next(ids, None)

    OutputCsvTotal.output() #导出csv格式文件
    DateManage.solve()
#
# print(hostinfo)
# print(nexturl)
# print(stok)
# print(html)
