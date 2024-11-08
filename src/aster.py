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

    def calculate_min_distance(self, state, stone_idx, used_switches, current_distance):
        # Base case: If all stones have been assigned to a switch
        if stone_idx == len(state.stones):
            return current_distance

        min_distance = 2**31 - 1  # Initialize with a large value
        
        # Try assigning the current stone to each available switch
        for i, switch in enumerate(state.switches):
            if not used_switches[i]:  # If the switch has not been assigned
                stone_position = state.stones[stone_idx][:2]
                stone_weight = state.stones[stone_idx][2]
                # Calculate distances
                dist_ares_to_stone = self.manhattan_distance(state.aresPos, stone_position)
                dist_stone_to_switch = self.manhattan_distance(stone_position, switch) * (stone_weight + 1)
                total_distance = dist_ares_to_stone + dist_stone_to_switch
                
                # Mark this switch as used
                used_switches[i] = True
                
                # Recursively assign the remaining stones
                min_distance = min(min_distance, self.calculate_min_distance(state, stone_idx + 1, used_switches, current_distance + total_distance))
                
                # Backtrack: Unmark the switch to try other pairings
                used_switches[i] = False
    
        return min_distance

    def heuristic(self, state):
        used_switches = [False] * len(state.switches)  # Track which switches have been assigned
        return self.calculate_min_distance(state, 0, used_switches, 0)


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
            self.memory = peak / (1024*1024)
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
                    self.memory = peak / (1024*1024)
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
        self.memory = peak / (1024*1024)
        self.goal = None
        return None
                
