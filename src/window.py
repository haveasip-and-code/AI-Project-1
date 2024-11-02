import tkinter as tk
from tkinter import messagebox, PhotoImage, Toplevel, Label
from PIL import Image, ImageTk
import state
import algorithm as algorithm
from maze import Maze
import threading

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

        self.canvas = tk.Canvas(self.master, width = self.width, height = self.height, background="black")
        self.canvas.grid(row=2,column=0, sticky=tk.S)
    
        self.stepsLabel = tk.Label(self.master, text = 'Steps: 0', font = ('Arial', 20))
        self.costLabel = tk.Label(self.master, text = 'Cost: 0', font = ('Arial', 20))
        self.stepsLabel.grid(row=4,column=0,sticky=tk.W)
        self.costLabel.grid(row=4,column=1,sticky=tk.W)
        

        inputOptions = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
        self.inputOption = tk.StringVar(self.master)
        self.inputOption.set(inputOptions[0])
        self.inputMenu = tk.OptionMenu(self.master, self.inputOption, *inputOptions)
        self.inputMenu.config(bg='#fad581')
        self.inputMenu.grid(row=0,column=0,sticky=tk.W)

        self.startButton = tk.Button(self.master, text='Start', relief="raised",command=self.start)
        self.startButton.grid(row=1,column=0,sticky=tk.N)

        algOptions = ['BFS', 'DFS', 'UCS', 'A*']
        self.algOption = tk.StringVar(self.master)
        self.algOption.set(algOptions[0])
        self.algMenu = tk.OptionMenu(self.master, self.algOption, *algOptions)
        self.algMenu.config(bg='#fad581')
        self.algMenu.grid(row=1,column=0,sticky=tk.SW)

    def show_loading_screen(self):
        self.loading_window = Toplevel(self.master)
        self.loading_window.title("Loading...")
        Label(self.loading_window, text="Finding solution, please wait...").pack(pady=10, padx=20)
        self.loading_window.geometry("300x100")
        self.loading_window.grab_set()

    
    def hide_loading_screen(self):
    # Hide the loading screen when done
        if self.loading_window:
            self.loading_window.destroy()

    def run_search(self, input_file, algorithm):
        self.maze.search(input_file, algorithm, self.stateList)  # Run the search
        self.hide_loading_screen()  # Hide the loading screen once search is complete

        # Check the result and show the appropriate message
        if len(self.stateList) > 0:

            tk.messagebox.showinfo("Solution found", "Solution found")
            self.master.after(2000, self.drawStates, len(self.stateList) - 2) 
        else:
            tk.messagebox.showinfo("No solution found", "No solution found")
            
    def start(self):
        self.stateList = []
        algorithm = self.algOption.get()
        input_file = "input/input-" + self.inputOption.get() + ".txt"
        self.initial = state.State()
        self.initial = self.maze.loadInput(input_file, self.initial)
        self.drawGrid(self.initial.grid, self.initial.stones)
        self.show_loading_screen()

        search_thread = threading.Thread(target=self.run_search, args=(input_file, algorithm))
        search_thread.start()
        # self.maze.search(input_file, algorithm, self.stateList)

        # Start drawing the states
        # if (len(self.stateList) > 0):
        #     tk.messagebox.showinfo("Solution found", "Solution found")
        #     self.master.after(3000, self.drawStates, len(self.stateList) - 2) 
        # else:
        #     tk.messagebox.showinfo("No solution found", "No solution found")

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

        self.ares = resize_image("images/ares.png", self.cellWidth, self.cellHeight)
        self.stone = resize_image("images/stone.png", self.cellWidth, self.cellHeight)
        self.switch = resize_image("images/switch.png", self.cellWidth, self.cellHeight)
        self.finish = resize_image("images/finish.png", self.cellWidth, self.cellHeight)

        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                x1 = j * self.cellWidth
                y1 = i * self.cellHeight
                x2 = x1 + self.cellWidth
                y2 = y1 + self.cellHeight
                if cell == '+':
                    self.canvas.create_image(x1, y1, image=self.switch, anchor='nw')
                    self.canvas.create_image(x1, y1, image=self.ares, anchor='nw')
                if cell == '#':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="brown", outline="black")
                elif cell == '.':
                    self.canvas.create_image(x1, y1, image=self.switch, anchor='nw')
                    # self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="yellow")
                elif cell == '@':
                    self.canvas.create_image(x1, y1, image=self.ares, anchor='nw')
                    # self.canvas.create_rectangle(x1, y1, x2-10, y2-10, fill="white", outline="white")
                elif cell == '$':
                    self.canvas.create_image(x1, y1, image=self.stone, anchor='nw')
                    # self.canvas.create_oval(x1, y1, x2-10, y2-10, fill="blue", outline="blue")
                    for x, y, weight in stones:
                        if (i, j) == (x, y):
                            center_x = (x1 + x2 - 10) / 2
                            center_y = (y1 + y2 - 10) / 2

                            stone_width = x2 - x1 - 10
                            stone_height = y2 - y1 - 10

                            # Set the font size as a fraction of the stone's height (adjust as needed)
                            font_size = int(stone_height * 0.4)

                            # Create the text with the calculated font size and center position
                            self.canvas.create_text(center_x, center_y, text=str(weight), fill="black", font=("Arial", font_size))
                            break
                elif cell == '*':
                    self.canvas.create_image(x1, y1, image=self.finish, anchor='nw')
                    for x, y, weight in stones:
                        if (i, j) == (x, y):
                            center_x = (x1 + x2) / 2
                            center_y = (y1 + y2) / 2
                            
                            switch_width = x2 - x1
                            switch_height = y2 - y1

                            # Set the font size as a fraction of the stone's height (adjust as needed)
                            font_size = int(switch_height * 0.4)

                            # Create the text with the calculated font size and center position
                            self.canvas.create_text(center_x, center_y, text=str(weight), fill="black", font=("Arial", font_size))
                            break

        self.master.update_idletasks()

    def drawStates(self, index):
        if index >= 0:
            self.drawGrid(self.stateList[index].grid, self.stateList[index].stones)
            self.stepsLabel.config(text = "Steps: " + str(self.stateList[index].getSteps()))
            self.costLabel.config(text = "Cost: " + str(self.stateList[index].getCost()))
            # Schedule the next state after 1 second
            self.master.after(1000, self.drawStates, index - 1)
    
    def run(self):
        self.master.mainloop()

def resize_image(image_path, width, height):
    img = Image.open(image_path)
    resized_img = img.resize((int(width), int(height)), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized_img)

    

    

    