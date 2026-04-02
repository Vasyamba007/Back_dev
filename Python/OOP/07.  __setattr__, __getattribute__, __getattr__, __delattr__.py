class Point:
    MAX_COORD = 100
    MIN_COORD = 0
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def set_coord(self, x, y):
        self.x = x
        self.y = y

    def set_bound(self, left):
        self.MIN_COORD = left

    @classmethod
    def set_bound_class(cls, left):
        cls.MIN_COORD = left
    
# Класс можно воспринимать как некоторое пространство имён, в котором записаны свойства и методы - атрибуты класса.
# Атрибуты класса - это MAX_COORD, MIN_COORD, __init__, set_coord
# Атрибуты класса не копируются в отдельные экземпляры и являются общими. Но из экземпляров мы можем
# обращаться к атрибутам, т.к. они (экземпляры) содержат ссылку на внешнее пространство имён - наш класс.
# И если в экземпляре не найден атрибут, то поиск переходит во внешнее пространство.

pt1 = Point(1, 2)
pt2 = Point(10, 20)
print(pt1.MAX_COORD)

# будет создан новый атрибут MIN_COORD внутри экземпляра, т.к. он изначально
# там отсутсвует
# pt1.set_bound(-100)
# print(pt1.__dict__)
# print(Point.__dict__)

# будет изменён атрибут клласса MIN_COORD
pt1.set_bound_class(-50)
print(pt1.__dict__)
print(Point.__dict__)


class Point_2(Point):

    # метод автоматически вызывается при считывании атрибута через экземпляр класса
    def __getattribute__(self, item):
        print('__getattribute__')
        return object.__getattribute__(self, item)

pt1 = Point_2(1, 2)

# теперь будет печататься строка __getattribute__
print(pt1.MAX_COORD)
print(pt1.x)


class Point_3(Point):

    def __getattribute__(self, item):
        if item == 'x':
            raise ValueError('Доступ к атрибуту "х" запрещён')
        else:
            return object.__getattribute__(self, item)
        
pt1 = Point_3(3, 2)

print(pt1.y)
# теперь будет вызываться исключение ValueError: Доступ к атрибуту "х" запрещён
# print(pt1.x)


class Point_4(Point):

    # метод автоматически вызывается при присваивании атрибуту значения
    def __setattr__(self, key, value):
        print('__setattr__')
        return object.__setattr__(self, key, value)
    
# выведет 2 раза __setattr__, __setattr__
pt4 = Point_4(10, 20)


class Point_5(Point):

    def __setattr__(self, key, value):
        if key == 'z':
            raise AttributeError('Недопустимое имя атрибута')
        else:
            # если прописать self.x = value, то будет бесконечный цикл
            # поэтому надо использовать конструкцию self.__dict__[key] = value
            return object.__setattr__(self, key, value)
    
pt5 = Point_5(10, 20)
# выведет исключение AttributeError: Недопустимое имя атрибута
# pt5.z = 0

pt5.v = 100
print(pt5.__dict__)


class Point_7(Point):
    
    # метод автоматически вызывается, когда идёт обращене к несуществующему
    # атрибуту через экземпляр класса
    def __getattr__(self, item):
        print('__getattr__' + item)

pt7 = Point_7(10, 20)
print(pt7.yy)
print(pt7.MAX_COORD)


class Point_8(Point):
    
    # иначе будет вызываться исключение
    def __getattr__(self, item):
        return False

pt8 = Point_8(1, 2)
print(pt8.yy)


class Point_9(Point):
    
    # автоматически вызывается, когда удаляется атрибут экземпляра класса
    def __delattr__(self, item):
        print('__delattr__' + item)
        object.__delattr__(self, item)

pt9 = Point_9(10, 20)
del pt9.x
print(pt9.__dict__)