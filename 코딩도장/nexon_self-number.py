not_self_number_set = {0}

for n in range(5000):
    n_str = str(n)
    n_len = len(n_str)
    d_n = n
    for k in range(n_len):
        d_n += int(n_str[k])
    not_self_number_set.add(d_n)

sum_self_number = sum(set(range(5000)) - not_self_number_set)
print(sum_self_number)

# print(sum(set(range(1, 5000)) - {x + sum([int(a) for a in str(x)]) for x in range(1, 5000)}))  모범답안


