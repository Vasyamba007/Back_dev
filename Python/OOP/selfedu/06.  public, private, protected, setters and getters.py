from accessify import private, protected

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
        self._protected_x = x
        self._protected_y = y

        self.__private_x = x
        self.__private_y = y
    

    @private
    @classmethod
    def check_value_accessify(cls, coord):
        return type(coord) in (int, float)

    @classmethod
    def __check_value(cls, coord):
        return type(coord) in (int, float)

    # сеттер - метод, изменяющий защищённые атрибуты
    def set_coord(self, x, y):
        if self.__check_value(x) and self.__check_value(y):
            self.__private_x = x
            self.__private_y = y
        else:
            raise ValueError('координаты должны быть числами')

    # геттер - метод, возвращающий защищённые атрибуты
    def get_coord(self):
        return self.__private_x, self.__private_y

    # сеттеры и геттеры иногда называют интерфейсными методами

    
pt = Point(1, 2)
print(pt.x, pt.y)
pt.x = 200
pt.y = 'coord_y'
print(pt.x, pt.y)

# Инкапсуляция - механизм, ограничивающий доступ к атрибутам из вне.
# attribute - режим доступа public
# _attribute - режим доступа protected - служит для обращения внутри класса и во всех его дочерних классах
# такой режим доступа просто даёт сигнал программисту не обращаться к атрибуту вне класса.
# __attribute - режим доступа private - служит для обращения только внутри класса

print(pt._protected_x, pt._protected_y)

# выведет исключение AttributeError: 'Point' object has no attribute '__private_x'
# print(pt.__private_x, pt.__private_y) 

# внутри класса к приватным атрибутам можно обращаться через сеттеры и геттеры
pt.set_coord(5, 6)
print(pt.get_coord())

# выведет исключение ValueError: координаты должны быть числами
# pt.set_coord('123', 6)
# print(pt.get_coord())

# посмотрим, какие атрибуты есть в экземпляре класса pt
print(dir(pt))

# всё равно можем получить доступ к приватному атрибуту, но так делать КРАЙНЕ не рекомендуется
print(pt._Point__private_x)

# модуль accessify запрещает получать доступ к private атрибуту через _Point__
# выведет исключение accessify.errors.InaccessibleDueToItsProtectionLevelException: Point.check_value_accessify() is inaccessible due to its protection level
print(pt.check_value_accessify(5))

# но как правило __atributte достаточно