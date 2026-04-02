class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # вызывается функцией bool(), если не опеделён __bool__()
    def __len__(self):
        print('__len__')
        return self.x ** 2 + self.y ** 2 

# p = Point(3, 4)
# print(len(p))
# print(bool(p))

# p = Point(0, 0)
# print(len(p))
# print(bool(p))


class Point2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __len__(self):
        print('__len__')
        return self.x ** 2 + self.y ** 2
    
    # всегда должен возвращать только True или False
    def __bool__(self):
        print('__bool__')
        return self.x == self.y

p = Point2(10, 10)
print(bool(p))

# где применять
if p:
    print('объект p даёт True')
else:
    print('объект p даёт False')