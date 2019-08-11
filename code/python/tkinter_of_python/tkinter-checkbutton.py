
import tkinter as tk

# tkinter,窗口视图
# checkbutton,勾选框


def print_selection():
    
    global lab
    global var1,var2

    if(var1.get()==1) & (var2.get()==0):
        lab.config(text='I love only python')
    elif(var1.get()==0) & (var2.get()==1):
        lab.config(text='I love only C++')
    elif(var1.get()==0) & (var2.get()==0):
        lab.config(text='I don not love either')
    else:
        lab.config(text='I love both')
    


if __name__=='__main__':

    window=tk.Tk()
    window.title('my window')
    window.geometry('300x200') #长宽

    lab=tk.Label(window,bg='yellow',width=100,text='empty')
    lab.pack()

    var1=tk.IntVar()
    var2=tk.IntVar()
    chkbutn1=tk.Checkbutton(window,text='Python',variable=var1,onvalue=1,offvalue=0,command=print_selection)
    chkbutn2=tk.Checkbutton(window,text='C++',variable=var2,onvalue=1,offvalue=0,command=print_selection)
    chkbutn1.pack()
    chkbutn2.pack()

    window.mainloop()
    
    
