from array import array


data = list(map(int, input().split(' ')))
data_1 = array('b', data)



def hill(data):
    data_1 = array('b', data)
    count = 0
    for i in range(len(data_1) - 1):
        if data_1[i] < data_1[i + 1]:
            count += 1
            continue
        elif data_1[i] > data_1[i + 1]:
            count -= 1
            continue
        else:
            return False
    return True

print(hill(data))
