
import tkinter as tk

# tkinter,窗口视图
# radio button


def print_selection():
    
    global lab
    global labstr

    lab.config(text='you have selected ' + labstr.get())
    


if __name__=='__main__':

    window=tk.Tk()
    window.title('my window')
    window.geometry('300x200') #长宽

    labstr=tk.StringVar()
    lab=tk.Label(window,bg='yellow',width=100,text='empty')
    lab.pack()
    
    rbutn1=tk.Radiobutton(window,text='Option A',variable=labstr,value='A',width=15,height=2,command=print_selection)
    rbutn2=tk.Radiobutton(window,text='Option B',variable=labstr,value='B',width=15,height=2,command=print_selection)
    rbutn3=tk.Radiobutton(window,text='Option C',variable=labstr,value='C',width=15,height=2,command=print_selection)
    rbutn1.pack()
    rbutn2.pack()
    rbutn3.pack()

    window.mainloop()
    
    
