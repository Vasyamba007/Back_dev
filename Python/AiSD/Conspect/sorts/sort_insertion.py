def sort_insertion(arr: list, reverse: bool=False) -> None:
    '''
    Сортирует переданный список arr методом вставки в порядке возрастания (reverse=False)
    или в порядке убывания (reverse=True).\n
    Лучший случай - при сортировке по возрастанию (убыванию) массив уже отсортирован по возрастанию (убыванию), 
    количество сравнений = n - 1, количество обменов = 0. Итоговая сложность: T(n - 1 + 0) -> |переходим к O-большое| 
    -> O(n).\n
    Худший случай - при сортировке по возрастанию (убыванию) массив отсортирован по убыванию (возрастанию), 
    количество сравнений = n(n - 1) / 2, количество обменов =  n(n - 1) / 2. Итоговая сложность: 
    T(n(n-1)/2 + n(n-1)/2) = T(n^2 - n) ~ |на большом количестве n младшие степени отбрасываем| ~ T(n^2) -> 
    -> |переходим к O-большое| -> O(n^2)\n
    Сложность по времени: O(n^2). В лучшем и худшем случаях асимптотическая сложность разная\n 
    Сложность по памяти: O(1). Дополнительная память требуется только для хранения индексов.
    Алгоритм хорошо себя показывает в полностью или частично отсортированном массиве, а также когда надо 
    доотсортировать вновь добавленную часть массива.
    '''
    n = len(arr)
    for i in range(1, n):
        for j in range(i, 0, -1):
            if not reverse and arr[j] < arr[j - 1]:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
            elif reverse and arr[j] > arr[j - 1]:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
            else:
                break


def sort_insertion_advanced(arr: list, reverse: bool=False) -> None:
    '''
    Сортирует переданный список arr методом вставки в порядке возрастания (reverse=False)
    или в порядке убывания (reverse=True). Преимущество перед обычной версией и sort_bubble в 
    том, что у нас операция обмена заменяется на операцию присваивания (обмен - это пара присваиваний). 
    Текущий элемент now вставляется в нужное место только один раз, после 2-го цикла. Благодаря этому 
    сокращается число операций присваивания, которая в современном компьютере достаточно медленная по сравнению
    с чтением данных.
    Сортировка устойчивая.
    '''
    n = len(arr)
    for i in range(1, n):
        now = arr[i]
        new_place = 0
        for j in range(i, 0, -1):
            if not reverse and now < arr[j - 1]:
                arr[j] = arr[j - 1]
            elif reverse and now > arr[j - 1]:
                arr[j] = arr[j - 1]
            else:
                new_place = j
                break
        arr[new_place] = now
    

def main():
    unsorted_list = [8, 5, -10, 11, 0]
    sort_insertion(unsorted_list)
    print(unsorted_list)

    unsorted_list = [8, 5, -10, 11, 0]
    sort_insertion(unsorted_list, True)
    print(unsorted_list)

    unsorted_list = [8, 5, -10, 11, 0]
    sort_insertion_advanced(unsorted_list)
    print(unsorted_list)

    unsorted_list = [8, 5, -10, 11, 0]
    sort_insertion_advanced(unsorted_list, True)
    print(unsorted_list)




if __name__ == '__main__':
    main()


