import os
import re
import get_pid
def get():
    #获取ap热点的pid
    pid = get_pid.get_pid()
    #构造查询这个ap热点的命令
    mycommand = "create_ap --list-clients " + pid
    info = os.popen(mycommand)
    info = info.read()
    info = info.split('\n')
    macs = []
    for each in info:
        theinfo = each.split(' ')
        for each2 in theinfo:
          if ':' in each2:
           each2 = each2.replace(':','-')
           mac = each2
           macs.append(mac)
       # if ':' in each:
         # mac = each
         # macs.append(mac)
    print(macs)
    return macs

