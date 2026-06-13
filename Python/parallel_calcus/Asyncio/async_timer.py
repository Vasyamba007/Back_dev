from itertools import cycle
from random import randint
import asyncio


async def delayed_greeting(name, delay):
    await asyncio.sleep(delay)
    print(f'Привет, {name}!')


async def main():
    n = 7
    names = cycle(('Гриша', 'Миша', 'Даша', 'Маша', 'Света'))

    tasks = [asyncio.create_task(delayed_greeting(next(names), randint(1, 5))) for _ in range(n)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())