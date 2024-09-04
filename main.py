from io import TextIOWrapper
from socket import create_connection
from threading import Thread, Lock
from os import system
from datetime import datetime
from platform import platform
from time import sleep

lock = Lock()
now : datetime = datetime.now()
TheTime : str = f'{now.month}-{now.day}---{now.hour}-{now.minute}'

with open('proxies.txt', 'r') as TheFile:
    proxies : list = TheFile.read().splitlines()

system(f'mkdir {TheTime}')
WorkAdd : TextIOWrapper = open(f'{TheTime}/work.txt', 'a')
BadAdd : TextIOWrapper = open(f'{TheTime}/bad.txt', 'a')

if platform().__contains__('Windows'):
    clear : int = lambda: system('cls')
else:
    clear : int = lambda: system('clear')

clear()
print(f"- !all proxies results in '{TheTime}' folder")
print(f'- proxies -> {len(proxies)}')
time_out = int(input(f'- timeout -> '))

class CounterClass:
    def __init__(self) -> None:
        self.work : int = 0
        self.bad : int = 0

counter = CounterClass()

def counter_function():
    clear()
    while counter.work + counter.bad != len(proxies):
        print(f'\rwork = {counter.work} - bad = {counter.bad}', end=' ')
        sleep(0.1)

def check(proxy:str) -> None:
    try:
        create_connection((proxy.split(':')[0], proxy.split(':')[1]), time_out)
        lock.acquire()
        counter.work += 1
        WorkAdd.write(f'{proxy}\n')
        WorkAdd.flush()
    except:
        lock.acquire()
        counter.bad += 1
        BadAdd.write(f'{proxy}\n')
        BadAdd.flush()
        
    lock.release()

def ExecuteCode() -> None:
    LoopThreads = 0
    for proxy in proxies:
        Thread(target=check, args=(proxy,)).start()
        LoopThreads += 1
        if LoopThreads >= 200:
            sleep(5)
            LoopThreads = 0

Thread(target=counter_function).start()
Thread(target=ExecuteCode).start()