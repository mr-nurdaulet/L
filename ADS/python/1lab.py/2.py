a,n,m = map(int,input().split())
res = 1
a=a%m
if m == 1 :
    print(0)
while n > 0 :
    if n % 2 == 1 :
        res = (res * a) % m
        n = n - 1
    else :
        a = (a * a) % m
        n = n // 2
print(res)