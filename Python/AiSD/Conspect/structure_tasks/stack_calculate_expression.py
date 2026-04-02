from collections import deque
from stack_shunting_yard import oper_push, shunting_yard
        
def calculate_expression(expression: str) -> float:
    answer_stack = deque()
    '''
    Вычислить значение выражения
    '''
    stack_postfix = list(shunting_yard(expression))
    for el in stack_postfix:
        if isinstance(el, (int, float)):
            answer_stack.append(el)
        else:
            b = answer_stack.pop()
            a = answer_stack.pop()
            answer_stack.append(eval(f'a {el} b'))
    # return answer_stack[0]
    return 



def main():
    print(calculate_expression('7 - (2 + 3) * 6 + (12 - 3) / 3')) # -20
    print(calculate_expression('7 - ((2 + 3) * 6 + (12 - 3) / 3)')) # -26
    print(calculate_expression('6 + 3 * (1 + 4 * 5) * 2')) # 132
    print(calculate_expression('1 + 2 ** 3 * 10')) # 81
    print(calculate_expression('- 2 + 6')) # 4



if __name__ == '__main__':
    main()