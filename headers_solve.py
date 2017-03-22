header = input("shuru\n")
k = ''
while header !='z':
    k += header + '\n'
    header = input("")
arr = k.splitlines()

for each in arr:

    kk = each.split(':')
    if not kk[0].startswith('"'):
        kk[0] ='"'+kk[0]
    if not kk[0].endswith('"'):
        kk[0] = kk[0] + '"'
    if not kk[1].startswith('"'):
        kk[1] = '"' + kk[1]
    if not kk[1].endswith('"'):
        kk[1] = kk[1] + '"' + ','
    print(":".join(kk))