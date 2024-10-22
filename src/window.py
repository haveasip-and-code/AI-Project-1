import tkinter as tk
from tkinter import messagebox
import state
import algorithm as algorithm
from maze import Maze

class Window:
    def __init__(self, master):
        self.stateList = [] 
        self.maze = Maze()

        self.master = master
        self.initial = None
        self.master.geometry("1000x600")

        self.width = 900
        self.height = 500
        self.master.title("Maze Escape")

        self.ares = tk.PhotoImage(file="images/ares.png")
        self.stone = tk.PhotoImage(file="images/stone.png")
        self.switch = tk.PhotoImage(file="images/switch.png")

        self.canvas = tk.Canvas(self.master, width = self.width, height = self.height, background="black")
        self.canvas.grid(row=2,column=0, sticky=tk.S)

        self.stepsLabel = tk.Label(self.master, text = '0', font = ('Arial', 20))
        self.costLabel = tk.Label(self.master, text = '0', font = ('Arial', 20))
        self.stepsLabel.grid(row=4,column=0,sticky=tk.W)
        self.costLabel.grid(row=4,column=1,sticky=tk.W)
        

        inputOptions = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
        self.inputOption = tk.StringVar(self.master)
        self.inputOption.set(inputOptions[0])
        self.inputMenu = tk.OptionMenu(self.master, self.inputOption, *inputOptions)
        self.inputMenu.grid(row=0,column=0,sticky=tk.W)

        self.startButton = tk.Button(self.master, text='Start', relief="raised",command=self.start)
        self.startButton.grid(row=1,column=0,sticky=tk.N)

        algOptions = ['BFS', 'DFS', 'UCS', 'A*']
        self.algOption = tk.StringVar(self.master)
        self.algOption.set(algOptions[0])
        self.algMenu = tk.OptionMenu(self.master, self.algOption, *algOptions)
        self.algMenu.grid(row=1,column=0,sticky=tk.SW)

        # self.master.resizable(width=False, height=False)
       
    def start(self):
        self.stateList = []
        algorithm = self.algOption.get()
        input_file = "input/input-" + self.inputOption.get() + ".txt"
        self.initial = state.State()
        self.initial = self.maze.loadInput(input_file, self.initial)
        self.drawGrid(self.initial.grid, self.initial.stones)
        self.maze.search(input_file, algorithm, self.stateList)
        # Start drawing the states
        if (len(self.stateList) > 0):
            tk.messagebox.showinfo("Solution found", "Solution found")
            self.master.after(3000, self.drawStates, len(self.stateList) - 2) 
        else:
            tk.messagebox.showinfo("No solution found", "No solution found")

    def drawGrid(self, grid, stones):
        self.canvas.delete("all")
        self.cellWidth = self.width / len(grid[0])
        if self.cellWidth > 80:
            self.cellWidth = 80

        self.cellHeight = self.height / len(grid)
        if self.cellHeight > 80:
            self.cellHeight = 80

        if self.cellWidth < self.cellHeight:
            self.cellHeight = self.cellWidth
        else:
            self.cellWidth = self.cellHeight

        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                x1 = j * self.cellWidth
                y1 = i * self.cellHeight
                x2 = x1 + self.cellWidth
                y2 = y1 + self.cellHeight
                if cell == '+':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="yellow")
                    self.canvas.create_rectangle(x1, y1, x2-10, y2-10, fill="white", outline="white")
                if cell == '#':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="brown", outline="black")
                elif cell == '.':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="yellow")
                elif cell == '@':
                    self.canvas.create_rectangle(x1, y1, x2-10, y2-10, fill="white", outline="white")
                elif cell == '$':
                    self.canvas.create_oval(x1, y1, x2-10, y2-10, fill="blue", outline="blue")
                    for x, y, weight in stones:
                        if (i, j) == (x, y):
                            self.canvas.create_text(x1+15, y1+15, text=str(weight), fill="white")
                            break
                elif cell == '*':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="pink", outline="pink")
                    for x, y, weight in stones:
                        if (i, j) == (x, y):
                            self.canvas.create_text(x1+10, y1+10, text=str(weight), fill="black")
                            break

        self.master.update_idletasks()

    def drawStates(self, index):
        if index >= 0:
            self.drawGrid(self.stateList[index].grid, self.stateList[index].stones)
            self.stepsLabel.config(text = str(self.stateList[index].getSteps()))
            self.costLabel.config(text = str(self.stateList[index].getCost()))
            # Schedule the next state after 1 second
            self.master.after(1000, self.drawStates, index - 1)
    
    def run(self):
        self.master.mainloop()
    

    

    

    