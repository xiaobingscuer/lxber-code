

import time
import multiprocessing as mp
import threading as td

# 多线程的劣势，一个时间片只能处理一个线程任务
# multiprocessing,多进程，利用cpu的多核去处理数据
# 将每个任务平均分配给相应的核去处理，
# 每个核有单独的运算空间，和运算能力
# 从而避免多线程的劣势

# Process也不能返回结果，需用队列保持，多进程有自己queue
# Pool可以返回值，默认使用所有的核数，也可指定核数
# 如何看cpu/核/内存被使用和进程情况，资源管理器

def job(x):
    x*x


def multiproc():
    
    pool=mp.Pool(processes=2) #使用2核
    
    res=pool.map(job,range(10)) #平均分配给所有的核
    print(res)

    res=pool.apply_async(job, (2,)) #只能传递一个值，因此只会放入一个核，但是传入的值是可迭代的，因此要加一个逗号（，）
    print(res.get())
    
    multi_res=[pool.apply_async(job,(i,)) for i in range(10)] #为了使apply_async输出多个值，因此放入迭代器中
    print([res.get() for res in multi_res]) #同样取值也需要迭代式地取

    
def main():

    s_t=time.time()
    multiproc()
    s_t=time.time()-s_t
    print("multiproc: \n",s_t)
    

    
@main()
def now():
    print("hello,world")
    
if __name__=='__main()__':
    main()




    
    
