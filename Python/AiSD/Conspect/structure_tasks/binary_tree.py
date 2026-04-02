class Node:
    '''
    Класс, моделирующий вершину бинарного дерева. В свойствах self.left и self.right 
    хранятся ссылки на левого и правого потомков.
    '''
    def __init__(self, data):
        self.data = data
        self.left = self.right = None


class Tree:
    '''
    Класс, моделирующий бинарное дерево.
    '''
    def __init__(self, value=None):
        self.root = Node(value)


    def __find(self, parent: Node, current: Node, value) -> tuple:
        '''
        Метод возвращает узел current со значением value, его родителя и флаг, который говорит, что найдено совпадение value и current.data.
        Если такого узла нет, то возвращаются два предка parent и current и флаг, который говорит, что не найдено совпадение value и current.data
        '''
        if value == current.data:
            return parent, current, True
        elif value < current.data and current.left:
            return self.__find(current, current.left, value)
        elif value > current.data and current.right:
            return self.__find(current, current.right, value)
        return parent, current, False


    def append(self, value):
        if self.root.data is None:
            self.root.data = value
        else:
            parent, current, flag = self.__find(None, self.root, value)
            if flag:
                print(f'Значение {value} уже есть в дереве')
                return
            elif value < current.data:
                current.left = Node(value)
            else:
                current.right = Node(value)
        print(f'Значение {value} добавлено в дерево')
        

    def __del_list(self, parent: Node, list: Node) -> None:
        '''
        Удаление листа
        
        :param self: Описание
        :param parent: Описание
        :param list: Описание
        '''
        if parent is None:
            self.root = None
        elif parent.left == list:
            parent.left = None
        else:
            parent.right = None


    def __find_min(self, parent_min_node: Node, min_node: Node) -> tuple:
        if min_node.left:
            return self.__find_min(min_node, min_node.left)
        else:
            return parent_min_node, min_node


    def __del_node(self, parent: Node, node: Node) -> None:
        '''
        Удаление узла с одним потомком
        
        :param parent: родитель удаляемого узла
        :param node: удаляемый узел
        '''
        if parent is None:
            if node.left:
                self.root = node.left
            else:
                self.root = node.right
        elif parent.left == node:
            if node.left:
                parent.left = node.left
            else:
                parent.left = node.right
        else:
            if node.left:
                parent.right = node.left
            else:
                parent.right = node.right
        

    def del_val(self, value) -> None:
        '''
        Удаление значений из дерева
        
        :param self: дерево
        :param value: удаляемое значение
        '''
        parent, current, flag = self.__find(None, self.root, value)
        if not flag:
            print(f'Значения {value} в дереве нет')
            return
        elif current.left == current.right == None:
            self.__del_list(parent, current)
        elif current.left and current.right:
            # ищем минимальное значение в правой ветви
            parent_min_node, min_node = self.__find_min(current, current.right)
            # перезаписываем найденный минимум вместо удаляемого значения
            current.data = min_node.data
            # удаляем узел с минимумом, это либо лист, либо узел с правым потомком
            if min_node.right:
                self.__del_node(parent_min_node, min_node)
            else:
                self.__del_list(parent_min_node, min_node)
        else:
            self.__del_node(parent, current)
        print(f'Значение {value} удалено из дерева')
        

    def show_wide(self):
        '''
        Показать вершины дерева методом обхода в ширину
        '''
        nodes = [self.root]
        while nodes:
            if not any(nodes):
                break
            nodes_new_level = []
            for el in nodes:
                if el is None:
                    print(None, end=' ')
                else:
                    print(el.data, end=' ')
                    nodes_new_level += [el.left, el.right]
            nodes = nodes_new_level
            print()


    def show_deep(self, node: Node, reverse: bool=False):
        '''
        Показать вершины дерева методом обхода в глубину.
        При обходе осуществляется соритровка, порядок сортировки определяется парамтером reverse.
        '''
        if node is None:
            return None
        if not reverse:
            self.show_deep(node.left, reverse)
            print(node.data)
            self.show_deep(node.right, reverse)
        else:
            self.show_deep(node.right, reverse)
            print(node.data)
            self.show_deep(node.left, reverse)
            
        
def main():
    numbers =  [10, 5, 9, 16, 1, 20, 7, 12, 4, 8, 6]
    t = Tree()
    for v in numbers:
        t.append(v)
    t.show_wide()
    t.show_deep(t.root)
    t.show_deep(t.root, reverse=True)
    t.del_val(100)
    t.del_val(20)
    t.show_wide()
    t.del_val(16)
    t.show_wide()
    t.append(6.5)
    t.show_wide()
    t.del_val(5)
    t.show_wide()
    numbers =  [50, 200, 150, 300]
    t = Tree(100)
    for v in numbers:
        t.append(v)
    t.show_wide()
    t.del_val(100)
    t.show_wide()

    
if __name__ == '__main__':
    main()