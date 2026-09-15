from collections  import deque

boris = deque(map(int,input().split()))
nursik = deque(map(int,input().split()))

move = 0 

while boris and nursik :
    b = boris.popleft()
    n = nursik.popleft()

    if b == 9 and n == 0:
        boris_wins = False
    elif b == 0 and n == 9:
        boris_wins = True
    elif b > n:
        boris_wins = True
    else:
        boris_wins = False

    if boris_wins:
        boris.append(b)
        boris.append(n)
    else:
        nursik.append(b)
        nursik.append(n)

    move += 1

if not boris:
    print("Nursik" , move)
else:
    print("Boris" , move)