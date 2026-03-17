# Name: Wentao Yan , ID: 948783320, UPI: wyan132
# Program description:
# - Column: stores one column of the board and supports adding a piece / checking if full.
# - GameBoard: manages the 2D grid (as a list of Column objects) and prints the board.
# - Connect4Game: controls turns, tracks the current piece and winner, and checks game-over.
# - main(): handles user input and the play loop; validates input and prints messages/board.
class Column:
    def __init__(self, size=4):
        self.size = size
        if self.size < 4:
            self.size = 4
        self.cells = ['.'] * self.size
    
    def add_piece(self, piece):
        if "." in self.cells:
            empty_index = self.cells.index(".")
            self.cells[empty_index] = piece
        else:
            raise ValueError("Column is full")
    
    def free_cells(self):
        return self.cells.count('.')
        
    def __str__(self):
        reversed_list = reversed(self.cells)
        sentence = " ".join([str(item) for item in reversed_list])
        return sentence
        
class GameBoard:
    def __init__(self, size=4):
        self.size = size
        if self.size < 4:
            self.size = 4
        self.columns = []
        for i in range(self.size):
            self.columns.append(Column(self.size))
    
    def add(self, col, piece):
        self.columns[col].add_piece(piece)
        
    def free_in_column(self, col):
        return self.columns[col].free_cells()
        
    def is_full(self):
        count = 0
        for item in self.columns:
            if item.free_cells() == 0:
                count += 1
        return count == self.size
        
    def __str__(self):
        result = ""
        for i in range(self.size):
            row_list = " ".join(item.cells[self.size - i - 1] for item in 
            self.columns)
            result += row_list + "\n"
        result = result + "-" * (self.size*2-1) + "\n"
        result += " ".join(str(i) for i in range(self.size))
        return result
                                                                                        
    def in_bounds(self, row, column):
        return 0 <= row < self.size and 0 <= column < self.size
            
    def has_four_in_direction(self, piece, start_row, start_column,
                               step_row, step_column):
        end_row = start_row + 3 * step_row
        end_column = start_column + 3 * step_column
        if not self.in_bounds(end_row, end_column):
            return False
        for step_num in range(1, 4):
            row = start_row + step_num * step_row
            column = start_column + step_num * step_column
            if self.columns[column].cells[row] != piece:
                return False
        return True
    
    def check_winner(self, piece):
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for row in range(self.size):
            for column in range(self.size):
                if self.columns[column].cells[row] != piece:
                    continue
                for step_row, step_column in directions:
                    if self.has_four_in_direction(piece, row, column,
                                                   step_row, step_column):
                        return True
        return False

class Connect4Game:
    def __init__(self, size=4):
        self.size = size
        if self.size < 4:
            self.size = 4
        self.board = GameBoard(self.size)
        self.current_piece = "x"
        self.winner = None
    
    def switch_piece(self):
        if self.current_piece == "x":
            self.current_piece = "o"
        else:
            self.current_piece = "x"
    
    def play_turn(self, col):
        self.board.add(col, self.current_piece)
        if self.board.check_winner(self.current_piece):
            self.winner = self.current_piece
        else:
            self.switch_piece()
    
    def is_game_over(self):
        return self.winner is not None or self.board.is_full()
    
    def __str__(self):
        return str(self.board)
        
def get_board_size():
    try:
        board_size = int(input("Enter the board size: "))
    except ValueError:
        board_size = 4
    if board_size < 4:
        board_size = 4
    return board_size

def prompt_column(game, board_size):
    prompt =  input(
        f"Player {game.current_piece}, choose a column (0-{board_size - 1}): ")
    return prompt
    
def get_valid_column(game, board_size):
    raw_input = prompt_column(game, board_size)
    try:
        column = int(raw_input)
    except ValueError:
        print(f"invalid literal for int() with base 10: '{raw_input}'")
        return None
    if column < 0 or column >= board_size:
        print(f"Invalid column. Choose between 0 and {board_size - 1}.")
        return None
    return column

def place_piece(game, column):
    try:
        game.play_turn(column)
        return True
    except Exception:
        print("Column is full")
        return False

def main():
    print("Welcome to Connect 4!")
    board_size = get_board_size()
    game = Connect4Game(board_size)
    print(game)
    while not game.is_game_over():
        column = get_valid_column(game, board_size)
        if column is None:
            continue
        if not place_piece(game, column):
            continue
        print(game)
    if game.winner is None:
        print("Game Over! It's a draw.")
    else:
        print(f"Game Over! Player {game.winner} wins!")
