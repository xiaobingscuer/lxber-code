
import tkinter as tk
from tkinter import messagebox

# tkinter,窗口视图
# pack,grid,place,如何放置部件
 

if __name__=='__main__':

    window=tk.Tk()
    window.title('my window')
    window.geometry('500x500') #长宽

    #tk.Label(window,text='pack').pack(side='top')
    #tk.Label(window,text='pack').pack(side='bottom')
    #tk.Label(window,text='pack').pack(side='left')
    #tk.Label(window,text='pack').pack(side='right')

    #for i in range(4):
    #    for j in range(3):
    #        tk.Label(window,text='grid').grid(row=i,column=j,padx=20,pady=20,ipadx=10,ipady=10) #pad为外部的间距，ipad为内部间距
    #        #tk.Label(window,text='grid').grid(row=i,column=j,ipadx=10,ipady=10)

    tk.Label(window,text='place').place(x=20,y=30,anchor='nw') #x,y为窗口位置，anchor为部件的方位锚定点，锚点与窗口位置钉在一起，以此固定部件位置
    
    

    window.mainloop()
    
    
