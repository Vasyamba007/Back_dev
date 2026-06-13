from sys import stdin
from string import ascii_letters
import re


class Pattern:

    PATTERN = re.compile(f'^(.+) - ([{ascii_letters}]+) (\\w+)$')  
    COUNTRY_CODE_PATTERN = r'^\+([1-9]\d{0,2})'
    OPERATOR_CODE_PATTERN = r'\((\d{2,4})\)'
    PERSONAL_NUMBER_PATTERN = r'([0-9X]{5,9})$'
    NUMBER_PATTERN = re.compile(' '.join([COUNTRY_CODE_PATTERN, OPERATOR_CODE_PATTERN, PERSONAL_NUMBER_PATTERN]))
    CLEAN_PATTERN = re.compile(r'[ -]')

    def __init__(self, pattern: str):
        
        number, country, operator = self.PATTERN.match(pattern.strip()).groups() 
        country_code, operator_code, uniq_num = self.NUMBER_PATTERN.match(number.strip()).groups()

        self.country = country
        self.operator = operator
        self.country_code = country_code
        self.operator_code = operator_code
        self.uniq_num = uniq_num
        self.check_pattern = self.__get_check_pattern()

    def __get_check_pattern(self):
        country_code_pattern = f'^\\+?({self.country_code})'
        operator_code_pattern = f'\\(?({self.operator_code})\\)?'
        uniq_num_pattern = f'({self.uniq_num.replace('X', '\\d')})$'
        return re.compile(country_code_pattern + operator_code_pattern + uniq_num_pattern) 
    
    def check_number(self, number) -> dict| None:
        unformat_number = self.CLEAN_PATTERN.sub('', number.unformat_number)
        match_obj = self.check_pattern.match(unformat_number)

        if match_obj:
            uniq_num = match_obj.groups()[-1]
            return {'country_code': self.country_code,
                    'operator_code': self.operator_code,
                    'uniq_num':  uniq_num,
                    'country': self.country, 
                    'operator': self.operator} 
        else:
            return match_obj

    def get_number_pattern(self):
        return f'+{self.country_code} ({self.operator_code}) {self.uniq_num}'
    
    def get_pattern(self):
        return f'{self.get_number_pattern()} - {self.country} {self.operator}'
    
    def __repr__(self):
        return self.get_pattern()


class Number(Pattern):
    
    # подругому пока не додумался, как получить 
    # все свойства экземпляров родительского класса
    attr_names = {name: None for name in Pattern.__dict__['__static_attributes__']}

    def __init__(self, number: str):
        self.unformat_number = number.strip()
        self.__dict__.update(**self.attr_names)

        del self.check_pattern

    def __str__(self):
        if not all((self.country_code, self.operator_code, self.uniq_num)):
            return self.unformat_number
        elif not all((self.country, self.operator)):
            return self.get_number_pattern()
        else:
            return self.get_pattern()

    def __repr__(self):
       self.__str__() 
        
    def format_number(self, **kwargs):
        for attr_name in kwargs:
            setattr(self, attr_name, kwargs[attr_name])
    

def main():
    numbers = [Number(stdin.readline()) for _ in range(int(input()))]
    patterns = [Pattern(stdin.readline()) for _ in range(int(input()))]

    for number in numbers:
        for pattern in patterns:
            if data := pattern.check_number(number):
                number.format_number(**data)
                print(number)
                break
    

if __name__ == '__main__':
    main() 