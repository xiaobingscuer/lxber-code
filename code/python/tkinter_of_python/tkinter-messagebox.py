
import tkinter as tk
from tkinter import messagebox

# tkinter,窗口视图
# messagebox,消息盒子,弹窗


def hit_me():
    messagebox.showinfo(title='showinfo',message='info..')
    messagebox.showwarning(title='showwarning',message='warning')
    messagebox.showerror(title='showerror',message='error')
    print(messagebox.askquestion(title='askquestion',message='ok ?')) #return 'yes' or 'no'
    print(messagebox.askyesno(title='askquestion',message='true or false')) #return True or False
    print(messagebox.askretrycancel(title='askquestion',message='try or cancel')) #return True or False
    print(messagebox.askokcancel(title='askquestion',message='ok or cancel')) #return True or False
    

if __name__=='__main__':

    window=tk.Tk()
    window.title('my window')
    window.geometry('500x500') #长宽

    tk.Button(window,text='hit me', command=hit_me).pack()

    window.mainloop()
    
    
