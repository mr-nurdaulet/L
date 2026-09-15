st = input()
s = ""
for c  in st :
    if len(s)>0 and s[-1]==c:
        s = s[:-1]
    else:
        s+=c 
if len(s) == 0 :
    print("Yes")
else:
    print("No")