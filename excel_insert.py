import xlrd
def insert():
    fname = "1518028手机MAC地址.xlsx"
    bk = xlrd.open_workbook(fname)
    shxrange = range(bk.nsheets)
    try:
        sh = bk.sheet_by_name("Sheet1")
    except:
        print("no sheet in %s named Sheet1" % fname)
    # 获取行数
    nrows = sh.nrows
    # 获取列数
    ncols = sh.ncols
    print("nrows %d, ncols %d" % (nrows, ncols))
    # 获取第一行第一列数据
    cell_value = sh.cell_value(1, 1)
    # print cell_value

    row_list = []
    # 获取各行数据
    for i in range(1, nrows):
        dic = {}
        row_data = sh.row_values(i)
        dic['mac'] = row_data[2]
        dic['name'] = row_data[0]
        print(row_data[2],row_data[0])
        row_list.append(dic)
    return row_list
