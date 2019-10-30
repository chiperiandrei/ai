# -----------table design--------
# c - computer sign
# p - player sign
# x - vacant sign ( no player is here )


# imports

import random

gameTable = []


def isFinalState(table):
    for i in range(0, 3):
        if table[0][i] != table[0][i + 1]:
            return False
        if table[3][i] != table[3][i + 1]:
            return False


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
    while True:
        y = input(playerName + ",choose your piece from 1 to 4 ")
        x = input(playerName + ", please insert move for piese #" + y + " ")
        if len(x) == 3:
            print(playerName + ", your move is " + x[0] + " " + x[2])
            doAMove(x, playerName + y)
            prettyPrintTable(gameTable)
            if playerName[0].lower() == 'c':
                playerName = 'Player'
            else:
                playerName = 'Computer'
