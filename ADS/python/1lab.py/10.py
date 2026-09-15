from collections import deque

def solve():
    n = int(input())
    dq = deque()

    for i in range(n , 0 , -1):
        dq.appendleft(i)
        for _ in range(i):
                x = dq.pop()
                dq.appendleft(x)
    print(*dq)

t = int(input())
for _ in range(t):
    solve()
