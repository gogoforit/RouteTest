import os
import re
def get_pid():
    k = os.popen("create_ap  --list-running")
    k = k.read()
    k = k.split('\n')
    k = k[2].split(' ')
    pid = k[0]
    print(pid)
    return pid

