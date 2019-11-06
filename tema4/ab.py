def minimax(table, depth, alpha, beta, maximizingPlayer):
    possibleMoves = table.valid_moves()
    tableIsFinal = table.is_final()
    if depth == 0 or tableIsFinal:
		return table
    if maximizingPlayer:
        value = -100000
        column = random.choice(possibleMoves)
        for col in possibleMoves:
            move = table.computer_moves()
            new_score = minimax(move, depth - 1, alpha, beta, False)
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = 1000000
        column = random.choice(possibleMoves)
        for col in possibleMoves:
            move = table.computer_moves()
            new_score = minimax(move, depth - 1, alpha, beta, True)
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
