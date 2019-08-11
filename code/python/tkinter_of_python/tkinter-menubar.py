
import tkinter as tk

# tkinter,窗口视图
# menubar,菜单

count=0

def do_job():
    global count
    lab.config(text='count: '+str(count))
    count+=1
    

if __name__=='__main__':

    window=tk.Tk()
    window.title('my window')
    window.geometry('500x500') #长宽

    
    lab=tk.Label(window,text='lxber',bg='green',font=('Arial',14))
    lab.pack()

    menubar=tk.Menu(window)
    
    filemenu=tk.Menu(menubar,tearoff=0)
    menubar.add_cascade(label='File',menu=filemenu)
    filemenu.add_command(label='New',command=do_job)
    filemenu.add_command(label='Open',command=do_job)
    filemenu.add_command(label='Save',command=do_job)
    filemenu.add_separator()
    filemenu.add_command(label='Exit',command=window.quit)

    submenu=tk.Menu(filemenu)
    filemenu.add_cascade(label='Import',menu=submenu,underline=0)
    submenu.add_command(label='sub1',command=do_job)
    submenu.add_command(label='sub2',command=do_job)

    editmenu=tk.Menu(menubar,tearoff=0)
    menubar.add_cascade(label='Edit',menu=editmenu)
    editmenu.add_command(label='Cut',command=do_job)
    editmenu.add_command(label='Copy',command=do_job)
    editmenu.add_command(label='Paste',command=do_job)
    editmenu.add_separator()
    editmenu.add_command(label='Exit',command=window.quit)

    window.config(menu=menubar)
    
    window.mainloop()
    
    
