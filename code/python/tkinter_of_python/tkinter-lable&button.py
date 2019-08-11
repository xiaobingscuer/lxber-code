
import tkinter as tk

# tkinter,窗口视图
# label & button


def hit_me():
    
    global on_hit,labstr
    
    if on_hit==False:
        labstr.set('you hit me')
        on_hit=True
    else:
        labstr.set('lxber')
        on_hit=False
    

if __name__=='__main__':

    window=tk.Tk()
    window.title('my window')
    window.geometry('300x100') #长宽

    labstr=tk.StringVar()
    labstr.set('lxber')

    lab=tk.Label(window,textvariable=labstr,bg='green',font=('Arial',14),width=15,height=2)
    #lab=tk.Label(window,text='lxber',bg='green',font=('Arial',14),width=15,height=2)
    lab.pack()
    # lab.place()

    on_hit=False
    
    butn=tk.Button(window,text='hit me',width=15,height=2,command=hit_me)
    butn.pack()

    window.mainloop()
    
    
