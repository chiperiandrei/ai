class NQueens:
    def __init__(self, noOfQueens):
        self.noOfQueens = noOfQueens
        self.noOfSolutions = 0
        self.solve()

    def solve(self):
        positions = [-1] * self.noOfQueens
        self.put_queen(positions, 0)
        print("Found", self.noOfSolutions, "solutions.")

    def put_queen(self, positions, row):
        if row == self.noOfQueens:
            self.prettyPrintMatrix(positions)
            self.showOnlyPositions(positions)
            self.noOfSolutions += 1
        else:
            for column in range(self.noOfQueens):
                if self.isValidPosition(positions, row, column):
                    positions[row] = column
                    self.put_queen(positions, row + 1)


    def isValidPosition(self, positions, busyRow, column):
        for i in range(busyRow):
            if positions[i] == column or \
                positions[i] - i == column - busyRow or \
                positions[i] + i == column + busyRow:

                return False
        return True

    def prettyPrintMatrix(self, positions):
        for row in range(self.noOfQueens):
            line = ""
            for column in range(self.noOfQueens):
                if positions[row] == column:
                    line += "Q "
                else:
                    line += ". "
            print(line)
        print("\n")

    def showOnlyPositions(self, positions):
        line = ""
        for i in range(self.noOfQueens):
            line += str(positions[i]+1) + " "
        print(line)

if __name__ == "__main__":
  x=int(input("no of queens"))
  NQueens(x)
