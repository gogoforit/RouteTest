from MongodbConn import MongoPipeline
import excel_insert
conn = MongoPipeline()
conn.open_connection('qiandao_mac_name')
#插入信息
#格式：
#MAC 姓名
info_list = excel_insert.insert()
# print(info_list)
for each in info_list:
    print(each)
    dic = {}
    if each['mac']:
        dic['mac'] = each['mac']
    if each['name']:
        dic['name'] = each['name']
    dic['_id'] = each['name']
    conn.process_item(dic, 'info')
    print(dic)
