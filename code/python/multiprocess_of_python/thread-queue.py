

import threading
import time
from queue import Queue

# 多线程里的操作无法返回结果的，需借助队列queue来保存计算结果

def job(l,q):
    for i in range(len(l)):
        l[i]=l[i]**2
    q.put(l)

def multithreading():
    q=Queue()
    threads=[]
    data=[[1,2,3],[3,4,5],[4,4,4],[5,5,5]]
    
    for i in range(4):
        t=threading.Thread(target=job, args=(data[i],q))
        t.start()
        threads.append(t)
        
    for thread in threads:
        thread.join()
        
    results=[]
    for _ in range(4):
        results.append(q.get())
    return results
    
def main():
    print(multithreading())

@main()
def now():
    print("hello,world")
    
if __name__=='__main()__':
    main()
    
