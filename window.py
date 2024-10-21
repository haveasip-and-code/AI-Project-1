import tkinter as tk
import state
import algorithm

class Window:
    def __init__(self, master):
        self.master = master
        self.initial = None
        self.master.geometry("800x600")
        self.width = 400
        self.height = 200
        self.master.title("Maze Escape")

        self.canvas = tk.Canvas(self.master, width = self.width, height = self.height, background="black")
        self.canvas.grid(row=2,column=0, sticky=tk.S)

        self.stepsLabel = tk.Label(self.master, text = '0', font = ('Arial', 20))
        self.weightLabel = tk.Label(self.master, text = '0', font = ('Arial', 20))
        self.stepsLabel.grid(row=4,column=0,sticky=tk.W)
        self.weightLabel.grid(row=4,column=1,sticky=tk.W)
        
        inputOptions = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.inputOption = tk.StringVar(self.master)
        self.inputOption.set(inputOptions[0])
        self.inputMenu = tk.OptionMenu(self.master, self.inputOption, *inputOptions)
        self.inputMenu.grid(row=0,column=0,sticky=tk.W)

        self.startButton = tk.Button(self.master, text='Start', command=self.start)
        self.startButton.grid(row=1,column=0,sticky=tk.N)

        self.restartButton = tk.Button(self.master, text='Restart', command=self.restart)
        self.restartButton.grid(row=1,column=0,sticky=tk.SE)

        algOptions = ['BFS', 'DFS', 'UCS', 'A*']
        self.algOption = tk.StringVar(self.master)
        self.algOption.set(algOptions[0])
        self.algMenu = tk.OptionMenu(self.master, self.algOption, *algOptions)
        self.algMenu.grid(row=1,column=0,sticky=tk.SW)

        # self.master.resizable(width=False, height=False)
       
    def start(self):
        print("Start button pressed")

    def restart(self):
        
        print("Restart button pressed")

    def drawGrid(self, grid):
        self.canvas.delete("all")
        self.cellwidth = self.width / len(grid[0])
        self.cellheight = self.height / len(grid)
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                x1 = j * self.cellwidth
                y1 = i * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                if cell == '#':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="brown", outline="black")
                elif cell == '.':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="yellow")
                elif cell == '@':
                    self.canvas.create_rectangle(x1, y1, x2-10, y2-10, fill="white", outline="white")
                elif cell == '$':
                    self.canvas.create_oval(x1, y1, x2-10, y2-10, fill="blue", outline="blue")
                elif cell == '*':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="pink", outline="pink")
        self.master.update_idletasks()


    
    

    

    

    