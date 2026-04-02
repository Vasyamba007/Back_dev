def sort_selection(arr: list, reverse: bool=False) -> None:
    '''
    Сортировка выбором. 
    Сложность по времени: О(N^2)
    Сложность по памяти: O(1)
    Не устойчивая.
    '''
    n = len(arr)
    for i in range(n - 1):
        indx_min = i
        for j in range(i + 1, n):
            if not reverse and arr[j] < arr[indx_min]:
                indx_min = j
            elif reverse and arr[j] > arr[indx_min]:
                indx_min = j
        arr[i], arr[indx_min] = arr[indx_min], arr[i]


def main():
    unsorted_list = [8, 5, -10, 11, 0]
    sort_selection(unsorted_list)
    print(unsorted_list)

    unsorted_list = [8, 5, -10, 11, 0]
    sort_selection(unsorted_list, True)
    print(unsorted_list)


if __name__ == '__main__':
    main()


