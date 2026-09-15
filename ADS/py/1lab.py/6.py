def process(s):
    res = ""

    for c in s:
        if(c=='#' and len(res)> 0):
            res = res[:-1]
        else:
            res+=c
    return res
s1,s2 = input().split()
if(process(s1)==process(s2)):
    print("Yes")
else:
    print("No")