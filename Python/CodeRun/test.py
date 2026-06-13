


a, b = 0, 2
attrs = ('жопа', 'хер')

attrs_a = {attr: None for attr in attrs[:a]}
attrs_b = {attr: None for attr in attrs[a:]}

print(attrs_a, attrs_b, sep='\n')