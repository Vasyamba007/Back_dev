from collections import deque


def array_reconstruct(a):
    """
    Функция реконструирет массив
    """
    d = dict()
    for i, j in a:
        d[i] = d.get(i, {j}) | {j}
        d[j] = d.get(j, {i}) | {i}
    print(d)

    res = deque()
    for key, values in d.items():
        if len(values) == 2:
            
            res.extend([values.pop(), key, values.pop()])
        else:
            res.extend([values.pop(), key])
    return tuple(res)
        
   


def main():
    input1 = [[4, 5], [6, 8], [6, 5], [4, 9]]
    print(array_reconstruct(input1))



if __name__ == '__main__':
    main()