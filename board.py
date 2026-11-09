import random


class Board:
    """Manages Peg Solitaire game logic board state, layout generation, move validation, and win/loss"""

    VALID_SIZES = (5, 7, 9)
    VALID_TYPES = ("English", "Hexagon", "Diamond")
    DEFAULT_SIZE = 7

    JUMP_DIRECTIONS = [
        (-2, 0),  # up
        (2, 0),  # down
        (0, -2),  # left
        (0, 2),  # right
        (-2, -2),  # up-left
        (-2, 2),  # up-right
        (2, -2),  # down-left
        (2, 2),  # down-right
    ]

    def __init__(self, board_type="English", size=7):  # English and size 7 default
        """Initializes board type, dimensions, and populations 2D grid with pegs, invalid spaces, and center gap"""
        # Needed code for some earlier bug fix checks iwth unit tests
        # match the board type no matter the capitalization ("hexagon" -> "Hexagon") # Bug fix from earlier test cases
        board_type = str(board_type).capitalize()
        if board_type not in Board.VALID_TYPES:
            raise ValueError(f"Unknown board type: {board_type}")

        # an invalid size (even, out of range, not a number) uses the default size
        if not Board.is_valid_size(size):
            size = Board.DEFAULT_SIZE
        size = int(size)  # in case the size came in as text like "7"

        self.board_type = board_type
        self.size = size

        # create a board as 2D array, with size as dimensions
        self.board = []
        for row in range(size):
            row_list = []  # create a row
            for col in range(size):  # fill out the columns for that row
                if self.board_type == "English" and self.is_english_corner(row, col):
                    row_list.append("INVALID")
                elif self.board_type == "Diamond" and self.is_diamond_corner(row, col):
                    row_list.append("INVALID")
                elif self.board_type == "Hexagon" and self.is_hexagon_corner(row, col):
                    row_list.append("INVALID")
                else:
                    row_list.append("PEG")
            # add new row array into board, making it 2D
            self.board.append(row_list)

        # make the center empty (sizes are 5, 7, and 9)
        center_pos = size // 2
        self.board[center_pos][center_pos] = "EMPTY"

    def is_english_corner(self, row, col):
        """Determines if a given grid coordinates falls within an invalid corner for an English Style board"""
        corner_depth = (self.size - 3) // 2

        # check to see if a position is part of the corner boundary
        is_corner_row = (row < corner_depth) or (row >= self.size - corner_depth)
        is_corner_col = (col < corner_depth) or (col >= self.size - corner_depth)

        # return whether the position is determined to be an invalid position (corner)
        return is_corner_row and is_corner_col

    def is_diamond_corner(self, row, col):
        """Determines if a given grid coordinates falls within an invalid corner for a Diamond Style board"""

        center = self.size // 2
        # if the combined row and colum exceeds the center radius
        return abs(row - center) + abs(col - center) > center

    def is_hexagon_corner(self, row, col):
        """Determines if a given grid coordinates falls within an invalid corner for a Hexagon board"""

        corner_depth = (self.size - 3) // 2

        # Mark out the corners
        top_left = (row + col) < corner_depth
        top_right = row + (self.size - 1 - col) < corner_depth
        bottom_left = ((self.size - 1 - row) + col) < corner_depth
        bottom_right = ((self.size - 1 - row) + (self.size - 1 - col)) < corner_depth

        return top_left or top_right or bottom_left or bottom_right

    def is_valid_move(self, start_pos, end_pos):  # pos parameters are tuples
        """Checks if a jumping peg from a starting position to an end position follows the game rules"""
        # unpack coordinates
        r1, c1 = start_pos
        r2, c2 = end_pos

        # check to see whether positions are within the bounds
        if (
            (r1 >= self.size or r1 < 0)
            or (c1 >= self.size or c1 < 0)
            or (r2 >= self.size or r2 < 0)
            or (c2 >= self.size or c2 < 0)
        ):
            return False

        # check if selected position contains peg and destination is empty
        if self.board[r1][c1] != "PEG" or self.board[r2][c2] != "EMPTY":
            return False

        # the jump must be exactly 2 cells in one of the allowed directions
        row_diff = r2 - r1
        col_diff = c2 - c1
        if (row_diff, col_diff) not in self.JUMP_DIRECTIONS:
            return False

        # check if jumped over position contains peg
        mid_r = r1 + row_diff // 2
        mid_c = c1 + col_diff // 2

        # returns true if it contains peg, false otherwise
        return self.board[mid_r][mid_c] == "PEG"

    def get_legal_moves(self, pos):
        """Returns a list of all valid moves a peg can jump to from a given position on the board"""
        r, c = pos
        legal_moves = []

        for dr, dc in self.JUMP_DIRECTIONS:
            dest = (r + dr, c + dc)
            if self.is_valid_move(pos, dest):
                legal_moves.append(dest)

        return legal_moves

    def is_valid_size(value):
        """Validates whether a given board follows matched allowed dimensions"""
        # Checks to see if valid size
        if isinstance(value, bool):
            return False

        if isinstance(value, str):
            value = value.strip()
            if not value.isdigit():
                return False

        return isinstance(value, (int, str)) and int(value) in Board.VALID_SIZES

    def make_move(self, start_pos, end_pos):
        """Executes a valid peg jump, updating the board grid by removing jumped peg and moving active peg"""
        # Check for valid move
        if not self.is_valid_move(start_pos, end_pos):
            return False

        # Unpack coordinates
        r1, c1 = start_pos
        r2, c2 = end_pos

        # Find peg that is being jumped over
        target_pos_r = r1 + ((r2 - r1) // 2)
        target_pos_c = c1 + ((c2 - c1) // 2)

        # === Update Board ===
        # Change starting position to empty
        self.board[r1][c1] = "EMPTY"
        # Change middle position to empty
        self.board[target_pos_r][target_pos_c] = "EMPTY"
        # Change destination to Peg
        self.board[r2][c2] = "PEG"

        return True

    def game_over_check(self):
        """Checks if any moves remain on the board to be played"""
        # Go through each position, if there is a peg, check if there is a valid move
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == "PEG":
                    current_pos = (row, col)
                    for d_row, d_col in self.JUMP_DIRECTIONS:
                        if self.is_valid_move(current_pos, (row + d_row, col + d_col)):
                            return True
        return False

    def check_win(self):
        """Evaluates if the player has won or lost if there is one peg remaining"""
        # Count the total number of pegs currently on the board
        peg_count = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == "PEG":
                    peg_count += 1

        # A win is achieved when exactly 1 peg remains
        return peg_count == 1

    def get_rating(self):
        """Generates a performance rating to the user based on final peg count"""
        peg_count = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == "PEG":
                    peg_count += 1

        if peg_count == 1:
            return "Rating: Outstanding (1 marble left)"
        elif peg_count == 2:
            return "Rating: Very Good (2 marbles left)"
        elif peg_count == 3:
            return "Rating: Good (3 marbles left)"
        else:
            return f"Rating: Average 4 or more left ({peg_count} left)"

    def count_pegs(self):
        """Counts and returns the current number of pegs active on the board"""
        peg_count = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == "PEG":
                    peg_count += 1
        return peg_count

    # Sprint 3

    # Automatic Random moves
    def select_random_move(self):
        """Gets a list of all valid moves from all pegs and randomly selects one"""
        valid_moves = []
        for row in range(self.size):
            for col in range(self.size):
                # For pegs
                if self.board[row][col] == "PEG":
                    # Make it our starting position
                    start_pos = (row, col)
                    # Add all of its legal moves to our valid moves list
                    for end_pos in self.get_legal_moves(start_pos):
                        valid_moves.append((start_pos, end_pos))

        # Return none if empty
        if not valid_moves:
            return None

        # Return a random move from valid moves
        return random.choice(valid_moves)

    def make_automated_move(self, move=None):
        """Executes an automated move"""
        if move is None:
            move = self.select_random_move()

        if move:
            start_pos, end_pos = move
            self.make_move(start_pos, end_pos)

        return move

    # Helper Function - Get playable positions (non invalid)
    def get_non_invalid_moves(self):
        """Helper function to obtain all non invalid positions"""
        # list of valid positions
        valid_positions = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != "INVALID":
                    # Add to valid moves
                    valid_positions.append((row, col))

        return valid_positions

    # Shuffle board
    def shuffle_board(self):
        """Takes the same piece count (empty and filled pegs) and scrambles them across the current board"""
        playable_positions = self.get_non_invalid_moves()

        # Get the current count of pegs and open positions
        peg_count = self.count_pegs()
        empty_count = len(playable_positions) - peg_count

        # Create a list that contains corresponding number of valid pegs and empty positions
        pieces = []
        for _ in range(peg_count):
            pieces.append("PEG")
        for _ in range(empty_count):
            pieces.append("EMPTY")

        # Shuffle the pieces
        random.shuffle(pieces)

        # Put the shuffled pieces back on the board
        for i in range(len(playable_positions)):
            # Go in order, select that position
            row, col = playable_positions[i]
            # Set that peg value to the new randomized value at the same index in pieces
            self.board[col][row] = pieces[i]
