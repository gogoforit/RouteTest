from mongodb_conn import MongoPipeline
conn = MongoPipeline()
conn.open_connection('qiandao_mac_name')
#插入信息
#格式：
#MAC 姓名
#以字符c结束
header = input("")
k = ''
while header !='c':
    dic = {}
    k = header.split(' ')
    dic['mac'] = k[0]
    dic['name'] = k[1]
    dic['_id'] = k[0]
    conn.process_item(dic, 'info')
    print(dic)
    header = input("")

# arr = k.splitlines()
# print(arr)
