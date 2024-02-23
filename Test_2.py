a = input()


def is_correct_bracket_seq(a):
    b, c, d = '(', '{', '['
    e, f, g = ')', '}', ']'
    count_1 = 0
    count_2 = 0
    count_3 = 0

    for i in range(len(a)):
        if b == a[i]:
            
        elif c == i:
            count_2 += 1
        elif d == i:
            count_3 += 1

    if count_1 == 0 and count_2 == 0 and count_3 == 0 :
        return True
    else:
        return False


print(is_correct_bracket_seq(a))
