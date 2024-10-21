from algorithm import Algorithm, UCS
from state import State

ucs = UCS()
initialState = State()
ucs.loadInput("input-01.txt", initialState)
goalState = ucs.UCSSearch(initialState)
ucs.displayStats()