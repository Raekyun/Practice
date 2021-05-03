# def solution(array, commands):
#     answer = []
#     for command in commands:
#         array_cut = array[command[0]-1 : command[1]]
#         array_cut_sorted = sorted(array_cut)
#         answer.append(array_cut_sorted[command[2]-1])
#     return answer


def solution(array, commands):
    return list(map(lambda x: sorted(array[x[0] - 1:x[1]])[x[2] - 1], commands))
