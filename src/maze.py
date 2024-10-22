from mazeSolverContext import MazeSolverContext
from bfs import BFS
from ucs import UCS
from state import State
from aster import Aster

class Maze:
    def __init__(self):
        self.input = None
        self._mazeSolverContext = MazeSolverContext()

    def loadInput(self, fileName, state):
        self.input = fileName
        with open(fileName, 'r') as file:
            lines = file.readlines()

        weights = list(map(int, lines[0].strip().split()))
        state.grid = [list(line.rstrip()) for line in lines[1:]]
        state.aresPos = None
        state.stones = [] 
        state.switches = []  
        state.parent = None

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

    def search(self, filename: str, algName: str, stateList: list):
        # Create an instance of State class
        initial = State()

        # Load input file
        self.loadInput(filename, initial)

        # Create an instance of Search class
        if algName == "BFS":
            self._mazeSolverContext.setStrategy(BFS(algName))
        # elif algName == "DFS":
        #    self._mazeSolverContext.setStrategy(DFS(algName))
        elif algName == "UCS":
            self._mazeSolverContext.setStrategy(UCS(algName))
        elif algName == "A*":
            self._mazeSolverContext.setStrategy(Aster(algName))
        
        self._mazeSolverContext.solveMaze(initial, stateList, self.input)

        # Print the solution
        for state in stateList:
            state.print_grid()
            for stone in state.getStones():
                print(stone)
            print(state.getPos())
            print(state.getWeight())
            print(state.getPath())
            print(state.getSteps())