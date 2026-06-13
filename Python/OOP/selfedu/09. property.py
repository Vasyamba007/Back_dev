class Person:

    def __init__(self, name, old):
        self.__name = name
        self.__old = old

    def get_old(self):
        return self.__old
    
    def set_old(self, old):
        self.__old = old


p = Person('Сергей', 20)
p.set_old(35)
print(p.get_old())

# Проблема: надо прописывать геттеры и сеттеры для разных приватных атрибутов
# Решение: используем объект property

class Person_property:

    def __init__(self, name, old):
        self.__name = name
        self.__old = old

    def get_old(self):
        return self.__old
    
    def set_old(self, old):
        self.__old = old

    # при считывании a = p.old вызывается геттер get_old
    # при записи p.old = 35 вызывается сеттер set_old
    old = property(get_old, set_old)


p = Person_property('Сергей', 20)
p.old = 35
print(p.old, p.__dict__)

# Почему в локальном пространстве не создаётся новое свойство old,
# как в коде ниже?

p.old2 = 36
print(p.old, p.__dict__)

# Дело в приоритете. Если в классе задан атрибут property,
# то в первую очередь выбирается он, даже если в экземпляре
# есть локальное свойство с таким же именем

p.__dict__['old'] = 'old in object p'
p.old = 45
print(p.old, p.__dict__)


# сейчас у локального свойства old будет приоритет выше,
# чем у свойства класса
class Person_without_prop:

    def __init__(self, name, old):
        self.__name = name
        self.__old = old

    def get_old(self):
        return self.__old
    
    def set_old(self, old):
        self.__old = old

    old = 4

p = Person_without_prop('Сергей', 20)
print(p.old, p.__dict__)
p.__dict__['old'] = 'old in object p'
print(p.old, p.__dict__)

# У нас получилось некоторое дублирование: мы можем работать
# со свойтсвом old как через геттер и сеттер, так и через объект property
# Было бы лучше, если бы у нас был один интерфейс взаимодействия
# со свойством old.

# У объекта property есть декораторы x.setter(), x.getter(),
# x.deletr

class Person2:

    def __init__(self, name, old):
        self.__name = name
        self.__old = old

    @property
    def old(self):
        return self.__old
    
    @old.setter
    def old(self, old):
        self.__old = old

    @old.deleter
    def old(self):
        del self.__old


p = Person2('Сергей', 20)
p.old = 35
print(p.old, p.__dict__)
del p.old
print(p.__dict__)

# Таким образом создали объект property для работы с приватным
# свойством old