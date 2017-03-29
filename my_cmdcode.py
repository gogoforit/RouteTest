import os
# commands = 'python'
# os.system(commands)
#命令行导出csv文件
def output():
   # os.chdir( r"H:\mong\bin")
    os.system('mongoexport -d qiandao_last_info -c info --csv -f time,mac,class_num,name -o qiandao_last_info.csv')
