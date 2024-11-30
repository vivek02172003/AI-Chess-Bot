import chess
import time
import functools

# Define constants
MAX_DEPTH = 3  # Maximum depth for Iterative Deepening
TIME_LIMIT = 5.0  # Time limit in seconds for move computation
evaluation_count = 0

piece_values = {
        'p': -1, 'r': -5, 'n': -3, 'b': -3, 'q': -9, 'k': -100,
        'P': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 9, 'K': 100
    }
# Opening book (stub)
OPENING_BOOK = {
    # Opening moves for White
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1": "e7e5",  # King's Pawn Opening
    "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1": "e7e5",  # English Opening
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1": "c7c5",  # Sicilian Defense
    "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1": "g8f6",  # Queen's Pawn Opening

    # Italian Game (1. e4 e5 2. Nf3 Nc6 3. Bc4)
    "rnbqkbnr/pppppppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2": "g8f6",
    "rnbqkbnr/pppppppp/8/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 2 3": "b8c6",

    # Ruy-Lopez (1. e4 e5 2. Nf3 Nc6 3. Bb5)
    "rnbqkbnr/pppppppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2": "b8c6",
    "rnbqkbnr/pppppppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 2 3": "a7a6",

    # Sicilian Defense (1. e4 c5 2. Nf3)
    "rnbqkbnr/pppppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2": "d7d6",
    "rnbqkbnr/pp1ppppp/3q4/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 2 3": "g8f6",

    # French Defense (1. e4 e6)
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1": "e7e6",

    # Caro-Kann Defense (1. e4 c6)
    "rnbqkbnr/pp1ppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1": "d7d5",

    # Queen's Gambit (1. d4 d5 2. c4)
    "rnbqkbnr/pppppppp/8/3p4/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 1 2": "e7e6",

    # King's Indian Defense (1. d4 Nf6)
    "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1": "g8f6",

    # Slav Defense (1. d4 d5 2. c4 c6)
    "rnbqkbnr/pp1ppppp/8/3p4/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 1 2": "c7c6",
}


def get_opening_move(board):
    fen = board.fen()
    uci_move = OPENING_BOOK.get(fen, None)
    if uci_move:
        return chess.Move.from_uci(uci_move)
    return None

def evaluate_board(board):
    global evaluation_count
    evaluation_count += 1
    # Piece values (positive for White, negative for Black)
    

    # Development bonus weights
    development_bonus = {
        chess.KNIGHT: 0.5,
        chess.BISHOP: 0.5,
        chess.QUEEN: 0.2,
        chess.PAWN: 0.1
    }

    # Rook activity bonus
    rook_activity_bonus = 0.5  # Bonus for rooks on open/semi-open files

    # Center squares
    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]

    # Evaluation score
    score = 0

    # Helper function to check if a file is open or semi-open
    def is_open_or_semi_open_file(board, square):
        file_index = chess.square_file(square)
        file_squares = [chess.square(file_index, rank) for rank in range(8)]
        pawns = [s for s in file_squares if board.piece_type_at(s) == chess.PAWN]
        if len(pawns) == 0:  # Open file
            return True
        if len(pawns) == 1:  # Semi-open file
            return board.color_at(pawns[0]) != board.turn
        return False

    # Helper function to check if a piece is under attack
    def is_piece_under_attack(board, square, color):
        """Check if a piece at a given square is under attack."""
        return board.is_attacked_by(not color, square)

    # Iterate over all pieces on the board
    for square, piece in board.piece_map().items():
        piece_symbol = piece.symbol()

        # Material value
        score += piece_values.get(piece_symbol, 0)

        # Development bonus
        if piece.piece_type in development_bonus:
            rank = chess.square_rank(square)
            if piece.color:  # White pieces
                if rank != 0:  # Not on back rank
                    score += development_bonus[piece.piece_type]
            else:  # Black pieces
                if rank != 7:  # Not on back rank
                    score -= development_bonus[piece.piece_type]

        # Center control bonus
        if square in center_squares:
            if piece.color:  # White
                score += 0.5
            else:  # Black
                score -= 0.5

        # Rook activity bonus
        if piece.piece_type == chess.ROOK:
            if is_open_or_semi_open_file(board, square):
                if piece.color:  # White
                    score += rook_activity_bonus
                else:  # Black
                    score -= rook_activity_bonus

        # Piece safety: Penalize if the piece is under attack
        if is_piece_under_attack(board, square, piece.color):
            attacking_pieces = [board.piece_at(sq) for sq in board.attackers(not piece.color, square)]
            defending_pieces = [board.piece_at(sq) for sq in board.attackers(piece.color, square)]
            
            if attacking_pieces:
                attacking_value = sum(2 if p.piece_type == chess.KING else abs(piece_values[p.symbol()]) for p in attacking_pieces)
                defending_value = sum(2 if p.piece_type == chess.KING else abs(piece_values[p.symbol()]) for p in defending_pieces)
                piece_value = abs(piece_values[piece.symbol()])
                if piece.color:  # White piece under attack
                    if attacking_value > defending_value:
                        score -= 0.5 * piece_value  # Penalize if attackers are stronger
                    else:
                        score += 0.5 * piece_value  # Reward if defenders are stronger
                else:  # Black piece under attack
                    if attacking_value > defending_value:
                        score += 0.5 * piece_value  # Penalize if attackers are stronger
                    else:
                        score -= 0.5 * piece_value  # Reward if defenders are stronger


    # Check bonus (Add some bonus for check)
    if board.is_check():
        if board.turn:  # White's turn
            score += 1
        else:  # Black's turn
            score -= 1

    return score


def is_move_into_danger(board, move):
    # Make the move on a copy of the board
    board.push(move)
    danger = board.is_attacked_by(not board.turn, move.to_square)
    board.pop()
    return danger

def is_piece_under_attack(board, square, color):
    """Check if a piece at a given square is under attack."""
    return board.is_attacked_by(not color, square)

def order_moves(board, moves):
    def move_score(move, board):
        score = 0
        # Capture moves are more valuable
        if board.is_capture(move):
            captured_piece = board.piece_at(move.to_square)
            moving_piece = board.piece_at(move.from_square)
            if captured_piece and moving_piece:
                captured_value = abs(piece_values[captured_piece.symbol()])
                moving_value = abs(piece_values[moving_piece.symbol()])
                if moving_value < captured_value:
                    score += 10  # Prioritize capturing more valuable pieces
                # Check if the captured piece is defended
                if not list(board.attackers(captured_piece.color, move.to_square)):
                    score += 15  # Reward capturing free pieces
        

        # Giving check is more valuable
        if board.gives_check(move):
            score += 2
        
        # # Penalize moves that place pieces in danger
        if is_move_into_danger(board, move):
            score -= 40

        # Encourage central control (center is d4, e4, d5, e5)
        square = move.to_square
        if square in [chess.D4, chess.E4, chess.D5, chess.E5]:
            score += 3

        # Encourage piece development (move pieces towards the center)
        piece = board.piece_at(move.from_square)
        if piece.piece_type == chess.KNIGHT:
            # Knights are more valuable when they are closer to the center
            if square in [chess.D3, chess.E3, chess.D4, chess.E4, chess.D5, chess.E5]:
                score += 2
        elif piece.piece_type == chess.BISHOP:
            # Bishops are valuable when developed and controlling the center
            if square in [chess.D3, chess.E3, chess.D4, chess.E4, chess.D5, chess.E5]:
                score += 2

         # Check if a piece is under attack
        # Reward moves that avoid danger
        if is_piece_under_attack(board, move.from_square, board.turn):
            moving_piece = board.piece_at(move.from_square)
            attacking_pieces = [board.piece_at(sq) for sq in board.attackers(not board.turn, move.from_square)]
            if attacking_pieces:
                attacking_value = max(abs(piece_values[p.symbol()]) for p in attacking_pieces)
                moving_value = abs(piece_values[moving_piece.symbol()])
                if moving_value > attacking_value:
                    score += 20  # Reward for moving a more valuable piece out of danger
                elif moving_value == attacking_value:
                    score += 0  # No reward for moving a piece of equal value out of danger
                else:
                    score += 10  # Smaller reward for moving a less valuable piece out of danger

        # Penalize moves that place a piece under attack by a less valuable piece
        if is_piece_under_attack(board, move.to_square, board.turn):
            defending_piece = board.piece_at(move.from_square)
            attacking_pieces = [board.piece_at(sq) for sq in board.attackers(not board.turn, move.to_square)]
            if attacking_pieces:
                attacking_value = max(abs(piece_values[p.symbol()]) for p in attacking_pieces)
                defending_value = abs(piece_values[defending_piece.symbol()])
                if defending_value > attacking_value:
                    score -= 15  # Penalize for placing a more valuable piece under attack
                else:
                    score -= 5  # Smaller penalty for placing a less valuable piece under attack
        
        # Adjust score based on whose turn it is
        # if board.turn == chess.WHITE:
        #     score *= 1  # White prefers positive scores
        # else:
        #     score *= -1  # Black prefers negative scores (minimizing score)

        return score
    
    # Use functools.partial to pass the board to the move_score function
    return sorted(moves, key=functools.partial(move_score, board=board), reverse=True)

transposition_table = {}

def minimax(board, depth, alpha, beta, is_maximizing):
    board_fen = board.fen()  # Convert the board to its FEN string representation

    # Check if the position is already in the transposition table
    if board_fen in transposition_table:
        return transposition_table[board_fen]

    if depth == 0 or board.is_game_over():
        eval = evaluate_board(board)
        transposition_table[board_fen] = eval  # Store the result in the transposition table
        return eval

    legal_moves = order_moves(board, board.legal_moves)

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
        transposition_table[board_fen] = max_eval  # Store the result in the transposition table
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
        transposition_table[board_fen] = min_eval  # Store the result in the transposition table
        return min_eval

# Find best move using Iterative Deepening
def find_best_move(board, max_depth, time_limit):
    global evaluation_count
    evaluation_count = 0 
    opening_move = get_opening_move(board)
    if opening_move:
        return opening_move

    start_time = time.time()
    best_move = None
    
    # for depth in range(1, max_depth + 1):
    # print(f"Searching at depth {depth}")
    current_best_move = None
    best_value = float('inf')
    
    for move in order_moves(board, board.legal_moves):
        board.push(move)
        move_value = minimax(board, max_depth - 1, float('-inf'), float('inf'), False)
        board.pop()
        
        if move_value < best_value:
            best_value = move_value
            current_best_move = move
    
    # Update the best move found so far
    if current_best_move:
        best_move = current_best_move

    print("Evaluation count:", evaluation_count)
    return best_move
