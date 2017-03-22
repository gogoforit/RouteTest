import os
# commands = 'python'
# os.system(commands)
def output():
    os.chdir( r"H:\mong\bin")
    os.system('mongoexport -d qiandao_last_info -c info --type=csv -f time,mac,name -o H:\code\路由测试\qiandao_last_info.csv')