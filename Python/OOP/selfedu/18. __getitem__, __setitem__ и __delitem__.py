# __getitem__(self, item) - получение значения по ключу item
# __setitem__(self, key, value) - запись значения value по ключу key
# __delitem__(self, key) - удаление элемена по ключу key


class Student:

    def __init__(self, name, marks):
        self.name = name
        self.marks = list(marks)

    # хотим обращаться к оценкам через синтаксис 's1[2]'
    def __getitem__(self, item):
        if 0 <= item < len(self.marks):
            return self.marks[item]
        else:
            raise IndexError('Неверный индекс')

    # хотим присваивать значения через синтаксис s1[2] = 4 
    def __setitem__(self, key, value):
        if not isinstance(key, int) or key < 0:
            raise TypeError('Индекс должен быть целым неотрицательным числом')

        if key >= len(self.marks):
            off = key + 1 - len(self.marks)
            self.marks.extend([None] * off)
        self.marks[key] = value

    def __delitem__(self, key):
        if not isinstance(key, int):
            raise TypeError('Индекс должен быть целым числом')

        del self.marks[key]


s1 = Student('Срегей', [5, 5, 3, 2, 5])
print(s1.marks[2])
print(s1[2])
# выведет 'Неверный индекс'
# print(s1[20])

s1[2] = 4
print(s1.marks)

# выведет Индекс должен быть целым неотрицательным числом
# s1[-2] = 4

s1[10] = 4
print(s1.marks)

del s1[2]
print(s1.marks)