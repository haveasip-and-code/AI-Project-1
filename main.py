from algorithm import Algorithm, BFS
from state import State

# Create an instance of BFS class
BFS1 = BFS()
initial = State()
BFS1.loadInput("input-03.txt", initial)
BFS1.BFSSearch(initial.grid, initial.ares_pos, initial.stones, initial.switches)
BFS1.displayStats()




# with open("input-03.txt", 'r') as file:
#     lines = file.readlines()

# weights = list(map(int, lines[0].strip().split()))
# grid = [list(line.rstrip()) for line in lines[1:]]
# ares_pos = None
# stones = [] 
# switches = []  

# weight_index = 0  
# for i, row in enumerate(grid):
#     for j, cell in enumerate(row):
#         if cell == '@':
#             ares_pos = (i, j) 
#         elif cell == '$':
#             stones.append((i, j, weights[weight_index]))
#             weight_index += 1
#         elif cell == '*':
#             stones.append((i, j, weights[weight_index]))
#             switches.append((i, j)) 
#             weight_index += 1
#         elif cell == '.':
#             switches.append((i, j)) 

# print("Stone Weights:", weights)
# print("Ares's Position:", ares_pos)
# print("Stone Positions with Weights:", stones)
# print("Switch Positions:", switches)
# print("Grid:")
# for row in grid:
#     print("".join(row))

# solution = algorithm.BFS(grid, ares_pos, stones, switches)
# if solution:
#     print("Solution found:", solution.path)
#     print("Cost:", solution.cost)