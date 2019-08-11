

import threading
import time

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
    
