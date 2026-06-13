class ThreadData:
    
    # общие локальные свойства экземпляров
    __shared_attrs = {
        'name': 'thread_1',
        'data': {},
        'id': 1
    }

    # при создании нового экземпляра его коллекция __dict__ ссылается
    # на __shared_attrs. Таким образом локальное пространство имён для разных экземпляров одинаковое.
    def __init__(self):
        self.__dict__ = self.__shared_attrs


th1 = ThreadData()
th2 = ThreadData()
print(th1.__dict__)
th2.id = 2
print(th1.__dict__)

th1.attr_new = 'new_attr'
print(th2.__dict__)