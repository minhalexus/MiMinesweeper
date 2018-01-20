from tkinter import *
import tkinter.messagebox
import random
import os, sys


LARGE_FONT = ("Verdana", 20)

buttons = []
bombs = random.sample(range(1, 65), 10)
if 58 not in bombs:
    bombs.pop()
    bombs.append(58)
bombs.sort()


x = []
for i in range(1,65):
    x.append(i)


class Minesweeper(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self,*args, **kwargs)
        container = Frame(self)

        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        menubar = Menu(container)
        filemenu = Menu(menubar, tearoff = 0)
        filemenu.add_command(label = "Restart", command = lambda: restartProgram())
        filemenu.add_separator()
        filemenu.add_command(label = "Exit", command = quit)
        menubar.add_cascade(label = "File", menu = filemenu)

        Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class StartPage(Frame):

    def __init__(self,parent,controller):
        gameFrame = Frame.__init__(self,parent)
        self.header()
        self.base()

    def header(self, *args):
        headerFrame = Frame(self, width=11, height=3, bg='grey', borderwidth=3, relief="raised")

        flags = Label(headerFrame, width=4, text="10", font=LARGE_FONT, padx=5, bg = 'black', fg = 'red')
        flags.pack(side=LEFT,fill="both", expand=True)

        if args == 1:
            reset = Button(headerFrame, width=4, height=2, bg='green')
            reset.pack(side=LEFT, fill="both", expand=True)
        else:
            reset = Button(headerFrame, width=4, height=2, bg='yellow', command = lambda: restartProgram())
            reset.pack(side=LEFT, fill="both", expand=True)


        timer = Label(headerFrame, width=4, text = "000", font=LARGE_FONT, padx=5, bg = 'black', fg = 'red')
        timer.pack(side=LEFT, fill="both", expand=True)

        headerFrame.pack(side=TOP, fill="both", expand=True)

    def base(self):

        baseFrame=Frame(self, width=200, height=240, bg='grey', borderwidth=3, relief="raised")

        for i in range(8):
            for j in range(1,9):
                button = Button(baseFrame, width=2, height=1, bg='grey')
                button.configure(command = lambda i=i, j=j: self.buttonPress((8*i) + j))
                buttons.append(button)
        for i in range(len(buttons)):
            buttons[i].grid(row = int(i/8), column = i%8)

        baseFrame.pack(side=BOTTOM, fill="both", expand=True)


    def buttonPress(self,val):
        try:
            if (buttons[val-1]['state']) != 'disabled':
                if val in bombs:
                    buttons[val - 1].configure(bg='red', state='disabled', relief='sunken')
                    tkinter.messagebox.showinfo('Minesweeper', 'Sorry You Lost!')

                else:
                    neighbours = self.getNeighbours(val)

                    badNeighbours = 0
                    for i in range(len(neighbours)):
                        if neighbours[i] in bombs:
                            badNeighbours += 1

                    buttons[val - 1].configure(bg='lightgrey', state = 'disabled', relief = 'sunken')
                    x.remove(val)

                    self.checkWinConditions()


                    if badNeighbours == 0:
                        for i in range (0,len(neighbours),2):
                            self.buttonPress(neighbours[i])
                    else:
                        buttons[val-1].configure(text = (badNeighbours))
        except:
            pass
    def checkWinConditions(self):
        if x == bombs:
            tkinter.messagebox.showinfo('Minesweeper', 'Congratulations! You Won!')




    def getNeighbours(self, val):

        neightbours = []
        corners = [1,8,57,58]
        lEdge = [9,17,25,33,41,49]
        tEdge =[2,3,4,5,6,7]
        bEdge=[58,59,60,61,62,63]
        rEdge = [16,24,32,40,48,56]


        if val in corners:
            neighbours = self.corners(val)
        elif val in tEdge:
            neighbours = self.tEdge(val)
        elif val in bEdge:
            neighbours = self.bEdge(val)
        elif val in lEdge:
            neighbours = self.lEdge(val)
        elif val in rEdge:
            neighbours = self.rEdge(val)
        else:
            neighbours =self.mid(val)

        return neighbours

    def corners(self, val):
        if val == 1:
            return [2,9,10]
        elif val == 8:
            return [7,15,16]
        elif val == 57:
            return [49,50,58]
        elif val == 64:
            return [55,56,63]

    def tEdge(self,val):
        n = []
        n.append(val-1)
        n.append(val + 1)
        n.append(val -1 + 8)
        n.append(val + 8)
        n.append(val + 1 + 8)
        return n

    def bEdge(self,val):
        n = []
        n.append(val - 1)
        n.append(val + 1)
        n.append(val - 1 - 8)
        n.append(val -8)
        n.append(val + 1 -8)
        return n

    def lEdge(self,val):
        n = []
        n.append(val - 8)
        n.append(val -8 + 1)
        n.append(val + 1)
        n.append(val + 8)
        n.append(val +8 + 1)
        return n

    def rEdge(self,val):
        n = []
        n.append(val - 8)
        n.append(val -8 - 1)
        n.append(val - 1)
        n.append(val + 8)
        n.append(val +8 - 1)
        return n

    def mid(self, val):
        n = []
        n.append(val - 8 - 1)
        n.append(val - 8)
        n.append(val - 8 + 1)

        n.append(val - 1)
        n.append(val + 1)

        n.append(val + 8 -1)
        n.append(val + 8)
        n.append(val + 8 + 1)
        return n


class PageOne(Frame):

    def __init__(self,parent,controller):
        gameFrame = Frame.__init__(self,parent)




def runApp():
    app = Minesweeper()
    app.geometry("200x270")
    app.wm_title("Minhal Minesweeper")
    app.mainloop()

def restartProgram():
    python = sys.executable
    os.execl(python, python, * sys.argv)

runApp()





