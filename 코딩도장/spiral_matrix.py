import numpy as np

# define matrix size
m = 10
n = 10
spiral_matrix = np.zeros((m, n))

# input first row
spiral_matrix[0, :] = range(n)

# initialize variables
current_number = n - 1
current_direction = 0
x_position = 0
y_position = n - 1
sub_num = 0
m_iter = m
n_iter = n

if m > n:
    iter_max = (min(m, n) - 1) * 2 + 1
else:
    iter_max = (min(m, n) - 1) * 2

for i in range(iter_max, 0, -1):
    current_direction += 1
    sub_num += 1
    if sub_num % 2 == 0:
        n_iter -= 1
        iter_inner = n_iter
    else:
        m_iter -= 1
        iter_inner = m_iter

    for k in range(iter_inner):
        current_number += 1
        if current_direction % 4 == 0:
            y_position += 1
        elif current_direction % 4 == 1:
            x_position += 1
        elif current_direction % 4 == 2:
            y_position -= 1
        elif current_direction % 4 == 3:
            x_position -= 1
        spiral_matrix[x_position, y_position] = current_number
