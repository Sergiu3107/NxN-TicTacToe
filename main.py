import sys
import pygame
import numpy as np
import time

pygame.init()

# Colors definition for the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (180, 180, 180)

# Game Configuration
WIDTH = 600  # Width of the game window
HEIGHT = 600  # Height of the game window
LINE_WIDTH = 3  # Thickness of the grid lines
DEPTH_LIMIT = 100  # Depth limit for AI search
CELL_SIZE = None  # Size of each cell in the grid (calculated later)
CIRCLE_RADIUS = None  # Radius of the circle used by player 1
CIRCLE_WIDTH = 5  # Width of the circle border
CROSS_WIDTH = 10  # Width of the cross border for AI player

# Time Control for AI move calculation
TIME_LIMIT = 0.01  # Time limit in seconds for each AI move


class TicTacToe:
    """
    Class representing the game logic for TicTacToe.
    Handles game state, win conditions, and move marking.
    """

    def __init__(self, grid_size, win_condition):
        """
        Initializes the TicTacToe game with a given grid size and win condition.

        Parameters:
        grid_size (int): Size of the grid (3x3, 4x4, etc.)
        win_condition (int): Number of consecutive marks needed to win (e.g., 3 in a row).
        """
        global CELL_SIZE, CIRCLE_RADIUS
        self.grid_size = grid_size  # Board grid size (3x3, 4x4, etc.)
        self.win_condition = win_condition  # Number of consecutive marks to win
        self.board = np.zeros((grid_size, grid_size))  # Initialize empty board
        self.current_player = 1  # Player 1 starts the game
        CELL_SIZE = WIDTH // grid_size  # Calculate size of each cell
        CIRCLE_RADIUS = CELL_SIZE // 3  # Calculate circle radius for player 1's mark

    def mark_cell(self, row, col, player):
        """
        Marks a cell with the specified player's mark.

        Parameters:
        row (int): Row index of the cell
        col (int): Column index of the cell
        player (int): 1 for Player 1, -1 for AI
        """
        self.board[row][col] = player

    def available_cell(self, row, col):
        """
        Checks if a cell is available to be marked.

        Parameters:
        row (int): Row index of the cell
        col (int): Column index of the cell

        Returns:
        bool: True if the cell is available (empty), False otherwise
        """
        return self.board[row][col] == 0

    def is_board_full(self):
        """
        Checks if the board is full (i.e., no empty cells left).

        Returns:
        bool: True if the board is full, False otherwise
        """
        return not np.any(self.board == 0)

    def check_win(self, player):
        """
        Checks if a player has won the game.

        Parameters:
        player (int): The player to check for win (1 for Player 1, -1 for AI)

        Returns:
        bool: True if the player has won, False otherwise
        """
        # Check rows and columns
        for row in range(self.grid_size):
            for col in range(self.grid_size - self.win_condition + 1):
                if all(self.board[row][col + i] == player for i in range(self.win_condition)):
                    return True

        for col in range(self.grid_size):
            for row in range(self.grid_size - self.win_condition + 1):
                if all(self.board[row + i][col] == player for i in range(self.win_condition)):
                    return True

        # Check diagonals
        for row in range(self.grid_size - self.win_condition + 1):
            for col in range(self.grid_size - self.win_condition + 1):
                if all(self.board[row + i][col + i] == player for i in range(self.win_condition)):
                    return True

        for row in range(self.grid_size - self.win_condition + 1):
            for col in range(self.win_condition - 1, self.grid_size):
                if all(self.board[row + i][col - i] == player for i in range(self.win_condition)):
                    return True

        return False


class AIPlayer:
    """
    Class representing the AI logic for playing TicTacToe.
    Uses Alpha-Beta pruning for decision-making and iterative deepening.
    """

    def __init__(self, game):
        """
        Initializes the AI player with a reference to the game.

        Parameters:
        game (TicTacToe): The game instance
        """
        self.game = game
        self.transposition_table = {}  # For memoization (not used in current version)
        self.history_table = {}  # Keeps track of the moves explored
        self.node_count = 0  # Keeps track of the number of nodes evaluated during search

    def find_immediate_win_or_block(self, player):
        """
        Checks if the AI or player can win or block an immediate winning move.

        Parameters:
        player (int): The player to check for immediate win or block (1 for Player 1, -1 for AI)

        Returns:
        tuple: (row, col) of the winning or blocking move, or None if no such move exists
        """
        for row in range(self.game.grid_size):
            for col in range(self.game.grid_size):
                if self.game.available_cell(row, col):
                    self.game.mark_cell(row, col, player)
                    if self.game.check_win(player):
                        self.game.mark_cell(row, col, 0)  # Undo the move
                        return (row, col)
                    self.game.mark_cell(row, col, 0)  # Undo the move
        return None

    def evaluate_line(self, line):
        """
        Evaluates a line (row, column, or diagonal) for scoring.

        Parameters:
        line (numpy array): The line (row, column, or diagonal) to evaluate

        Returns:
        int: A score based on the line's composition (positive, negative, or neutral)
        """
        player_count = np.sum(line == 1)
        ai_count = np.sum(line == -1)
        if player_count > 0 and ai_count > 0:
            return 0  # Mixed line (no advantage)
        elif player_count > 0:
            return -10 ** player_count  # Player advantage
        elif ai_count > 0:
            return 10 ** ai_count  # AI advantage
        return 0

    def evaluate_board(self):
        """
        Evaluates the entire board to calculate a score for the AI.

        Returns:
        int: The total score based on the current state of the board
        """

        def evaluate_subsequences(line):
            """
            Helper function to evaluate multiple subsequences (of length `win_condition`) within a line.
            """
            score = 0
            for i in range(len(line) - self.game.win_condition + 1):
                subsequence = line[i:i + self.game.win_condition]
                score += self.evaluate_line(subsequence)
            return score

        score = 0
        # Evaluate rows
        for row in self.game.board:
            score += evaluate_subsequences(row)
        # Evaluate columns
        for col in self.game.board.T:
            score += evaluate_subsequences(col)
        # Evaluate diagonals
        for offset in range(-self.game.grid_size + 1, self.game.grid_size):
            score += evaluate_subsequences(np.diag(self.game.board, k=offset))
            score += evaluate_subsequences(np.diag(np.fliplr(self.game.board), k=offset))
        return score

    def iterative_deepening(self, depth_limit):
        """
        Performs iterative deepening search to select the best move for the AI.

        Parameters:
        depth_limit (int): The maximum depth to search

        Returns:
        tuple: Best move (row, col) for the AI
        """
        best_move = None
        start_time = time.time()
        depth_node_counts = {}  # Track nodes explored at each depth

        for depth in range(1, depth_limit + 1):
            self.node_count = 0  # Reset node count for each depth
            score, move = self.alpha_beta(self.game.board, depth, -float('inf'), float('inf'), True, start_time)
            depth_node_counts[depth] = self.node_count  # Store node count for this depth

            if move:
                best_move = move
            if time.time() - start_time > TIME_LIMIT:
                break  # Stop if the time limit is reached

        # Print depth-wise node counts for performance analysis
        print("Depth-wise node exploration:")
        for d, count in depth_node_counts.items():
            print(f"Depth {d}: {count} nodes")

        return best_move

    def alpha_beta(self, state, depth, alpha, beta, is_maximizing, start_time):
        """
        Implements the Alpha-Beta pruning algorithm for optimized minimax search.

        Parameters:
        state (numpy array): The current game state (board)
        depth (int): The remaining depth to search
        alpha (float): Best score for the maximizing player
        beta (float): Best score for the minimizing player
        is_maximizing (bool): Whether the current player is maximizing or minimizing
        start_time (float): The start time of the search for time control

        Returns:
        tuple: The best score and corresponding move (row, col)
        """
        self.node_count += 1

        # Check for timeout based on the time limit
        if time.time() - start_time > TIME_LIMIT:
            return 0, None  # Timeout condition

        # Terminal conditions (win or board full)
        if self.game.check_win(-1):
            return float('inf'), None  # AI wins
        if self.game.check_win(1):
            return float('-inf'), None  # Player wins
        if self.game.is_board_full() or depth == 0:
            return self.evaluate_board(), None  # Draw or depth limit reached

        best_move = None
        moves = [(row, col) for row in range(self.game.grid_size) for col in range(self.game.grid_size) if
                 self.game.available_cell(row, col)]
        # Sort moves by history table to prioritize previously explored moves
        moves.sort(key=lambda move: self.history_table.get(move, 0), reverse=True)

        if is_maximizing:
            best_score = -float('inf')
            for row, col in moves:
                state[row, col] = -1  # AI move
                score, _ = self.alpha_beta(state, depth - 1, alpha, beta, False, start_time)
                state[row, col] = 0  # Undo move
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
                alpha = max(alpha, best_score)
                if beta <= alpha:  # Alpha-Beta Pruning
                    break
        else:
            best_score = float('inf')
            for row, col in moves:
                state[row, col] = 1  # Player 1 move
                score, _ = self.alpha_beta(state, depth - 1, alpha, beta, True, start_time)
                state[row, col] = 0  # Undo move
                if score < best_score:
                    best_score = score
                    best_move = (row, col)
                beta = min(beta, best_score)
                if beta <= alpha:  # Alpha-Beta Pruning
                    break

        return best_score, best_move

    def make_move(self):
        """
        Makes a move for the AI player using the evaluation function and iterative deepening search.
        """
        self.node_count = 0
        start_time = time.time()

        # Check if the AI has an immediate winning move
        win_move = self.find_immediate_win_or_block(-1)
        if win_move:
            self.game.mark_cell(win_move[0], win_move[1], -1)
            print(f"AI found immediate win in {time.time() - start_time:.4f} sec")
            return

        # Check if the AI needs to block the player
        block_move = self.find_immediate_win_or_block(1)
        if block_move:
            self.game.mark_cell(block_move[0], block_move[1], -1)
            print(f"AI blocked in {time.time() - start_time:.4f} sec")
            return

        # Perform search using iterative deepening to find the best move
        move = self.iterative_deepening(DEPTH_LIMIT)
        print(f"Nodes explored: {self.node_count}")

        if move:
            self.game.mark_cell(move[0], move[1], -1)  # AI move

        print(f"AI move took {time.time() - start_time:.4f} sec")
        print("---------------------------\n")


class Renderer:
    """
    Class responsible for rendering the game state (board and moves) using Pygame.
    """

    def __init__(self, screen, game):
        """
        Initializes the renderer with a Pygame screen and a game instance.

        Parameters:
        screen (pygame.Surface): The Pygame window where everything is drawn
        game (TicTacToe): The TicTacToe game instance to be rendered
        """
        self.screen = screen
        self.game = game

    def draw_lines(self, color=WHITE):
        """
        Draws the grid lines for the game board.

        Parameters:
        color (tuple): The color of the grid lines (default is WHITE)
        """
        for i in range(1, self.game.grid_size):
            pygame.draw.line(self.screen, color, (0, CELL_SIZE * i), (WIDTH, CELL_SIZE * i), LINE_WIDTH)
            pygame.draw.line(self.screen, color, (CELL_SIZE * i, 0), (CELL_SIZE * i, HEIGHT), LINE_WIDTH)

    def draw_figures(self, color=WHITE):
        """
        Draws the figures (crosses and circles) on the board.

        Parameters:
        color (tuple): The color of the figures (default is WHITE)
        """
        for row in range(self.game.grid_size):
            for col in range(self.game.grid_size):
                if self.game.board[row][col] == 1:
                    # Draw circle for Player 1
                    pygame.draw.circle(self.screen, color,
                                       (int(col * CELL_SIZE + CELL_SIZE // 2), int(row * CELL_SIZE + CELL_SIZE // 2)),
                                       CIRCLE_RADIUS, CIRCLE_WIDTH)
                elif self.game.board[row][col] == -1:
                    # Draw cross for AI
                    pygame.draw.line(self.screen, color,
                                     (col * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 4),
                                     (col * CELL_SIZE + 3 * CELL_SIZE // 4, row * CELL_SIZE + 3 * CELL_SIZE // 4),
                                     CROSS_WIDTH)
                    pygame.draw.line(self.screen, color,
                                     (col * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + 3 * CELL_SIZE // 4),
                                     (col * CELL_SIZE + 3 * CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 4),
                                     CROSS_WIDTH)


class Game:
    """
    The main game class that manages the game loop, player inputs, and AI moves.
    """

    def __init__(self):
        """
        Initializes the game with user-defined grid size and win condition.
        Also sets up the Pygame window and initializes the Renderer and AI player.
        """
        grid_size = int(input("Choose grid size: "))
        win_condition = int(input("Choose win condition: "))

        self.game = TicTacToe(grid_size, win_condition)  # Initialize the game logic
        self.ai = AIPlayer(self.game)  # Initialize the AI player
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Pygame window
        self.renderer = Renderer(self.screen, self.game)  # Renderer for drawing the game board
        pygame.display.set_caption('Tic Tac Toe')  # Set window caption
        self.screen.fill(BLACK)  # Fill the screen with black initially

    def run(self):
        """
        Main game loop. Handles user input, AI moves, and renders the game state.
        """
        self.renderer.draw_lines()  # Draw the grid lines
        game_over = False  # Flag to track if the game is over

        while True:
            # Handle user events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()  # Quit the game

                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    # Player makes a move
                    mouse_x = event.pos[0] // CELL_SIZE
                    mouse_y = event.pos[1] // CELL_SIZE
                    if self.game.available_cell(mouse_y, mouse_x):
                        self.game.mark_cell(mouse_y, mouse_x, 1)  # Player 1 moves
                        if self.game.check_win(1):  # Check if Player 1 wins
                            game_over = True
                        else:
                            self.ai.make_move()  # AI makes a move
                            if self.game.check_win(-1):  # Check if AI wins
                                game_over = True

                        if self.game.is_board_full() and not game_over:
                            game_over = True  # Draw condition if board is full

            # Draw the updated game state (board and moves)
            if not game_over:
                self.renderer.draw_figures()  # Draw figures (crosses/circles)
            else:
                # Draw the final state (green for Player 1 win, red for AI win, gray for draw)
                self.renderer.draw_figures(
                    GREEN if self.game.check_win(1) else RED if self.game.check_win(-1) else GRAY)
                self.renderer.draw_lines(GREEN if self.game.check_win(1) else RED if self.game.check_win(-1) else GRAY)

            pygame.display.update()  # Update the Pygame display


# Main entry point
if __name__ == "__main__":
    Game().run()  # Start the game loop
