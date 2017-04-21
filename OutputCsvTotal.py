import os
import time
# commands = 'python'
# os.system(commands)
#命令行导出csv文件
def output():
    # os.chdir( r"/home/kk/python_code/theinfo/RouteTest")
    root_cwd = os.getcwd()
    mytime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    cwd = root_cwd + '/' + str(mytime)
    isExists = os.path.exists(cwd)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(cwd)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        pass
    os.chdir(cwd)
    os.system('mongoexport -d qiandao_last_info -c info --csv -f _id,time,mac,class_num,name,studentid -o qiandao_last_info.csv')
    os.chdir(root_cwd)
