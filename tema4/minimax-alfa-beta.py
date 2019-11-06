def minimax(table, depth, alpha, beta, maximizingPlayer):
    possibleMoves = table.valid_moves()
    tableIsFinal = table.is_final()
    if depth == 0 or tableIsFinal:
        if tableIsFinal: # final table
            if game_won(table) and not is_computer_turn(table):
                return (None, 100000)
            elif game_won(table) and is_computer_turn(table):
                return (None, -100000)
            else:
                return (None, 0)
        else:  # leaf 
            return (None, score(table, -1))
    if maximizingPlayer:
        value = -100000
        column = random.choice(possibleMoves)
        for col in possibleMoves:
            move = table.computer_moves()
            new_score = minimax(move, depth - 1, alpha, beta, False)[1]
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
            new_score = minimax(move, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
