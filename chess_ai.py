import chess

# Define constants
MAX_DEPTH = 3  # Depth of the search tree

def evaluate_board(board):
    # Simple evaluation: material count
    piece_values = {
        'p': -1, 'r': -5, 'n': -3, 'b': -3, 'q': -9, 'k': -100,
        'P': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 9, 'K': 100
    }
    score = 0
    for piece in board.piece_map().values():
        score += piece_values.get(piece.symbol(), 0)
    return score

def minimax(board, depth, alpha, beta, is_maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    
    legal_moves = list(board.legal_moves)
    
    if is_maximizing:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, depth):
    best_move = None
    best_value = float('-inf')
    
    for move in board.legal_moves:
        board.push(move)
        move_value = minimax(board, depth - 1, float('-inf'), float('inf'), False)
        board.pop()
        
        if move_value > best_value:
            best_value = move_value
            best_move = move
    
    return best_move
