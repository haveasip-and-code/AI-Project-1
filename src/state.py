
class State:
    def __init__(self, grid=None, switches=[], aresPos=(0,0), stones=[], cost=0, path="", parent=None):
        self.switches = switches
        self.grid = grid
        self.aresPos = aresPos
        self.stones = stones
        self.cost = cost
        self.path = path
        self.parent = parent

    def __lt__(self, other):
        return self.getCost() < other.getCost()
      
    def checkGoalState(self):
        for (x, y, weight) in self.stones:
            if (x,y) not in self.switches:
                return False
        return True

    def expandState(self):
        state = self
        actions = [(-1, 0, 'u'), (1, 0, 'd'), (0, -1, 'l'), (0, 1, 'r')]
        for action in actions:
            new_pos = (self.aresPos[0] + action[0], self.aresPos[1] + action[1])
            if (new_pos[0] < 0 or new_pos[0] >= len(self.grid) or new_pos[1] < 0 or new_pos[1] >= len(self.grid[0])):
                continue
            if (self.grid[new_pos[0]][new_pos[1]] == '#'):
                continue
            if (new_pos in [(x, y) for x, y, weight in self.stones]):
                dx = new_pos[0] + action[0]
                dy = new_pos[1] + action[1]
                if (self.grid[dx][dy] == '#' or (dx, dy) in [(x, y) for x, y, weight in self.stones]):
                    continue
                new_stones = list(self.stones)
                for i, (x, y, weight) in enumerate(new_stones):
                    if (x, y) == new_pos:
                        new_stones[i] = (dx, dy, weight)
                        break
                new_stones = tuple(new_stones)
                action = action[2].upper()
            else:
                new_stones = self.stones
                action = action[2]
            newGrid = self.updateGrid(new_pos, new_stones)
            yield State(newGrid, self.switches, new_pos, new_stones, self.cost + self.getActionCost(new_pos), self.path + action, state)
    
    def updateGrid(self,new_pos, new_stones):
        new_grid =  [list(row) for row in self.grid]
        for i, row in enumerate(new_grid):
            for j, cell in enumerate(row):
                if new_grid[i][j] == '#' or new_grid[i][j] == '.':
                    continue
                else:
                    new_grid[i][j] = ' '

        for x, y, weight in new_stones:
            new_grid[x][y] = '$'

        new_grid[new_pos[0]][new_pos[1]] = '@'

        for x, y in self.switches:
            new_grid[x][y] = '.'
            
        for x, y, weight in new_stones:
            if (x, y) in self.switches:
                new_grid[x][y] = '*'
        
        for x, y in self.switches:
            if new_pos == (x, y):
                new_grid[x][y] = '+'
                
        new_grid = tuple(tuple(row) for row in new_grid)
        return new_grid
    
    def getActionCost(self, new_pos):
        if (new_pos in [(x, y) for x, y, weight in self.stones]):
            for x, y, weight in self.stones:
                if (x, y) == new_pos:
                    return 1 + weight
        return 1

    def getWeight(self):
        if self == None:
            return 0
        return self.cost - len(self.path)
    
    def getPath(self):
        if self == None:
            return ""
        return self.path
    
    def getSteps(self):
        if self == None:
            return 0
        return len(self.path)
    
    def getCost(self):
        if self == None:
            return 0
        return self.cost

    def getStones(self):
        if self == None:
            return []
        return self.stones
    
    def getPos(self):
        if self == None:
            return (0,0)
        return self.aresPos
    
    def print_grid(self):
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))
        print() 
    
    