import random
import copy


class Tictactoe:
    player1_symbol = "X"  # X Default player 1
    player2_symbol = "O"  # O Default player 2

    def __init__(self):
        # Load defaults. None for empty board. No winner. Player 1 default is human
        self.board = [[None for _ in range(0, 3)] for _ in range(0, 3)]
        self.winner, self.human_symbol, self.ai_symbol = None, "X", "O"
        self.player_turn, self.human_turn = 1, 1

    def run(self):
        self.draw()
        self.player_select()

        # Continue while no winner
        while self.winner is None:
            self.play()
            self.draw()
            self.winner = self.check_winner(self.board)
            self.player_turn = self.player_turn % 2 + 1

        # Game Over. Prints game result
        if self.winner == "Draw":
            print("Game is Draw")
        elif self.winner is self.player1_symbol:
            print("Player 1 - X wins")
        else:
            print("Player 2 - O wins")

    def player_select(self):
        while True:
            try:
                ans = int(input("Select if player 1 or 2:"))
                if ans in [1, 2]:
                    self.human_turn = ans
                    def f(x): return "O" if (x == 2) else "X"   # Returns "O" if 2 and "X" for 1
                    self.human_symbol = f(ans)
                    self.ai_symbol = f(ans + 1)
                    break
                else:
                    print('Please select "1" or "2" only!')
            except ValueError:
                print("Invalid input")

    def play(self):
        if self.player_turn == self.human_turn:     # Calls Human.move if player's turn
            move = Human.move(self.check_available_moves(self.board))

            # Uncomment for AI vs AI mode
            # move = SmartPlayer.move(self.board, self.check_available_moves(self.board), self.human_symbol,self.player_turn)
        else:                                       # Calls for an opponent
            # Uncomment for p2p mode
            # move = Human.move(self.check_available_moves(self.board))

            # Uncomment for Opponent that moves randomly
            # move = RandomPlayer.move(self.check_available_moves(self.board))

            # Calls for a smart player (AI) that utilizes minimax algorithm
            move = SmartPlayer.move(self.board, self.check_available_moves(self.board), self.ai_symbol, self.player_turn)

        # Update board based on move returned by player (Human/AI)
        self.board = self.update_board(move, self.board, self.player_turn)

    @staticmethod
    def check_winner(board):
        # Check columns
        for i in range(0, 3):
            col = [row[i] for row in board]
            if all((col[0] == element) and (element is not None) for element in col):
                return col[0]

        # Check rows
        for row in board:
            if all((row[0] == element) and (element is not None) for element in row):
                return row[0]

        # Check diagonal
        diagonal = [board[i][i] for i in range(len(board))]
        if all((diagonal[0] == element) and (element is not None) for element in diagonal):
            return diagonal[0]

        # Check anti-diagonal
        anti_diagonal = [board[i][-i - 1] for i in range(len(board))]
        if all((anti_diagonal[0] == element) and (element is not None) for element in anti_diagonal):
            return anti_diagonal[0]

        # Check if no None
        if len(Tictactoe.check_available_moves(board)) == 0:
            return "Draw"

        return None

    @staticmethod
    def check_available_moves(board):
        # Check available moves by returning index of empty squares (containing None)
        return [(row_ix, col_ix) for row_ix, row in enumerate(board) for col_ix, col in enumerate(row) if col is None]

    @staticmethod
    def update_board(move, old_board, player_turn):
        # Deep copy board to create a different object each time. For minimax simulation.
        new_board = copy.deepcopy(old_board)
        if player_turn == 1:
            new_board[move[0]][move[1]] = Tictactoe.player1_symbol  # None to "X"
        else:  # player_turn == 2 "O"
            new_board[move[0]][move[1]] = Tictactoe.player2_symbol  # None to "O"

        return new_board

    def draw(self):
        # Draw board for GUI simulation
        for row in self.board:
            print("-------------------")
            for cell in row:
                print("| ", (lambda x: " " if x is None else x)(cell), end="  ")
            print("|")
        print("-------------------")


class Human:

    @staticmethod
    def move(moves):
        # The method prompts use to input an integer to represent move on a certain cell
        while True:
            try:
                ans = int(input("Enter the cell to put move: "))
                if 0 <= ans <= 8:
                    if (ans // 3, ans % 3) in moves:
                        return ans // 3, ans % 3
                    else:
                        print("Please enter a valid move (empty cells only)")
                else:
                    print("Please enter number only from 0-8")
            except ValueError:
                print("Please enter integer only")


class RandomPlayer:

    @staticmethod
    def move(moves):
        # Player that randomly chooses from a list of available moves
        input("Press Enter to continue (opponent moves)...")
        return random.choice(moves)


class SmartPlayer:

    @staticmethod
    def move(board, moves, symbol, player_turn):
        # Calls minimax method and returns the best move for the player based on current game
        return SmartPlayer.minimax(moves, board, symbol, player_turn)[0]

    @staticmethod
    def minimax(moves, board, symbol, ai_turn, depth=1):
        # Check if there is a winner in the simulation.
        # Positive if won, negative if lost, 0 for draw. The more depth (turns) the lesser the magnitude of score
        winner = Tictactoe.check_winner(board)
        if winner == symbol:
            return None, 1 / depth
        if winner == "Draw":
            return None, 0
        if winner is not None:
            return None, -1 / depth

        best_move = None
        best_score = float("-inf")
        worst_score = float("inf")
        player_turn = (depth + ai_turn) % 2 + 1     # Returns which player's turn for the current simulation

        for move in moves:
            # Get the score for each available moves
            sub_best_move, score = SmartPlayer.minimax([x for x in moves if x != move],
                                                       Tictactoe.update_board(move, board, player_turn),
                                                       symbol,
                                                       ai_turn,
                                                       depth + 1)

            if (ai_turn != player_turn) and (score < worst_score):  # Saves the most negative score
                # worst_score, best_move = score, move
                worst_score = score
            if (ai_turn == player_turn) and (score > best_score):   # Saves the most positive (best) score and the move
                best_score, best_move = score, move

        if ai_turn == player_turn:
            return best_move, best_score    # Returns the best move if AI's turn
        else:
            return best_move, worst_score   # Returns a bad score (simulation result is lost) if enemy of AI's turn


if __name__ == '__main__':
    game = Tictactoe()
    game.run()
