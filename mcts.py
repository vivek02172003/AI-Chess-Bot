import random
import chess

class MCTSNode:
    def __init__(self, board, parent=None):
        self.board = board.copy()
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def expand(self):
        legal_moves = list(self.board.legal_moves)
        for move in legal_moves:
            new_board = self.board.copy()
            new_board.push(move)
            self.children.append(MCTSNode(new_board, self))

    def simulate(self):
        board_copy = self.board.copy()
        while not board_copy.is_game_over():
            legal_moves = list(board_copy.legal_moves)
            move = random.choice(legal_moves)
            board_copy.push(move)
        result = board_copy.result()
        return 1 if result == "1-0" else -1

    def update(self, result):
        self.visits += 1
        self.wins += result

def mcts(board, iterations):
    root = MCTSNode(board)
    for _ in range(iterations):
        node = root
        # Selection
        while node.children and all(child.visits > 0 for child in node.children):
            node = max(node.children, key=lambda n: n.wins / n.visits + (2 * (2 * (n.visits ** 0.5)) / n.visits))
        
        # Expansion
        if not node.children:
            node.expand()
        
        # Simulation
        result = node.simulate()
        
        # Backpropagation
        while node is not None:
            node.update(result)
            node = node.parent

    # Choose the best move
    best_child = max(root.children, key=lambda c: c.visits)
    return best_child.board.peek()
