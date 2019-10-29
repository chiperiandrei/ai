#-----------table design--------
#c - computer sign
#p - player sign
#x - vacant sign ( no player is here ) 


#imports

import random


gameTable = []

def isFinalState(table):
	for i in range(0,3):
		if table[0][i] != table[0][i+1]:
			return False
			
def initDefaultTable():
	table = [
		['c','c','c','c'],
		['x','x','x','x'],
		['x','x','x','x'],
		['p','p','p','p']
	]
	return table
def prettyPrintTable(table):
	s = [[str(e) for e in row] for row in table]
	lens = [max(map(len, col)) for col in zip(*s)]
	fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
	table1 = [fmt.format(*row) for row in s]
	print ('\n'.join(table1))
if __name__ == "__main__":
	gameTable = initDefaultTable()
	if gameTable == []:
		print("There is an error during the initialisation of game table!")
	else:
		print("Table has been initialised!")
		prettyPrintTable(gameTable)
	firstPlayer = random.choice(['c','p'])
	if firstPlayer == 'c':
		print("Computer is starting...")
	else:
		print("Player is starting...")
	playerName = 'Computer' if firstPlayer == 'c' else 'Player'
	while True:
		x=input("Insert move for " + playerName)
		if len(x) == 3:
			print(playerName + ", your move is " + x[0] +" "+ x[2])
			if playerName[0].lower()=='c':
				playerName = 'Player'
			else:
				playerName = 'Computer'
