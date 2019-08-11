
import tkinter as tk

# tkinter,窗口视图
# list box,列表选择


def print_selection():
    
    global lsbox
    global labstr

    value=lsbox.get(lsbox.curselection())
    labstr.set(value)
   


if __name__=='__main__':

    window=tk.Tk()
    window.title('my window')
    window.geometry('300x200') #长宽

    labstr=tk.StringVar()
    lab=tk.Label(window,bg='yellow',width=4,textvariable=labstr)
    lab.pack()
    
    butn1=tk.Button(window,text='print selection',width=15,height=2,command=print_selection)
    butn1.pack()

    liststr=tk.StringVar()
    liststr.set((11,22,33,44))
    lsbox=tk.Listbox(window,listvariable=liststr)
    lsbox.pack()

    lsitems=[1,2,3,4]
    for item in lsitems:
        lsbox.insert('end',item)
    lsbox.insert(1,'first')#按索引插
    lsbox.insert(2,'second')
    lsbox.delete(2)

    window.mainloop()
    
    
