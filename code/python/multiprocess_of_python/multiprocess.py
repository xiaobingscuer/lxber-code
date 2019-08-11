

import time
import multiprocessing as mp

# 多线程的劣势，一个时间片只能处理一个线程任务
# multiprocessing,多进程，利用cpu的多核去处理数据
# 将每个任务平均分配给相应的核去处理，
# 每个核有单独的运算空间，和运算能力
# 从而避免多线程的劣势
# 

def job(a,b):
    print("job a, b")


def main():
    
    p1=mp.Process(target=job, args=(1,2))

    p1.start()

    p1.join()
    

    
#@main()
#def now():
#    print("hello,world")
    
if __name__=='__main()__':
    main()
    
