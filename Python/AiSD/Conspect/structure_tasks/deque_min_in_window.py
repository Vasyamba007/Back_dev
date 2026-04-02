from collections import deque


def min_in_window(a: list, k: int) -> list:
    '''
    Находит минимальный элемент в пределах окна, которое передвигается по массиву
    :param a: массив
    :type k: размер окна
    '''
    # В дэке хранятся индексы массива а, порядок индексов поддерживается таким,
    # чтобы значения а[i] в дэке всегда возрастали. Поэтому deq[0] - всегда минимум в окне.
    deq = deque()
    for i in range(k):
        while deq and a[deq[-1]] >= a[i]:
            deq.pop() 
        deq.append(i)
    ans = []
    ans.append(a[deq[0]])
    for i in range(k, len(a)):
        while deq and a[deq[-1]] >= a[i]:
            deq.pop() 
        while deq and deq[0] <= i - k:
            deq.popleft()
        deq.append(i)
        ans.append(a[deq[0]])
    return ans


def main():
    print(min_in_window([1, 3, 2, 4, 5, 3, 1], 3))


if __name__ == '__main__':
    main()
