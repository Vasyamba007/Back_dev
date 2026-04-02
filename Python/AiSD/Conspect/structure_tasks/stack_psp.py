from collections import deque


def psp(expression: str) -> bool:
    '''
    Функция проверяет, правильно ли расставлены скобки в выражении.
    Если правильно - возвращает True, если нет - False. Решаем задачу с помощью стэка.
    '''
    br_dict = {
        ')': '(',
        ']': '[',
        '}': '{'    
    }
    stack = deque()
    for s in expression:
        if s in br_dict.values():
            stack.append(s)
        elif s in br_dict.keys():
            if not stack:
                return f'Есть закрывающая скобка {s}, но нет открывающей {br_dict[s]}'
            last_br = stack.pop()
            if last_br != br_dict[s]:
                return f'Закрывающая скобка {s} не соответствует открывающей {last_br}'
    if not stack:
        return 'ОК'
    else:
        return f'Незакрытые открывающие скобки: {' '.join(stack)}'


def main():
    print(psp('3 * (1 + 2)'))
    print(psp('3 * (1 + 2'))
    print(psp('3 * 1 + 2)'))
    print(psp('3 * (1 + 2) / {3 * 2}'))
    print(psp('3 * (1 + 2) / 3 * 2}'))
    print(psp('3 * (1 + 2) / {3 * 2'))
    print(psp('3 * (1 + 2 / 3 * 2}'))
    print(psp('3 * (1 + 2 / {3 * 2'))
    print(psp('3 * (4 * [2 + 10])'))
    print(psp('3 * (4 * 2 + 10])'))
    print(psp('3 * (4 * [2 + 10)'))


if __name__ == '__main__':
    main()