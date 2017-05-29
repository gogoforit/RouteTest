from insert_tools import mac_insert as excel_insert
from models.mongodb_conn import MongoPipeline

conn = MongoPipeline()
conn.open_connection('qiandao_mac_name')

class_number = 28
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
    dic['class_num'] = class_number
    conn.process_item(dic, 'info')
    print(dic)
