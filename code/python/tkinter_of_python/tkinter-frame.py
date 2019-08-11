
import tkinter as tk

# tkinter,窗口视图
# frame,框架,布局

count=0

def do_job():
    global count
    lab.config(text='count: '+str(count))
    count+=1
    

if __name__=='__main__':

    window=tk.Tk()
    window.title('my window')
    window.geometry('500x500') #长宽

    tk.Label(window,text='on the window',bg='gray').pack()

    frm=tk.Frame(window)
    frm.pack()

    frm_left=tk.Frame(frm,)
    frm_right=tk.Frame(frm,)

    frm_left.pack(side='left')
    frm_right.pack(side='right')

    tk.Label(frm_left,bg='blue',text='first on the frame left').pack()
    tk.Label(frm_left,bg='blue',text='second on the frame left').pack()
    tk.Label(frm_right,bg='red',text='on the frame right').pack()
    
    window.mainloop()
    
    
