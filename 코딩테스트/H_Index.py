# def solution(citations):
#     len_cit = len(citations)
#     answer = 0
#     for i in range(len_cit+1):
#         counter = 0
#         for j in range(len_cit):
#             if citations[j] >= i:
#                 counter += 1
#         if counter >= i:
#             answer = i
#     return answer


def solution(citations):
    citations = sorted(citations)
    l = len(citations)
    for i in range(l):
        if citations[i] >= l-i:
            return l-i
    return 0