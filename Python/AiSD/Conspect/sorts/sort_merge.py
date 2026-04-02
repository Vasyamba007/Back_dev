
def sort_merge(lst: list | tuple, reverse: bool=False) -> list:
    '''
    Возвращает список, отсортированный методом слияния.
    Сложность по времени: O(n*log(2)n)
    Сложность по памяти: O(n)
    '''
    if (length := len(lst)) < 2:
        return lst
    else:
        mid = length // 2
        a, b = sort_merge(lst[mid:], reverse), sort_merge(lst[:mid], reverse) 
    return merge(a, b, reverse)


def merge(a: list | tuple, b: list | tuple, reverse: bool=False) -> list:
    '''
    Возвращает отсортированный список, полученный слиянием отсортированных массивов a и b.
    '''
    merged_list = []
    i, j = 0, 0
    length_a, length_b = len(a), len(b)
    while i < length_a and j < length_b:
        if not reverse:
            if a[i] < b[j]:
                merged_list.append(a[i])
                i += 1
            else:
                merged_list.append(b[j])
                j += 1
        else:
            if a[i] > b[j]:
                merged_list.append(a[i])
                i += 1
            else:
                merged_list.append(b[j])
                j += 1
    merged_list += a[i:] + b[j:]
    return merged_list


def main():
    sorted_list_1 = [5, 6, 7, 8, 20]
    sorted_list_2 = [4, 5, 6, 10]
    sorted_list_3 = [20, 8, 7, 6, 5]
    sorted_list_4 = [10, 6, 5, 4]
    print(merge(sorted_list_1, sorted_list_2))
    print(merge(sorted_list_3, sorted_list_4, True))

    unsorted_list = [8, 5, -10, 11, 0]
    print(sort_merge(unsorted_list))
    print(sort_merge(unsorted_list, True))


if __name__ == '__main__':
    main()