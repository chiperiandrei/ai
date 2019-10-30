# -----------table design--------
# c - computer sign
# p - player sign
# x - vacant sign ( no player is here )


# imports

import random

gameTable = []


def isFinalState(table):
    if table[0][0].__str__()[0] == table[0][1].__str__()[0] == table[0][2].__str__()[0] == table[0][3].__str__()[
        0] == 'p':
        return True
    if table[3][0].__str__()[0] == table[3][1].__str__()[0] == table[3][2].__str__()[0] == table[3][3].__str__()[
        0] == 'c':
        return True


def initDefaultTable():
    table = [
        ['c1', 'c2', 'c3', 'c4'],
        ['x', 'x', 'x', 'x'],
        ['x', 'x', 'x', 'x'],
        ['p1', 'p2', 'p3', 'p4']
    ]
    return table


def prettyPrintTable(table):
    s = [[str(e) for e in row] for row in table]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table1 = [fmt.format(*row) for row in s]
    print('\n'.join(table1))


def inMatrixAndIsNotOccupied(row, col, moveString, player):
    global gameTable
    return row >= 0 and row < 4 and col >= 0 and col < 4 and gameTable[int(moveString[0]) - 1][
        int(moveString[2]) - 1] != player[0].lower() + player[-1]


def isValidMove(currentposition, moveString, player):
    global gameTable
    dx = [-1, 0, 1, 1, 1, 0, -1]
    dy = [1, 1, 1, 0, -1, -1, -1]
    for i in range(0, 8):
        row = int(currentposition[0]) + dx[i]
        col = int(currentposition[0]) + dx[i]
        return inMatrixAndIsNotOccupied(row, col, moveString, player)


def doAMove(moveString, player):
    global gameTable
    lastPositioni = 0
    lastPositionj = 0
    for i in range(0, 4):
        for j in range(0, 4):
            if gameTable[i][j] == player[0].lower() + player[-1]:
                lastPositioni = i
                lastPositionj = j

    gameTable[lastPositioni][lastPositionj] = 'x'
    gameTable[int(moveString[0]) - 1][int(moveString[2]) - 1] = player[0].lower() + player[-1]


if __name__ == "__main__":
    gameTable = initDefaultTable()
    if gameTable == []:
        print("There is an error during the initialisation of game table!")
    else:
        print("Table has been initialised!")
        prettyPrintTable(gameTable)
    firstPlayer = random.choice(['c', 'p'])
    if firstPlayer == 'c':
        print("Computer is starting...")
    else:
        print("Player is starting...")
    playerName = 'Computer' if firstPlayer == 'c' else 'Player'
    ok = True
    currentMoves = {
        "p1": "30",
        "p2": "31",
        "p3": "32",
        "p4": "00",
        "c1": "33",
        "c2": "01",
        "c3": "02",
        "c4": "03"
    }
    while isFinalState(gameTable) != True or ok == True:
        ok = False
        if playerName == 'Player':
            y = input(playerName + ",choose your piece from 1 to 4 ")
            x = input(playerName + ", please insert move for piese #" + y + " ")
            if len(x) == 3:
                print(playerName + ", your move is " + x[0] + " " + x[2])
                if isValidMove(currentMoves[playerName[0].lower() + y], x, playerName + y):
                    doAMove(x, playerName + y)
                else:
                    print("Bad move! Try again!!")
                    y = input(playerName + ",choose your piece from 1 to 4 ")
                    x = input(playerName + ", please insert move for piese #" + y + " ")
                    if isValidMove(currentMoves[playerName[0].lower() + y], x, playerName + y):
                        doAMove(x, playerName + y)
                prettyPrintTable(gameTable)
                if playerName[0].lower() == 'c':
                    playerName = 'Player'
                else:
                    playerName = 'Computer'
        else:
            y = random.randint(1, 4)
            print(playerName + " has been choosen the piese #" + y.__str__())
            x = input(playerName + ", please insert move for piese #" + y.__str__() + " ")
            if len(x) == 3:
                print(playerName + ", your move is " + x[0] + " " + x[2])
                if isValidMove(currentMoves[playerName[0].lower() + y.__str__()], x, playerName + y.__str__()):
                    doAMove(x, playerName + y.__str__())
                else:
                    print("get another move")
                    x = input("da alta mutare")
                prettyPrintTable(gameTable)
                if playerName[0].lower() == 'c':
                    playerName = 'Player'
                else:
                    playerName = 'Computer'
