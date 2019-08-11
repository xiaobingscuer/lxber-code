
import tkinter as tk

# tkinter,窗口视图
# scale,可拉动条尺


def print_selection(v):
    
    global lab

    lab.config(text='you have selected ' + v)
    


if __name__=='__main__':

    window=tk.Tk()
    window.title('my window')
    window.geometry('300x200') #长宽

    labstr=tk.StringVar()
    lab=tk.Label(window,bg='yellow',width=100,text='empty')
    lab.pack()
    
    scale=tk.Scale(window,label='try me',from_=5,to=10,orient=tk.HORIZONTAL,length=300,showvalue=True,tickinterval=1,resolution=0.001,command=print_selection)
    scale.pack()

    window.mainloop()
    
    
