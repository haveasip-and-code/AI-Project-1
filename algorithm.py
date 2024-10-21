from collections import deque
import os
import heapq
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


class UCS(Algorithm):
    algName = "UCS"
    def __init__(self):
        super().__init__()
    
    def UCSSearch(self, state):
        initialState = State(state.grid, state.switches, state.aresPos, state.stones, 0, "")
        self.goal = initialState
        priority_queue = []
        heapq.heappush(priority_queue, (initialState.getCost(), initialState))
        self.visited.add((initialState.aresPos, tuple(initialState.stones)))

        while priority_queue:
            currentState = heapq.heappop(priority_queue)[1]
            if currentState.checkGoalState():
                self.goal = currentState
                return self.goal
            for nextState in currentState.expandState():
                if (nextState.aresPos, tuple(nextState.stones)) not in self.visited:
                    heapq.heappush(priority_queue, (nextState.getCost(), nextState))
                    self.visited.add((nextState.aresPos, tuple(nextState.stones)))

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