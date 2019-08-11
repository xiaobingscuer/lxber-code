

import time
import multiprocessing as mp
import threading as td

# 多线程的劣势，一个时间片只能处理一个线程任务
# multiprocessing,多进程，利用cpu的多核去处理数据
# 将每个任务平均分配给相应的核去处理，
# 每个核有单独的运算空间，和运算能力
# 从而避免多线程的劣势

# Process不能返回结果，需用队列保持，多进程有自己queue
# Pool可以返回值，默认使用所有的核数，也可指定核数
# 如何看核被使用情况

# 共享内存,用作不同cpu/核之前的交流媒介

# lock，锁，协调不同进程对共享内存的有序使用,避免无序抢夺共享内存

def job(v,num,lock):
    lock.acquire()
    for _ in range(10):
        time.sleep(0.1)
        v.value+=num
        print(v.value)
    lock.release()

def main():
    lock=mp.Lock()
    v=mp.Value('i',0)
    
    p1=mp.Process(target=job,args=(v,1,lock))
    p2=mp.Process(target=job,args=(v,3,lock))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
    

@main()
def now():
    print("hello,world")
    
if __name__=='__main()__':
    main()




    
    
