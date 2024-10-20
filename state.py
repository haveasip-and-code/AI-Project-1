
class State:
    def __init__(self, grid=None, switches=[], aresPos=(0,0), stones=[], cost=0, path=""):
        self.switches = switches
        self.grid = grid
        self.aresPos = aresPos
        self.stones = stones
        self.cost = cost
        self.path = path

    def checkGoalState(self):
        for (x,y,weight) in self.stones:
            if (x,y) not in self.switches:
                return False
        return True

    def expandState(self):
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
            yield State(self.updateGrid(new_pos, new_stones), self.switches, new_pos, new_stones, self.cost + self.actionCost(new_pos), self.path + action)

    def actionCost(self, new_pos):
        if (new_pos in [(x, y) for x, y, weight in self.stones]):
            for x, y, weight in self.stones:
                if (x, y) == new_pos:
                    return 1 + weight
        return 1
    
    def updateGrid(self, new_pos, new_stones):
        new_grid = list(self.grid)
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
        return new_grid

    def displayWeight(self):
        return self.cost - len(self.path)
    
    def displayPath(self):
        return self.path
    
    def displaySteps(self):
        return len(self.path)
    
    def displayCost(self):
        return self.cost
    
    
        