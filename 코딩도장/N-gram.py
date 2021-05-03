def n_gram(text, n):
    max_iter = len(text) + 1 - n
    for i in range(max_iter):
        print(text[i:n + i])


def n_gram_words(text, n):
    words = text.split(' ')
    words_number = len(words)
    if words_number < n:
        print('wrong inputs: the number of words is less than n')
    else:
        for i in range(words_number + 1 - n):
            for j in range(n):
                print(words[i + j])


if __name__ == '__main__':
    text = input('input text: ')
    n = int(input('input n: '))
    n_gram(text, n)
