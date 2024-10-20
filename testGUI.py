import window
from state import State
from algorithm import Algorithm, BFS
import tkinter as tk
import window
BFS1 = BFS()
initial = State()
state = State()
BFS1.loadInput("input-02.txt", initial)
state = BFS1.BFSSearch(initial.grid, initial.ares_pos, initial.stones, initial.switches)

