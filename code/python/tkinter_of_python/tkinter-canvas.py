
import tkinter as tk

# tkinter,窗口视图
# canvas,画布


def moveit():
    global cav,rect
    cav.move(rect,0,10)
    


if __name__=='__main__':

    window=tk.Tk()
    window.title('my window')
    window.geometry('500x500') #长宽

    cav=tk.Canvas(window,bg='gray',height=300,width=500)
    image_file=tk.PhotoImage(file='feng.gif')
    image=cav.create_image(0,0,anchor='nw',image=image_file)

    x0,y0,x1,y1=50,50,80,80
    line=cav.create_line(x0,y0,x1,y1)
    oval=cav.create_oval(x0+50,y0+100,x1,y1+100,fill='red')
    arc=cav.create_arc(x0+30,y0+30,x1+30,y1+30,start=0,extent=180)
    rect=cav.create_rectangle(200,0,300,100,fill='red')
    cav.pack()
    
    butn=tk.Button(window,text='move',command=moveit)
    butn.pack()

    window.mainloop()
    
    
