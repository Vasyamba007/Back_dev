from collections import deque


def oper_push(now, prev, prior_dict) -> bool:
    '''
    Функция, которая опеделяет, надо ли оператор предыдущий оператор выталкивать в итоговый стэк
    :param now: текущий оператор
    :param prev: предыдущий оператор
    :param prior_dict: словарь с приоритетами
    '''
    # операция возведения в степень - право-ассоциативная, поэтому её обрабатываем отдельно
    if now == '**':
        if prior_dict[prev] > prior_dict[now]:
            return True
        return False        
    elif prior_dict[prev] >= prior_dict[now]:
        return True
    return False


def shunting_yard(expression: str) -> deque:
    '''
    Алгоритм сортировочной станции. Сложность О(N).
    Функция преобразовывает входное выражание в инфиксной форме в постфиксную.
    Между опрендами должен быть знак пробела.
    :param expression: выражение
    '''
    # словарь с возможными операторами и их приоритетами
    prior_dict = {
        '**': 100,
        '*': 10,
        '/': 10,
        '+': 1,
        '-': 1
        }
    # виды скобок
    br_dict = {
        ')': '(',
        ']': '[',
        '}': '{'    
    }
    # наш итоговый стэк
    stack_OPN = deque()
    # вспомогательный стэк операторов
    stack_operators = deque()
    # чтобы было проще парсить элементы заменим скобки на скобки с пробелом.
    # вдобавок учтём унарный минус добавлением 0, т.е. как бы преобразуем его в бинарный
    new_expression = ''
    for s in expression:
        if s in br_dict.keys() or s in br_dict.values():
            new_expression += f' {s} '
        elif s == '-':
            if new_expression == '':
                new_expression += f'0 {s} '
            elif new_expression[-2] == '( ':
                new_expression += f'0 {s} '
            else:
                new_expression += s
        else:
            new_expression += s
    # заполняем stack_OPN
    for el in new_expression.split():
        if el[0].isdigit():
            stack_OPN.append(float(el))
        elif el in prior_dict.keys():
            # выталкиваем все операторы с большим или равным приоритетом в ответ
            # останавливаемся, когда дошли до начала stack_operators, до открывающей скобки или оператора с меньшим приоритетом
            while stack_operators:
                if stack_operators[-1] in br_dict.values():
                    break
                elif oper_push(el, stack_operators[-1], prior_dict):
                    stack_OPN.append(stack_operators.pop())
                else:
                    break
            stack_operators.append(el)
        elif el in br_dict.values():
            stack_operators.append(el)
        else:
            # закрывающая скобка должна выталкивать все элементы в итоговый стэк, пока
            # не встретит открывающую скобку. Поэтому открывающая скобка 100 % должна быть. 
            while stack_operators[-1] not in br_dict.values():
                stack_OPN.append(stack_operators.pop())
            del stack_operators[-1]
    # оставшиеся операторы добавляем в итоговый стэк
    while stack_operators:
        stack_OPN.append(stack_operators.pop())
    return stack_OPN
        

def main():
    print(shunting_yard('7 - (2 + 3) * 6 + (12 - 3) / 3'))
    print(shunting_yard('7 - ((2 + 3) * 6 + (12 - 3) / 3)'))
    print(shunting_yard('6 + 3 * (1 + 4 * 5) * 2'))
    print(shunting_yard('1 + 2 ** 3 * 10'))
    print(shunting_yard('- 2 + 6'))



if __name__ == '__main__':
    main()