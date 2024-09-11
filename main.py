import pygame
import chess

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 640, 640  # Size of the window
BOARD_SIZE = 8  # Chessboard is 8x8
SQUARE_SIZE = WIDTH // BOARD_SIZE  # Size of each square on the board

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
    PIECES[symbol] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))  # Scale the image to fit the square

# Set up display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Function to draw the chessboard
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(window, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to draw the pieces on the board
def draw_pieces(board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_img = PIECES[piece.symbol()]
            row = chess.square_rank(square)
            col = chess.square_file(square)
            window.blit(piece_img, pygame.Rect(col * SQUARE_SIZE, (7-row) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to get user input for moves in CLI
def get_move():
    move = input("Enter your move (e.g., e2 e4): ").strip()
    move = move.replace(" ", "")  # Remove spaces
    try:
        chess_move = chess.Move.from_uci(move)
        return chess_move
    except:
        print("Invalid move format. Use standard algebraic notation (e.g., e2e4).")
        return None

def main():
    clock = pygame.time.Clock()
    board = chess.Board()

    # Main loop
    running = True
    while running:
        draw_board()
        draw_pieces(board)
        pygame.display.flip()

        # Handle Pygame events (e.g., quitting the game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get and execute user move from the CLI
        if not board.is_game_over():
            move = get_move()
            if move and move in board.legal_moves:
                board.push(move)
            else:
                print("Illegal move or invalid input.")
        
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
