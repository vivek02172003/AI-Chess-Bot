import pygame
import chess
from chess_ai import find_best_move  # Import the AI function
from mcts import mcts
import random

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
            window.blit(piece_img, pygame.Rect(col * SQUARE_SIZE, (7 - row) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def main():
    clock = pygame.time.Clock()
    board = chess.Board()
    selected_square = None
    dragging_piece = None
    piece_offset_x, piece_offset_y = 0, 0
    
    # Main loop
    running = True
    while running:
        draw_board()
        draw_pieces(board)
        
        # Render dragging piece
        if dragging_piece:
            x, y = pygame.mouse.get_pos()
            window.blit(dragging_piece, (x - piece_offset_x, y - piece_offset_y))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Mouse click event - select piece
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // SQUARE_SIZE
                row = 7 - (y // SQUARE_SIZE)
                selected_square = chess.square(col, row)
                
                piece = board.piece_at(selected_square)
                if piece and piece.color == board.turn:
                    dragging_piece = PIECES[piece.symbol()]
                    piece_offset_x = x % SQUARE_SIZE
                    piece_offset_y = y % SQUARE_SIZE
            
            # Mouse release event - drop piece
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_piece:
                    x, y = event.pos
                    col = x // SQUARE_SIZE
                    row = 7 - (y // SQUARE_SIZE)
                    target_square = chess.square(col, row)
                    
                    # Attempt to make the move
                    move = chess.Move(selected_square, target_square)
                    if move in board.legal_moves:
                        board.push(move)
                        selected_square = None
                        dragging_piece = None
                        
                        # Check if the game is over after the move
                        if board.is_game_over():
                            print("Game over!")
                            running = False
                            break
                        
                        # AI move
                        if board.turn == chess.BLACK:
                            best_move = mcts(board, 25)
                            if best_move:
                                board.push(best_move)
                    
                    else:
                        print("Invalid move")  # Show invalid move message
                    dragging_piece = None
        
        # Delay for consistent frame rendering
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
