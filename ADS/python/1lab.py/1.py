def Fgcd( a ,  b):
    while b!=0 :
        c = b
        b = a % b 
        a = c 
    return a ; 


a,b=map(int,input().split())
ans = Fgcd(a,b)
print(ans)