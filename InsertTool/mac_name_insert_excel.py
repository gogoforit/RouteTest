from MongodbConn import MongoPipeline
from InsertTool import mac_insert as excel_insert
conn = MongoPipeline()
conn.open_connection('qiandao_mac_name')
#插入信息
#格式：
#MAC 姓名
info_list = excel_insert.insert()
# print(info_list)
for each in info_list:
    print(each)
    mac = each['mac'].replace(':','-').lower()
    dic = {}
    if each['mac']:
        dic['mac'] = mac
    if each['name']:
        dic['name'] = each['name']
    if each['studentid']:
        dic['studentid'] = each['studentid']
    dic['_id'] = mac
    conn.process_item(dic, 'info')
    print(dic)
