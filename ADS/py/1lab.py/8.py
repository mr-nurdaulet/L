n = int(input())
arr = list(map(int , input().split()))
s = []
for x in arr:
    while len(s) > 0 and s[-1]>= x:
        s.pop()
    if len(s) == 0 :
        print(-1 , end = " ")
    else:
        print(s[-1] , end = " ")
    s.append(x)