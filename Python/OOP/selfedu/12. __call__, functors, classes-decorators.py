class Counter:

    def __init__(self):
        self.__counter = 0

    def __call__(self, step=1, *args, **kwargs):
        print('__call__')
        self.__counter += step
        return self.__counter

# когда прописываем '()', то автоматически вызывается метод __call__
# __call__(self, *args, **kwargs):
#    obj = self.__new__(self, *args, **kwargs)
#    self.__init__(obj, *args, **kwargs)
#    return obj
# благодаря __call__ мы можем вызывать объект как функцию
# классы, которые себя так ведут называются функторами
c = Counter()
c2 = Counter()
c()
c(2)
res = c(10)
res2 = c2(-5)
print(res, res2)

# вместо замыкания функций можно реализовывать класс с магическим методом call

class StripChars:

    def __init__(self, chars):
        self.__counter = 0
        self.__chars = chars

    def __call__(self, *args, **kwargs):
        if not isinstance(args[0], str):
            raise TypeError('Аргумент должен быть строкой')

        return args[0].strip(self.__chars)


s1 = StripChars('?:!.; ')
s2 = StripChars(' ')
res = s1(' Hello World! ')
res2 = s2(' Hello World! ')
print(res, res2, sep='\n')

# реализация декоратора с помощью классов
import math

class Derivate:

    def __init__(self, func):
        self.__fn = func

    def __call__(self, x, dx=0.0001, *args, **kwargs):
        return (self.__fn(x + dx) - self.__fn(x)) / dx

    
@Derivate
def df_sin(x):
    return math.sin(x)

# df_sin = Derivate(df_sin)
print(df_sin(math.pi / 3))