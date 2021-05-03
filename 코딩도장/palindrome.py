def a(string):
    max_iter = len(string) // 2
    k = 0
    for i in range(max_iter):
        if string[i] == string[-1 - i]:
            k += 1
            pass
        else:
            print('this is not palindrome')
            break
    if k == max_iter:
        print('this is palindrome')


if __name__ == '__main__':
    string = input('input string: ')
    a(string)
