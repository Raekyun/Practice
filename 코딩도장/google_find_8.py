n = 0

for x in range(1,10000):
    for a in str(x):
        if int(a)==8:
            n+=1

print(n)

# 모범답안: str(list(range(1,10001))).count('8')