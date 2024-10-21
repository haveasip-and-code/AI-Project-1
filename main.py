from algorithm import Algorithm, BFS
from state import State
from window import Window
import tkinter as tk

# Create an instance of BFS class
BFS1 = BFS()
initial = State()
BFS1.loadInput("input-01.txt", initial)
solution = BFS1.BFSSearch(initial)
BFS1.displayStats()
stateList = []
BFS1.tracePath(stateList)
for state in stateList:
    state.print_grid()
    for stone in state.displayStones():
        print(stone)
    print(state.displayPos())
    print(state.displayWeight())
    print(state.displayPath())
    print(state.displaySteps())


# Create an instance of Window class
root = tk.Tk()
window = Window(root)  # Ensure the window fills the root


def draw_states(index):
    if index >= 0:
        window.drawGrid(stateList[index].grid)
        root.after(1000, draw_states, index - 1 )  # Schedule the next state after 1 second

# Start drawing the states
root.after(5000, draw_states, len(stateList) - 1)

root.mainloop()



