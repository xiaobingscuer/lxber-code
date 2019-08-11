

import threading
import time
from queue import Queue
import copy

# 多线程有时并不能提升效率
# 多线程是由GIL(Global Interpreter Lock,全局解释器锁)控制，每个时间片只能运行一个线程
# 多线程适用于处理多个相关性小的事情
# 如果对规模较大的数据进行分块处理，可能需要多进程

#                   I/O         I/O     I/O        I/O
# |------------------|-----------|-------|----------|------|
# thread 1: run ---->|           |       |run ----->|      |
# thread 2:          |run ------>|       |          |      |
# thread 3:          |           |run -->|          |run ->|
#                    |           |       |          |      |
#                   / \         / \     /  \       / \
#              释放锁  加锁 释放 加锁 释放 加锁 释放 加锁
#           release  acquire 
#                   GIL         GIL     GIL        GIL
 
def normal(l):
    total = sum(l)
    print(total)    
    return total
    
def job(l,q):
    total=sum(l)
    q.put(total)

def multithreading(l):
    q=Queue()
    threads=[]
    
    for i in range(4):
        t=threading.Thread(target=job, args=(l,q))
        t.start()
        threads.append(t)
        
    for thread in threads:
        thread.join()
        
    total=0
    for _ in range(4):
        total+=q.get()
    print(total)
    
    return total
    
def main():
    l=list(range(1000000))
    s_t=time.time()
    normal(l*4)
    s_t=time.time()-s_t
    print("normal: ",s_t)

    s_t=time.time()
    multithreading(l)
    s_t=time.time()-s_t
    print("mulithreading: ",s_t)

@main()
def now():
    print("hello,world")
    
if __name__=='__main()__':
    main()
    
