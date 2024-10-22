import time
import tracemalloc
from collections import deque
from algorithm import Algorithm
from state import State

class DFS(Algorithm):
    def __init__(self, algName):
        super().__init__(algName)
    
    def solve(self, state):
        # Start the timer and memory tracker
        tracemalloc.start()  
        startTime = time.time()

        # Initialize the initial state and goal state
        initialState = State(state.grid, state.switches, state.aresPos, state.stones, 0, "", state.parent)
        self.goal = initialState

        # Check if the initial state is the goal state
        if (initialState.checkGoalState()):
            endTime = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            self.time = (endTime - startTime) * 1000  # ms
            self.memory = peak / 1024
            return self.goal
        
        # Initialize the queue and add the initial state to it
        stack = deque()
        stack.append(initialState)
        self.visited[(initialState.aresPos, tuple(initialState.stones))] = initialState.getCost()


        # Start the DFS algorithm
        while stack:
            currentState = stack.pop()
            currentState.print_grid()
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
                stack.append(newState)
                self.visited[(newState.aresPos, tuple(newState.stones))] = newState.getCost()



        # Stop the timer and memory tracker
        endTime = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.time = (endTime - startTime) * 1000  # ms
        self.memory = peak / 1024
        self.goal = None
        return None
        
