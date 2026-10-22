import asyncio
import time
from time import perf_counter

def make_drink(name):
    print(f'{name} 만들기 시작 ')
    time.sleep(2)
    print(f'{name} 완성')
    return name

def main():
    make_drink('커피')
    make_drink('차')

if __name__=='__main__':
    main()
