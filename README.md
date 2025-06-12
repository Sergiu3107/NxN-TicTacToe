
# Tic-Tac-Toe

## General Project Description

This project implements an interactive Tic-Tac-Toe game with a powerful AI algorithm using Python and Pygame. The AI uses a combination of advanced search techniques to make optimal decisions, including **Alpha-Beta Pruning**, **Iterative Deepening**, and **History Heuristic**. The project allows the player to compete against the AI on a customizable board with a variable win condition.

The **AI algorithm** aims to play optimally by evaluating every possible game state using an **evaluation function** that assigns a score to each board configuration. Additionally, the AI uses optimization techniques such as a **Transposition Table** to save computation time by avoiding the re-evaluation of previously seen states.

## Explanation of Algorithms Used and Their Motivation

### 1. **Alpha-Beta Pruning**

**Alpha-Beta Pruning** is an optimization of the **Minimax** algorithm that significantly reduces the number of nodes evaluated in the decision tree. By evaluating deep possibilities, Alpha-Beta Pruning allows the algorithm to "prune" branches that won’t affect the final outcome, saving both time and computing resources. This is the primary technique used to determine the best move and reduce the search complexity.

In games with many possible moves and states, minimizing the number of nodes is essential to ensure the AI performs efficiently within a reasonable time frame.

### 2. **Iterative Deepening**

**Iterative Deepening** is a hybrid technique between **Depth-First Search (DFS)** and **Breadth-First Search (BFS)** that combines the benefits of both by incrementally increasing the depth of search over time. The idea is that the AI begins searching at a shallow depth (e.g., depth 1) and gradually increases the depth limit until a maximum depth or time limit is reached.

In our implementation, **Iterative Deepening** helps the AI make decisions within a limited time window. Instead of diving too deep and getting stuck searching for a perfect move, it evaluates moves incrementally at increasing depths.

1.  **Start with shallow depth**: The algorithm begins with depth 1 (evaluating only the immediate player and AI moves).
    
2.  **Increment depth**: After each iteration, the search depth is increased by 1 (depth 2, depth 3, etc.).
    
3.  **Best move based on progress so far**: If the time limit is exceeded, the AI returns the best move found up to that point.
    

Implementation-wise, the `iterative_deepening` function repeatedly calls the `alpha_beta` function, increasing the depth on each iteration until the predefined `TIME_LIMIT` is exceeded.

```py
def  iterative_deepening(self, depth_limit):
    best_move = None 
    start_time = time.time() 
    for depth in  range(1, depth_limit + 1):
        self.node_count = 0 score, move = self.alpha_beta(self.game.board, depth, -float('inf'), float('inf'), True, start_time) 

		if time.time() - start_time > TIME_LIMIT: 
			break 		
		best_move = move 
	return best_move
```

### 3. **History Heuristic**

**History Heuristic** is a technique used to improve search efficiency by ordering moves based on how frequently they have influenced past decisions. This prioritization accelerates the search by focusing on moves that were previously found to be impactful.

In each iteration of `alpha_beta`, available moves are sorted using a `history_table`, which tracks how often specific moves were explored. Moves that were more frequently involved in beneficial outcomes are evaluated first.

```py
moves.sort(key=lambda move: self.history_table.get(move, 0), reverse=True)
```
With this approach, the algorithm becomes more efficient over time, as it "learns" which moves tend to be more promising and prioritizes them in future iterations.

### 4. **Transposition Table**

A **Transposition Table** is a data structure used to store previously evaluated game states. A transposition refers to the same game state reached through different move sequences. Using a transposition table helps avoid redundant calculations.

Within the `alpha_beta` function, before evaluating a state, the algorithm checks whether the state has already been evaluated using `transposition_table`. If so, it reuses the stored result, saving time and computation.

The table is a dictionary where the key is a unique representation of the board state, and the value is the evaluated score for that state.


```py
if state_str in self.transposition_table: 
	return self.transposition_table[state_str]
```

After evaluating a state, its result is stored in the table for future reuse.

### 5. **Evaluation Function**

The evaluation function is responsible for assigning a score to each game state, helping the AI determine if a state is favorable. Scores can be positive (AI advantage), negative (player advantage), or zero (neutral). The function analyzes all board lines (rows, columns, and diagonals) and assigns a score based on the number of consecutive symbols for each player.

In our implementation, the evaluation function scans every line and assigns values based on the number of player or AI symbols. For example, a line with two AI symbols and an empty cell receives a positive score, while a similar line with player symbols receives a negative score.

```py
def  evaluate_line(self, line):
    player_count = np.sum(line == 1)
    ai_count = np.sum(line == -1) 
    if player_count > 0  and ai_count > 0: 
	    return  0  # Mixed line (no advantage)  
	elif player_count > 0: 
	    return -10 ** player_count # Player advantage  
	elif ai_count > 0: 
		return  10 ** ai_count # AI advantage 
	return  0
```

The evaluation function is essential for making intelligent decisions and optimizing AI performance, as it determines the importance of each potential move.

## Test Results (Algorithm Performance)

We conducted tests using different board sizes and win conditions to evaluate the AI’s performance:

-   **3x3 boards** with a win condition of 3: The AI performs efficiently using Alpha-Beta Pruning and Iterative Deepening, taking around 0.01 seconds per move depending on game complexity.
    
-   **5x5 boards** with a win condition of 4: Performance slightly decreases, but the AI still finds good moves in about 0.1–0.2 seconds, thanks to optimizations like the Transposition Table and History Heuristic.
    

Overall, the algorithm works efficiently even for larger boards like **15x15** with a win condition of 5. In such cases, move selection time increases due to the growing complexity of the decision tree. Still, the AI remains competitive and playable even on large-scale boards, though performance naturally decreases slightly.

## How to Run the Code

### Prerequisites:

1.  Make sure you have **Python 3.x** installed on your system.
    
2.  Install the **Pygame** library using pip:
    

```py
pip install pygame
pip install numpy
```

### Running the Game:

1.  Download or clone the repository to your local machine.
    
2.  Open your terminal or command prompt and navigate to the project directory.
    
3.  Run the main script using:
    
```
python main.py
```

4.  At the beginning of the game, you will be prompted to choose:
    
    -   **Board size** (e.g., 3 for 3x3, 4 for 4x4, etc.)
        
    -   **Win condition** (number of consecutive symbols needed to win, usually 3)
        
5.  Once these options are selected, the game will start automatically. The player interacts using the mouse, while the AI makes its moves based on the implemented algorithm.
    
6.  The game continues until a player wins or the board is full. In case of a victory, either the player or AI will be declared the winner and the game will end.
    

### Controls:

-   The **player** uses the **mouse** to place symbols on the board.
    
-   The **AI** moves automatically based on the logic implemented in the AI algorithms.
    


## References

- [Minimax Algorithm – Wikipedia](https://en.wikipedia.org/wiki/Minimax)
- [Alpha-Beta Pruning – Wikipedia](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)

- [How to Build a Tic-Tac-Toe AI in Python – Real Python](https://realpython.com/python-tic-tac-toe/)
- [How to Play Tic-Tac-Toe on a 5x5 Grid – StackExchange](https://boardgames.stackexchange.com/questions/41410/how-to-play-tic-tac-toe-on-a-5x5-grid)

- [Pygame Documentation](https://www.pygame.org/docs/)

- [Best Algorithm for 5x5 Tic-Tac-Toe AI Using 4 in a Row – StackOverflow](https://stackoverflow.com/questions/41135751/best-algorithm-for-5x5-tictactoe-ai-using-4-in-a-row)

- [Iterative Deepening Depth-First Search (IDDFS) – GeeksforGeeks](https://www.geeksforgeeks.org/iterative-deepening-searchids-iterative-deepening-depth-first-searchids/)
- [AI Game Playing: Iterative Deepening and Time-Limited Search – University of Edinburgh](https://www.inf.ed.ac.uk/teaching/courses/ai/notes/lecture10.pdf)

- [History Heuristic for Move Ordering – Chess Programming Wiki](https://www.chessprogramming.org/History_Heuristic)
- [Move Ordering Techniques in Game Tree Search – University of Alberta](https://webdocs.cs.ualberta.ca/~mmueller/ps/moveordering.pdf)

- [Transposition Tables in Game-Tree Search – Chess Programming Wiki](https://www.chessprogramming.org/Transposition_Table)
- [Optimizing Game Tree Search with Transposition Tables – StackOverflow](https://stackoverflow.com/questions/20523756/transposition-table-in-minimax-algorithm)

- [Designing Evaluation Functions in Board Games – Stanford University](http://web.stanford.edu/class/cs221/lectures/lecture16.pdf)
- [How to Write an Evaluation Function for Games – Loyola Marymount University](http://cs.lmu.edu/~ray/notes/evalfunctions/)
