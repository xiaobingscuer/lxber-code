

import threading
import time

# join,主线程（父线程）等待子线程完成任务，然后才执行主线程（父线程）之后的任务
# 如果每个线程都使用了join()方法，那么主线程（父线程）需要等到所有子线程都完成任务之后才开始自己的任务
#
# example:
#
#       main_thread
#           |
#           |    thread_1
#           |-------|       
#           |       |    thread_2
#           |       |--------|
#           |       |        |
#           |      -------------all done         
#  ---------------------------------- all done
#           |
#           |
#
#

def thread_first_job():
    print('T1 start\n')
    for i in range(10):
        time.sleep(0.1)
    print('T1 finish\n')

def thread_second_job():
    print('T2 start\n')
    print('T2 finish\n')

    
def main():
    thread_first=threading.Thread(target=thread_first_job, name='T1')
    thread_second=threading.Thread(target=thread_second_job, name='T2')

    thread_first.start()
    thread_second.start()
    
    #thread_first.join()
    thread_second.join()
    
    print("all done\n")
    
    #print(threading.active_count())
    #print(threading.enumerate())
    #print(threading.current_thread())
    print('\n')

@main()
def now():
    print("hello,world")
    
if __name__=='__main()__':
    main()
    
