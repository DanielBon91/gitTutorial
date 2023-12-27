from timeit import default_timer as timer
import math
import time

def hello_world():
    print('Hello, world!')
hello = hello_world
hello()

def hello_world_2():
    def intern():
        print('Hello, world 2!')
    return intern
hello2=hello_world_2()
hello2()

def say_something(func):
    func()
say_something(hello_world)
##################################################
def log_dec(func):
    def wrap():
        print(f'calling - {func}')
        func()
        print(f'Func - {func}')
    return wrap

wrapper = log_dec(hello_world)
wrapper()

@log_dec
def good_by():
    print('Thüüüüüs!')

good_by()
##################################################
def diff_time(func):
    def inner(*args, **kwargs):

        start = timer()

        func(*args, **kwargs)

        end = timer()

        print(f'Function {func.__name__} take {end-start}')

    return inner

@diff_time
def fact(num):
    time.sleep(2)
    print(math.factorial(num))

fact(90)
##################################################
help(diff_time)


