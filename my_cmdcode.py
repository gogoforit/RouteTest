import os
# commands = 'python'
# os.system(commands)
#命令行导出csv文件
def output():
    os.chdir( r"H:\mong\bin")
    os.system('mongoexport -d qiandao_last_info -c info --type=csv -f time,mac,name -o qiandao_last_info.csv')