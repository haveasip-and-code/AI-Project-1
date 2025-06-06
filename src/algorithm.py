from abc import abstractmethod

class Algorithm:
    def __init__(self, algName: str):
        self.visited = {}

        self.time = 0
        self.memory = 0
        self.goal = None
        self.algName = algName

    @abstractmethod
    def solve(self, state):
        pass

    def tracePath(self, stateList) -> None:
        currentState = self.goal
        while (currentState != None):
            stateList.append(currentState)
            currentState = currentState.parent

    def displayStats(self, input_file: str) -> None:
        # Write the stats to the output file
        fileName = "output/output" + input_file[11:]
        with open(fileName, "a") as file:
            file.write(self.algName + "\n")
            if (self.goal == None):
                file.write("Steps: 0, ")
                file.write("Cost: 0, ")
            else:
                file.write("Steps: " + str(self.goal.getSteps()) + ", ")
                file.write("Cost: " + str(self.goal.getCost()) + ", ")


            file.write("Nodes: " + str(len(self.visited)) + ", ")
            file.write("Time (ms): " + str(self.time) + ", ")
            file.write("Memory (MB): " + str(self.memory) + "\n")

        # Write the path to the output file

        if self.goal != None:
            with open(fileName, "a") as file:
                file.write(str(self.goal.getPath()) + "\n")
        else:
            with open(fileName, "a") as file:
                file.write("No solution found\n")

