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

# Load piece images
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
    PIECES[symbol] = pygame.image.load(f'pieces-basic-png/{name}.PNG')

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

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
