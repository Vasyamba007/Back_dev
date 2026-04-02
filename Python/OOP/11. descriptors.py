class Point3D:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def verify_coord(cls, coord):
        if type(coord) != int:
            raise TypeError('Координата должна быть целым числом')
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, coord):
        self.verify_coord(coord)
        self._x = coord

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, coord):
        self.verify_coord(coord)
        self._y = coord

    @property
    def z(self):
        return self._z
    
    @z.setter
    def z(self, coord):
        self.verify_coord(coord)
        self._z = coord

p = Point3D(1, 2, 3)
print(p.__dict__)

# Недостаток - происходит дублирование функций для каждой координаты
# Решение - использовать дескрипторы

# Дескриптор неданных (non-data descriptor) - класс с магическим методом __get__ 
# Дескриптор неданных имеет тот же приоритет, что и обычные атрибуты класса
# Дескриптор данных (data descriptor) - класс с магическим методом __get__, __set__ и/или __del__  
# Дескриптор данных имеет приоритет выше, чем локальные атрибуты экземпляра класса

# дескриптор неданных
class ReadIntX:

    def __set_name__(self, owner, name):
        self.name = '_x'

    def __get__(self, instance, owner):
        return getattr(instance, self.name)
    
# дескриптор данных
class Integer:

    @classmethod
    def verify_coord(cls, coord):
        if type(coord) != int:
            raise TypeError('Координата должна быть целым числом')
 
    # self - ссылка на экземпляр класса Integer
    # owner - ссылка на класс Point3D_descriptor
    # name - имя дескриптора (x или y или z)
    def __set_name__(self, owner, name):
        # создаём локальное свойство self.name в экземпляре класса Integer
        self.name = '_' + name
    
    # self - ссылка на экземпляр класса Integer
    # instance - ccылка на экземпляр класса Point3D_descriptor,
    # из которого был вызван дескриптор
    # owner - ссылка на класс Point3D_descriptor
    def __get__(self, instance, owner):
        # return instance.__dict__[self.name]
        return getattr(instance, self.name)

    # self - ссылка на экземпляр класса Integer
    # instance - ccылка на экземпляр класса Point3D_descriptor,
    # из которого был вызван дескриптор
    # value - значение 1, 2, 3
    def __set__(self, instance, value):
        self.verify_coord(value)
        print(f'__set__:{self.name} = {value}')
        # instance.__dict__[self.name] = value
        setattr(instance, self.name, value)
    
class Point3D_descriptor:

    # x, y, z - дескрипторы в классе Point3D_descriptor
    # после создания экземпляра класса Integer автоматически вызывается метод __set_name__
    x = Integer()
    y = Integer()
    z = Integer()
    xr = ReadIntX()

    def __init__(self, x, y, z):
        # self.x(y , z) - обращение к дескрипторам x (y, z)
        # в момент присваивания срабатывает __set__
        self.x = x
        self.y = y
        self.z = z

   
pt = Point3D_descriptor(1, 2, 3)
print(pt.__dict__)
print(pt.x)
print(pt._x)

# добавил дескриптор неданных
print(pt.xr, pt.__dict__)

# Т.к. дескриптор неданных имеет тот же приоритет, что и обычные атрибуты класса
# то при операции присваивания pt.xr = 5 мы смотрим на пространство имён
# экземпляра pt, не находим там свойства xr и создаём его.
pt.xr = 5
print(pt.xr, pt.__dict__)


# превращаем дескриптор неданных в дескриптор данных

# дескриптор данных
class ReadIntX_2:

    def __set_name__(self, owner, name):
        self.name = '_x'

    def __get__(self, instance, owner):
        return getattr(instance, self.name)
    
    def __set__(self, instance, value):
        setattr(instance, self.name, value)


class Integer_2:

    @classmethod
    def verify_coord(cls, coord):
        if type(coord) != int:
            raise TypeError('Координата должна быть целым числом')

    def __set_name__(self, owner, name):
        self.name = '_' + name
    
    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        self.verify_coord(value)
        setattr(instance, self.name, value)
    

class Point3D_descriptor_2:

    x = Integer_2()
    y = Integer_2()
    z = Integer_2()
    xr = ReadIntX_2()

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

p = Point3D_descriptor_2(1, 2, 3)
p.__dict__['xr'] = 5
print(p.xr, p.__dict__)

# теперь при обращении к p.xr взято не локальное свойство,
# а дескриптор данных
