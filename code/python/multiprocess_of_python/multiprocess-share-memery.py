

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

value=mp.Value('d',1) # 设置共享内存value,数据类型double,值为1
array=mp.Array('i',[1,2,3])

def main():
    
    
@main()
def now():
    print("hello,world")
    
if __name__=='__main()__':
    main()




    
    
