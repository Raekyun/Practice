multi_of_three = {3 * i for i in range(1,334)}
multi_of_five = {5 * i for i in range(1,200)}

answers = sum(multi_of_three.union(multi_of_five))

# sum([x for x in range(1000) if x%3==0 or x%5==0]) 모범답안 1

# set3 = set(range(3, 1000, 3))      모범답안 2
# set5 = set(range(5, 1000, 5))
#
# print sum(set3 | set5)