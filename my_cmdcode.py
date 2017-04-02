import os
# commands = 'python'
# os.system(commands)
#命令行导出csv文件
def output():
    os.chdir( r"/home/pi/code/code/RouteTest")
    os.system('mongoexport -d qiandao_last_info -c info --csv -f time,mac,class_num,name,studentid -o qiandao_last_info.csv')
