


import threading
import time
from queue import Queue
import copy

# lock,对共享内存块的一系列操作加锁，用来协调不同线程对共享内存的操作
# 本例中job1与job2对内存A的操作不相互影响，让main()函数变为线程安全的函数


A=0
lock=threading.Lock()

def job1():
    global A, lock
    lock.acquire()
    for i in range(10):
        A += 1
        print("job1 %d \n" % A)
    lock.release()

def job2():
    global A, lock
    lock.acquire()
    for i in range(10):
        A +=10
        print("job2 %d \n" % A)
    lock.release()


def main():
    
    t1=threading.Thread(target=job1)
    t2=threading.Thread(target=job2)

    t1.start()
    t2.start()
    

    t1.join()
    t2.join()

    
@main()
def now():
    print("hello,world")
    
if __name__=='__main()__':
    main()
    
