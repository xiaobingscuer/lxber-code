
import tkinter as tk

# tkinter,窗口视图
# entry & text


def insert_point():
    
    global enty,text

    var=enty.get()
    text.insert('insert',var)

   
def insert_end():
    
    global enty,text

    var=enty.get()
    text.insert('end',var)

def insert_position():
    
    global enty,text

    var=enty.get()
    text.insert(1.1,var) #第1行1列，行从1开始，列从0开始

if __name__=='__main__':

    window=tk.Tk()
    window.title('my window')
    window.geometry('300x200') #长宽

    enty=tk.Entry(window,show=None)
    #enty=tk.Entry(window,show='*') #密码形式
    enty=tk.Entry(window,show='1') #显示为特定字符
    enty.pack()

    text=tk.Text(window,height=3)
    text.pack()
    
    butn1=tk.Button(window,text='insert point',width=15,height=2,command=insert_point)
    butn2=tk.Button(window,text='insert end',width=15,height=2,command=insert_end)
    butn3=tk.Button(window,text='insert position',width=15,height=2,command=insert_position)
    butn1.pack()
    butn2.pack()
    butn3.pack()

    window.mainloop()
    
    
