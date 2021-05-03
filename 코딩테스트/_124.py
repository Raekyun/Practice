def solution(n):
    answer = ''
    quotient = (n - 1) // 3
    remainder = (n - 1) % 3
    answer = str(2 ** remainder) + answer
    while quotient > 0:
        quotient = quotient // 3
        remainder = quotient % 3
        answer = str(2 ** remainder) + answer
    return answer
