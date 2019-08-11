

import time
import multiprocessing as mp
import threading as td

# 多线程的劣势，一个时间片只能处理一个线程任务
# multiprocessing,多进程，利用cpu的多核去处理数据
# 将每个任务平均分配给相应的核去处理，
# 每个核有单独的运算空间，和运算能力
# 从而避免多线程的劣势

# 多进程也不能返回结果，需用队列保持，多进程有自己queue

def job(q):
    res=0
    for i in range(1000):
        res+=i+i**2+i**3
    q.put(res)

def normal():
    res=0
    for _ in range(2):
        for i in range(1000):
             res+=i+i**2+i**3
    print(res)

def multiproc():
    q=mp.Queue()
    
    p1=mp.Process(target=job, args=(q,))
    p2=mp.Process(target=job, args=(q,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    res1=q.get()
    res2=q.get()

    print(res1+res2)

def multithread():
    q=mp.Queue()
    
    t1=td.Thread(target=job, args=(q,))
    t2=td.Thread(target=job, args=(q,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    res1=q.get()
    res2=q.get()

    print(res1+res2)
    
def main():

    s_t=time.time()
    normal()
    s_t=time.time()-s_t
    print("normal: \n",s_t)

    s_t=time.time()
    multithread()
    s_t=time.time()-s_t
    print("multithread: \n",s_t)

    s_t=time.time()
    multiproc()
    s_t=time.time()-s_t
    print("multiproc: \n",s_t)
    

    
@main()
def now():
    print("hello,world")
    
if __name__=='__main()__':
    main()




    
    
