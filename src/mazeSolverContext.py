from algorithm import Algorithm

class MazeSolverContext():
    def __init__(self):
        self._strategy = None

    def setStrategy(self, strategy: Algorithm):
        self._strategy = strategy

    def solveMaze(self, state, stateList: list, input: str):
        self._strategy.solve(state)
        self._strategy.displayStats(input)
        self._strategy.tracePath(stateList)
        
    
    def getNodes(self) -> int:
        return len(self._strategy.visited)
    
    
    def getMemory(self) -> int:
        return self._strategy.memory
    
    
    def getTime(self) -> int:
        return self._strategy.time