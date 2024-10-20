from collections import deque
import os
from state import State
import tracemalloc
import time

class Algorithm:
    def __init__(self):
        self.goal = None
        self.input = input
        self.time = 0 
        self.memory = 0
        self.visited = set()

    def loadInput(self, fileName, state):
        self.input = fileName
        with open(fileName, 'r') as file:
            lines = file.readlines()

        weights = list(map(int, lines[0].strip().split()))
        state.grid = [list(line.rstrip()) for line in lines[1:]]
        state.aresPos = None
        state.stones = [] 
        state.switches = []  

        weightIndex = 0  
        for i, row in enumerate(state.grid):
            for j, cell in enumerate(row):
                if cell == '@':
                    state.aresPos = (i, j) 
                elif cell == '$':
                    state.stones.append((i, j, weights[weightIndex]))
                    weightIndex += 1
                elif cell == '*':
                    state.stones.append((i, j, weights[weightIndex]))
                    state.switches.append((i, j)) 
                    weightIndex += 1
                elif cell == '.':
                    state.switches.append((i, j)) 
        self.initial = state

    def displayStats(self):
        output = "output" + self.input[5:]
        with open(output, "a") as file:
            file.write("Nodes: " + str(len(self.visited)) + ", ")
            file.write("Time (ms): " + str(self.time) + ", ")
            file.write("Memory (MB): " + str(self.memory) + "\n")


class BFS(Algorithm):
    algName = "BFS"
    def __init__(self):
        super().__init__()
    
    def BFSSearch(self,state):
        tracemalloc.start()  
        startTime = time.time()
        initialState = State(state.grid, state.switches, state.aresPos, state.stones, 0, "")
        self.goal = initialState
        if (initialState.checkGoalState()):
            endTime = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            self.time = (endTime - startTime) * 1000  # ms
            self.memory = peak / 1024
            return self.goal
        queue = deque()
        queue.append(initialState)
        self.visited.add((initialState.aresPos, tuple(initialState.stones)))

        while queue:
            currentState = queue.popleft()
            for newState in currentState.expandState():
                if (newState.checkGoalState()):
                    self.goal = newState
                    endTime = time.time()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    self.time = (endTime - startTime) * 1000  # ms
                    self.memory = peak / 1024
                    return self.goal
                if (newState.aresPos, tuple(newState.stones)) in self.visited:
                    continue
                queue.append(newState)
                self.visited.add((newState.aresPos, tuple(newState.stones)))
        endTime = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.time = (endTime - startTime) * 1000  # ms
        self.memory = peak / 1024
        return None
    
    def displayStats(self):
        fileName = "output" + self.input[5:]
        with open(fileName, "a") as file:
            file.write(self.algName + "\n")
            file.write("Steps: " + str(self.goal.displaySteps()) + ", ")
            file.write("Weight: " + str(self.goal.displayWeight()) + ", ")
        Algorithm.displayStats(self)
        if self.goal.displaySteps() > 0:
            with open(fileName, "a") as file:
                file.write(str(self.goal.displayPath()) + "\n")
        else:
            with open(fileName, "a") as file:
                file.write("No solution found\n")