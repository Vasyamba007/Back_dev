class Vector:
    MIN_COORD = 0
    MAX_COORD = 100

    
    @classmethod
    def validate(cls, arg):
        return cls.MIN_COORD <= arg <= cls.MAX_COORD

    def __init__(self, x, y):
        self.x = self.y = 0
        if self.validate(x) and self.validate(y):
            self.x = x
            self.y = y
        
        print(self.norm2(self.x, self.y))

    def get_coord(self):
        return self.x, self.y
    

    @staticmethod
    def norm2(x, y):
        return x * x + y * y

    
v = Vector(1, 2)

res = v.get_coord()
print(res)

# должны передать в качестве аргумента ссылку на экземпляр класса
res = Vector.get_coord(v)
print(res)

# метод класса не требует ссылку на экземпляр класса
print(Vector.validate(5))

v = Vector(1, 200)

res = v.get_coord()
print(res)

# внутри класса лучше использовать только ссылки на экземпляр (self) или класс (cls),
# а не имя класса (Vector).

# статический метод не имеет доступа к атрибутам класса и экземплярам и служит
# для выполнения вспомогательных функций, связанных с этим классом
print(Vector.norm2(5, 6))

# ИТОГ
# 1) Обычные методы, вызываемые из экземпляров, могут работать как с атрибутами экземпляра,
# так и с атрибутами класса через self
# 2) Если предполагается, что метод будет работать только с атрибутами класса, то используют
# декоратор @classmethod и ссылку на класс cls
# 3) Если необходимо определить сервисную функцию, которая не будет обращаться ни к атрибутам
# экземпляров, ни к атрибутам класса, а будет работать только с переданными аргументами, то
# используют декоратор @staticmethod

