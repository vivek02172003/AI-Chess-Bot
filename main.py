import pygame
import chess
from chess_ai import find_best_move  # Import the AI function

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 640, 640
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)

# Load piece images and scale them
PIECES = {}
piece_names = {
    'p': 'black-pawn',
    'r': 'black-rook',
    'n': 'black-knight',
    'b': 'black-bishop',
    'q': 'black-queen',
    'k': 'black-king',
    'P': 'white-pawn',
    'R': 'white-rook',
    'N': 'white-knight',
    'B': 'white-bishop',
    'Q': 'white-queen',
    'K': 'white-king'
}

for symbol, name in piece_names.items():
    image = pygame.image.load(f'pieces-basic-png/{name}.PNG')
    PIECES[symbol] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

# Set up display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(window, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_img = PIECES[piece.symbol()]
            row = chess.square_rank(square)
            col = chess.square_file(square)
            window.blit(piece_img, pygame.Rect(col * SQUARE_SIZE, (7-row) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def main():
    clock = pygame.time.Clock()
    board = chess.Board()
    
    # Main loop
    running = True
    while running:
        draw_board()
        draw_pieces(board)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle user move via CLI
        if board.turn == chess.WHITE:  # Assuming user plays white
            print(board)
            move_input = input("Enter your move (e.g., e2e4): ")
            if move_input:
                try:
                    move = chess.Move.from_uci(move_input)
                    if move in board.legal_moves:
                        board.push(move)
                    else:
                        print("Invalid move")
                        continue  # Skip AI move if invalid user move
                except ValueError:
                    print("Invalid move format")
                    continue  # Skip AI move if move format is invalid

            # After the user makes a valid move, check if the game is over
            if board.is_game_over():
                print("Game over!")
                break
            
            # AI move after user's move
            if not board.is_game_over() and board.turn == chess.BLACK:
                best_move = find_best_move(board, 3)
                if best_move:
                    board.push(best_move)

            # Print the board after AI makes a move
            print(board)

        # Delay to ensure frame rendering consistency
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
