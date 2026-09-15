def isPrime(n):
    if n < 2 :
        return False
    for i in range(2 , int(n**0.5) + 1):
        if n % i == 0 :
            return False
    return True
n = int(input())
current = 0 
arr = []
while arr.__len__() < n :
    if isPrime(current) :
        arr.append(current)
    current += 1
print(arr[n-1])