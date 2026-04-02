# если a == b, то hash(a) == hash(b)
# если hash(a) == hash(b), то это не значит, что a == b
# если hash(a) != hash(b), то a != b

# (хэш ключа, ключ) -- по хэшу идёт поиск ключа в словаре

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


p1 = Point(1, 2)
p2 = Point(1, 2)

print(p1 == p2)

# получим ошибку unhashable type
# если переопределили метод __eq__, то hash() перестаёт работать
# print(hash(p1), hash(p2), sep='\n')


class Point2:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))


p1 = Point2(1, 2)
p2 = Point2(1, 2)

print(hash(p1), hash(p2), sep='\n')

# чего мы добились?

d = {}
d[p1] = 1
d[p2] = 2
print(d)

# теперь хэши p1 и p2 равны