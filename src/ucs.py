from algorithm import Algorithm
from state import State
import heapq

class UCS(Algorithm):
    def __init__(self, algName):
        super().__init__(algName)
    def solve(self, state):
        #Initialize the initial state and goal state
        initialState = State(state.grid, state.switches, state.aresPos, state.stones, 0, "")
        self.goal = initialState
        #Create a priority queue and add the initial state to it
        priority_queue = []
        heapq.heappush(priority_queue, (initialState.getCost(), initialState))

        self.visited[(initialState.aresPos, tuple(initialState.stones))] = 0

        while priority_queue:
            currentState = heapq.heappop(priority_queue)[1]
            if currentState.checkGoalState():
                self.goal = currentState
                return self.goal
            for nextState in currentState.expandState():
                if (nextState.aresPos, tuple(nextState.stones)) not in self.visited or nextState.getCost() < self.visited[(nextState.aresPos, tuple(nextState.stones))]:
                    heapq.heappush(priority_queue, (nextState.getCost(), nextState))
                    self.visited[(nextState.aresPos, tuple(nextState.stones))] = nextState.getCost()

        self.goal = None
        return None