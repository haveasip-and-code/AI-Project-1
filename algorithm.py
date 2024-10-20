from collections import deque
import os
from state import State
import tracemalloc
import time

class Algorithm:
    def __init__(self):
        self.initial = None
        self.goal = None
        self.input = input
        self.time = 0 
        self.memory = 0
        self.visited = set()

    def getInitial(self):
        return self.initial

    def loadInput(self, fileName, state):
        self.input = fileName
        with open(fileName, 'r') as file:
            lines = file.readlines()

        weights = list(map(int, lines[0].strip().split()))
        state.grid = [list(line.rstrip()) for line in lines[1:]]
        state.ares_pos = None
        state.stones = [] 
        state.switches = []  

        weight_index = 0  
        for i, row in enumerate(state.grid):
            for j, cell in enumerate(row):
                if cell == '@':
                    state.ares_pos = (i, j) 
                elif cell == '$':
                    state.stones.append((i, j, weights[weight_index]))
                    weight_index += 1
                elif cell == '*':
                    state.stones.append((i, j, weights[weight_index]))
                    state.switches.append((i, j)) 
                    weight_index += 1
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
    alg_name = "BFS"
    def __init__(self):
        super().__init__()
    
    def BFSSearch(self,grid, aresPos, stones, switches):
        tracemalloc.start()  
        start_time = time.time()
        initialState = State(aresPos, stones, 0, "")
        self.goal = initialState
        if (initialState.checkGoalState(switches)):
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            self.time = (end_time - start_time) * 1000  # ms
            self.memory = peak / 1024
            return self.goal
        queue = deque()
        queue.append(initialState)
        self.visited.add((aresPos, tuple(initialState.stones)))

        while queue:
            currentState = queue.popleft()
            for newState in currentState.expandState( grid):
                if (newState.checkGoalState( switches)):
                    self.goal = newState
                    end_time = time.time()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    self.time = (end_time - start_time) * 1000  # ms
                    self.memory = peak / 1024
                    return self.goal
                if (newState.aresPos, tuple(newState.stones)) in self.visited:
                    continue
                queue.append(newState)
                self.visited.add((newState.aresPos, tuple(newState.stones)))
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.time = (end_time - start_time) * 1000  # ms
        self.memory = peak / 1024
        return None
    
    def displayStats(self):
        fileName = "output" + self.input[5:]
        with open(fileName, "a") as file:
            file.write(self.alg_name + "\n")
            file.write("Steps: " + str(self.goal.displaySteps()) + ", ")
            file.write("Weight: " + str(self.goal.displayWeight()) + ", ")
        Algorithm.displayStats(self)
        if self.goal.displaySteps() > 0:
            with open(fileName, "a") as file:
                file.write(str(self.goal.displayPath()) + "\n")
        else:
            with open(fileName, "a") as file:
                file.write("No solution found\n")
                


        