from string import ascii_letters

# 
class Person:

    S_RUS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя-'
    S_RUS_UPPER = S_RUS.upper()

    def __init__(self, fio, old, ps, weight):
        self.verify_fio(fio)
        # проверки ниже не нужны, т.к. мы прописали их в сеттерах
        # self.verify_old(old)
        # self.verify_ps(ps)
        # self.verify_weight(weight)

        self.__fio = fio.split()
        self.old = old
        self.passport = ps
        self.weight = weight

    
    @classmethod
    def verify_fio(cls, fio):
        if type(fio) != str:
            raise TypeError('ФИО должно быть строкой')
        
        f = fio.split()

        if len(f) != 3:
            raise TypeError('Неверный формат ФИО')
        
        # ascii_letters - набор больших и маленьких латинских букв
        letters = ascii_letters + cls.S_RUS + cls.S_RUS_UPPER
        for s in f:
            if len(s) < 1:
                raise TypeError('В ФИО должен быть хотя бы один символ')
            if len(s.strip(letters)) != 0:
                raise TypeError('В ФИО можно использовать только буквенные символы и дефис')
            
    @classmethod
    def verify_old(cls, old):
        if type(old) != int or old > 120 or old < 14:
            raise TypeError('Возраст должен быть целым числом в диапазоне от 14 до 120 лет')
    
    @classmethod
    def verify_weight(cls, w):
        if type(w) != float or w < 20:
            raise TypeError('Вес должен быть вещественным числом от 20 и выыше')
    
    @classmethod
    def verify_ps(cls, ps):
        if type(ps) != str:
            raise TypeError('Паспорт должен быть строкой')
        
        s = ps.split()
        if len(s) != 2 or len(s[0]) != 4 or len(s[1]) != 6:
            raise TypeError('Неверный формат паспорта')
        
        for p in s:
            if not p.isdigit():
                raise TypeError('Серия и номер паспорта должны быть числами')
    
    @property
    def fio(self):
        return self.__fio
    
    @property
    def old(self):
        return self.__old
    
    @old.setter
    def old(self, old):
        self.verify_old(old)
        self.__old = old

    @property
    def weight(self):
        return self.__weight
    
    @weight.setter
    def weight(self, weight):
        self.verify_weight(weight)
        self.__weight = weight

    @property
    def passport(self):
        return self.__passport
    
    @passport.setter
    def passport(self, ps):
        self.verify_ps(ps)
        self.__passport = ps

    

p = Person('Титов Василий Андреевич', 29, '1234 345678', 70.0)
# выведет исключение
# p = Person('Титов2 Василий Андреевич', 29, '12 345678', 70)
print(p.fio)

# выведет исключение
# p.fio = 'Титов Алексей Васильевич'

p.old = 100
p.weight = 75.0
print(p.__dict__)

# p3 = Person('Ковальчук Артём Александрович', 29, '123 123456', 70.0)