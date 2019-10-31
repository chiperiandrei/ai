# -----------table design--------
# c - computer sign
# p - player sign
# x - vacant sign ( no player is here )


# imports

import random

gameTable = []
currentMoves={
"p1": "30",
"p2": "31",
"p3": "32",
"p4": "33",
"c1": "00",
"c2": "01",
"c3": "02",
"c4": "03"
}
winner='x'

def isFinalState(table):
    global winner
    if table[0][0].__str__()[0] == table[0][1].__str__()[0] == table[0][2].__str__()[0] == table[0][3].__str__()[0] == 'p':
      winner = 'p'
      return True
    if table[3][0].__str__()[0] == table[3][1].__str__()[0] == table[3][2].__str__()[0] == table[3][3].__str__()[0] == 'c':
        winner = 'c'
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


def isValidMove(currentposition, moveString, player):
  global gameTable
  if gameTable[int(moveString[0]) - 1][int(moveString[2]) - 1] != 'x':
    return False
  else:
    return True


def doAMove(moveString, player):
    global gameTable
    global currentMoves
    lastPositioni = 0
    lastPositionj = 0
    for i in range(0, 4):
        for j in range(0, 4):
            if gameTable[i][j] == player[0].lower() + player[-1]:
                lastPositioni = i
                lastPositionj = j

    gameTable[lastPositioni][lastPositionj] = 'x'
    gameTable[int(moveString[0]) - 1][int(moveString[2]) - 1] = player[0].lower() + player[-1]
    newI = int(moveString[0]) - 1
    newJ = int(moveString[2]) - 1
    currentMoves[player[0].lower() + player[-1]]=newI.__str__()+newJ.__str__()


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
    while isFinalState(gameTable) != True or ok == True:
        ok = False
        if playerName == 'Player':
          y = input(playerName + ",choose your piece from 1 to 4 ")
          flag =True
          while(flag==True):
            x = input(playerName + ", please insert move for piese #" + y + " ")
            if len(x) == 3:
              print(playerName + ", your move is " + x[0] + " " + x[2])
              if isValidMove(currentMoves[playerName[0].lower() + y], x, playerName + y):
                doAMove(x, playerName + y)
                flag=False
                prettyPrintTable(gameTable)
                print(currentMoves)
                if playerName[0].lower() == 'c':
                    playerName = 'Player'
                else:
                    playerName = 'Computer'
        else:
            y = random.randint(1, 4)
            flag =True
            while(flag==True):
              x = input(playerName + ", please insert move for piese #" + y.__str__() + " ")
              if len(x) == 3:
                print(playerName + ", your move is " + x[0] + " " + x[2])
                if isValidMove(currentMoves[playerName[0].lower() + y.__str__()], x, playerName + y.__str__()):
                  doAMove(x, playerName + y.__str__())
                  flag=False
                  prettyPrintTable(gameTable)
                  print(currentMoves)
                  if playerName[0].lower() == 'c':
                     playerName = 'Player'
                  else:
                      playerName = 'Computer'
    if winner =='c':
      winner='Computer'
    else:
      winner='Player'
    print("End game! " + winner + " wins!!")
         
