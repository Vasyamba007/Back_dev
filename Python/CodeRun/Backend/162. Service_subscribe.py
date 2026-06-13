

class Subscriber:
    
    def __init__(self, description: str):
        a, b, *attrs = description.split()

        self.triggers = {attr: None for attr in attrs[:int(a)]}
        self.shipments = {attr: None for attr in attrs[int(a):]}

class Request



def main():
    n, m = map(int, input().split())

    subscribers = [Subscriber(input()) for _ in range(n)]

    for i in range(m):
        pass



if __name__ == '__main__':
    main()