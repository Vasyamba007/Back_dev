def prod_without_now(a):
    """
    Функция возвращает массив, в котором каждый элемент - произведение всех элементов входного массива, кроме текущего.
    Сложность по времени: О(n)
    """
    n = len(a)
    prod_left, prod_right = 1, 1
    left, right = [], []

    for i in range(n):
        prod_left *= a[i]
        left.append(prod_left)
        prod_right *= a[n - i - 1]
        right.append(prod_right)
    right = right[::-1]

    res = []
    for i in range(n):
        res_add = 1
        if i - 1 >= 0:
            res_add *= left[i - 1]
        if i + 1 < n:
            res_add *= right[i + 1]
        res.append(res_add)

    return res


def main():
    input1 = [1, 2, 3, 3]
    print(prod_without_now(input1))
    input2 = [1, 1, 1, 1, 0]
    print(prod_without_now(input2))


if __name__ == '__main__':
    main()