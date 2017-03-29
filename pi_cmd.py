import os
import re
k = os.popen("ip neighbor")
k = k.read()
k = k.split(' ')
for each2 in k:
	if ':' in each2:
		print(each2)
