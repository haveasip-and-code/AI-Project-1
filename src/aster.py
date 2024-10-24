from algorithm import Algorithm
from state import State
import time
import tracemalloc
from heapq import heappush, heappop

class Aster(Algorithm):
    def __init__(self, algName):
        super().__init__(algName)

    def manhattan_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return abs(x1 - x2) + abs(y1 - y2)

    def heuristic(self, state):
        h = 2**31 - 1
        # For each stone, calculate its weighted distance to the nearest switch
        for stone_idx, (x, y, weight) in enumerate(state.stones):
            for switch in state.switches:
                h = min(h, self.manhattan_distance(state.aresPos, (x, y)) + self.manhattan_distance((x, y), switch) * (weight + 1))
        return h

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
        
        # Initialize the priority queue and add the initial state to it
        queue = []
        heappush(queue, (self.heuristic(initialState) + initialState.getCost(), initialState))
        self.visited[(initialState.aresPos, tuple(initialState.stones))] = 0

        # Start the A* algorithm
        while queue:
            currentState = heappop(queue)[1]
            for newState in currentState.expandState():
                # Check if the new state is the goal state
                if (newState.checkGoalState()):
                    self.goal = newState
                    endTime = time.time()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    self.time = (endTime - startTime) * 1000
                    self.memory = peak / 1024
                    return self.goal
                
                # Check if the state has been visited before
                if (newState.aresPos, tuple(newState.stones)) in self.visited and newState.getCost() >= self.visited[(newState.aresPos, tuple(newState.stones))]:
                    continue
                heappush(queue, (self.heuristic(newState) + initialState.getCost(), newState))
                self.visited[(newState.aresPos, tuple(newState.stones))] = newState.getCost()

        # Stop the timer and memory tracker
        endTime = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.time = (endTime - startTime) * 1000
        self.memory = peak / 1024
        self.goal = None
        return None
                
