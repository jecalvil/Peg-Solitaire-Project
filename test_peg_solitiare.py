import json
import os
import unittest

from board import Board
from game_logger import GameLogger


# Helper funcitons
def make_custom_board(size, peg_positions, board_type="English"):
    """Creates a custom board of a certain side with defined positions, used
    to set up specific board situations"""

    # create the board
    game = Board(board_type, size)

    # actually make sure that the pegs asked for are valid and that they exist just in case
    for row, col in peg_positions:
        on_board = (
            row >= 0 and row < size and col >= 0 and col < size
        )  # within the space
        if not on_board or game.board[row][col] == "INVALID":
            raise ValueError(
                f"{(row, col)} is not a playable spot on {board_type} {size}"
            )

    # go through each position and if it is not marked as a specific peg then make it empty
    for row in range(size):
        for col in range(size):
            if game.board[row][col] == "INVALID":
                continue
            if (row, col) in peg_positions:
                game.board[row][col] = "PEG"
            else:
                game.board[row][col] = "EMPTY"
    return game


def count_cells(game, cell_value):
    """Count the number of game cells equal to either EMPTY, PEG, or INVALID"""
    total = 0
    for row in game.board:
        for cell in row:
            if cell == cell_value:
                total += 1
    return total


def count_playable_cells(game):
    """Playable cells are ones with a peg or empty hole"""
    return count_cells(game, "PEG") + count_cells(game, "EMPTY")


def make_board_with_peg_count(peg_count):
    """Makes English board size 9 with specific number of pegs, filling the first playable spots, top to bottom"""
    layout = Board("English", 9)
    positions = []
    for row in range(9):
        for col in range(9):
            if layout.board[row][col] != "INVALID" and len(positions) < peg_count:
                positions.append((row, col))
    return make_custom_board(9, positions)


# Story 1 - Choose board size ==================================
class TestBoardSize(unittest.TestCase):
    """Unit tests for validating board size selection and error handling."""

    # Successful pick of a valid board size (5, 7, 9)
    def test_valid_board_size(self):
        """Verifies that valid board sizes (5, 7, and 9) are successfully accepted across all board types."""

        # English
        for size in [5, 7, 9]:
            board1 = Board("English", size=size)
            self.assertEqual(
                board1.size, size, f"Board size should be 5, 7, or 9 (English)"
            )

        # Diamond
        for size in [5, 7, 9]:
            board2 = Board("Diamond", size=size)
            self.assertEqual(
                board2.size, size, f"Board size should be 5, 7, or 9 (Diamond)"
            )

        # Hexagon
        for size in [5, 7, 9]:
            board3 = Board("Hexagon", size=size)
            self.assertEqual(
                board3.size, size, f"Board size should be 5, 7, or 9 (Diamond)"
            )

    # Rejection fo an Even Board Size - 6
    def test_invalid_board_size(self):
        """Verifies that even board sizes (such as 6) are rejected and default to 7."""
        # English
        board = Board("English", size=6)
        self.assertEqual(
            board.size, 7, "Even board size should be rejected and default to 7"
        )
        # Diamond
        board = Board("Diamond", size=6)
        self.assertEqual(
            board.size, 7, "Even board size should be rejected and default to 7"
        )
        # Hexagon
        board = Board("Hexagon", size=6)
        self.assertEqual(
            board.size, 7, "Even board size should be rejected and default to 7"
        )

    # Rejection of other even board sizes, default to 7
    def test_other_even_sizes_rejected(self):
        """Verifies that various even board sizes correctly fail validation and fall back to the default size."""
        for bad_size in [4, 8, 10]:
            self.assertFalse(Board.is_valid_size(bad_size), f"{bad_size} is even")
            self.assertEqual(Board("English", bad_size).size, 7)

    # Out of range (negative, small, 0, too large)
    def test_out_of_range_rejected(self):
        """Verifies that out-of-range dimensions (negative, zero, too small, or too large) are rejected and default to 7."""
        for bad_size in [3, 1, 0, -7, 11, 100]:
            self.assertFalse(Board.is_valid_size(bad_size), f"{bad_size} out of range")
            self.assertEqual(Board("English", bad_size).size, 7)

    # other symbols, decimals, and values
    def test_non_numeric_rejected(self):
        """Verifies that non-numeric, decimal, boolean, and empty inputs for board size are rejected"""
        for bad_size in ["", " ", "abc", "#", "7.1", "-7", 7.1, None, True]:
            self.assertFalse(Board.is_valid_size(bad_size), f"{bad_size!r} not a size")
            self.assertEqual(Board("English", bad_size).size, 7)

    # I have radio buttons, so text doesn't matter, but added implementation to still work just in case
    # sizes typed as text should still work
    def test_valid_sizes_accepted_as_text(self):
        """Verifies that board sizes provided as string values are correctly parsed and accepted."""
        for text_size in ["5", "7", "9", " 7 "]:
            self.assertTrue(Board.is_valid_size(text_size))
            self.assertEqual(Board("English", text_size).size, int(text_size))

    # test unknown/unspecified board types
    def test_unknown_board_type_rejected(self):
        """Verifies that unrecognized board type names raise a ValueError."""
        invalid_types = ["Triangle", "Banana", "Prism"]
        for board_type in invalid_types:
            with self.subTest(board_type=board_type):
                with self.assertRaises(ValueError):
                    Board(board_type, 7)


# Story 3 - start a new game
class TestNewGame(unittest.TestCase):
    """Unit tests for initializing new game boards and checking initial counts."""

    # 3.1, English 7 with 33 spots, 32 pegs and one mepty hole
    def test_english_7_counts(self):
        """Verifies initial cell and peg counts for a standard 7x7 English board."""
        game = Board("English", 7)
        self.assertEqual(count_playable_cells(game), 33)
        self.assertEqual(count_cells(game, "PEG"), 32)
        self.assertEqual(count_cells(game, "EMPTY"), 1)

    # test other english sizes
    def test_english_other_sizes(self):
        """Verifies initial cell and peg counts for alternative English board sizes"""
        sizes_and_cells = {5: 21, 9: 45}
        for size, expected_cells in sizes_and_cells.items():
            game = Board("English", size)
            self.assertEqual(
                count_playable_cells(game), expected_cells
            )  # peg plus hole
            self.assertEqual(
                count_cells(game, "PEG"), expected_cells - 1
            )  # -1 for the open space

    # 3.2 c     reating game of a different board size and type (Diamond and hexagon for testing)
    def test_diamond_counts(self):
        """Verifies initial cell and peg counts for Diamond board sizes"""
        sizes_and_cells = {5: 13, 7: 25, 9: 41}
        for size, expected_cells in sizes_and_cells.items():
            game = Board("Diamond", size)
            self.assertEqual(
                count_playable_cells(game), expected_cells
            )  # counts playable cells
            self.assertEqual(
                count_cells(game, "PEG"), expected_cells - 1
            )  # counts pegs
            self.assertEqual(
                count_cells(game, "EMPTY"), 1
            )  # counts empty (should just be 1 at start)

    def test_hexagon_counts(self):
        """Verifies initial cell and peg counts for Hexagon board sizes."""
        sizes_and_cells = {5: 21, 7: 37, 9: 57}
        for size, expected_cells in sizes_and_cells.items():
            game = Board("Hexagon", size)
            self.assertEqual(count_playable_cells(game), expected_cells)
            self.assertEqual(count_cells(game, "PEG"), expected_cells - 1)
            self.assertEqual(count_cells(game, "EMPTY"), 1)

    def test_center_only_empty(self):
        """Verifies that only the center position is empty upon starting any valid board configuration"""
        for board_type in ["English", "Diamond", "Hexagon"]:
            for size in [5, 7, 9]:
                game = Board(board_type, size)
                center = size // 2
                self.assertEqual(game.board[center][center], "EMPTY")
                self.assertEqual(count_cells(game, "EMPTY"), 1)

    # Rejecting ability to start new game of invalid board size (out of range   ), sitll gives 7 as board size
    # Similar to old user story 3.3, but covered under stories 1 and 2. Redundant but a valueable check
    def test_invalid_size_falls_back_to_default(self):
        """Verifies that initializing a game with an invalid size correctly falls back to default settings."""
        for bad_size in [6, 11, "abc"]:
            game = Board("Diamond", bad_size)
            self.assertEqual(game.size, 7)
            self.assertEqual(count_playable_cells(game), 25)


# ================================CHATGPT Unit Tests=====================
# Story 4 - make a move =================
class TestMakeMove(unittest.TestCase):
    """Unit tests for validating peg selection and move execution"""

    # AC 4.1: Selecting a peg that has a legal move.
    def test_ac_4_1_peg_has_legal_moves(self):
        """Verifies that selecting a peg correctly identifies its legal move destinations."""
        game = make_custom_board(9, [(4, 2), (4, 3)])

        legal_moves = game.get_legal_moves((4, 2))

        self.assertIn(
            (4, 4), legal_moves
        )  # check whether this move which is legal is within the legal moves

    # AC 4.2: Making a valid jump. # modified to include a diagonal jump as well
    def test_ac_4_2_valid_jump_updates_board(self):
        """Verifies that executing a valid orthogonal or diagonal jump correctly updates board state and peg counts."""
        # Test orthogonal jump (English board)
        game_ortho = make_custom_board(9, [(4, 2), (4, 3)], board_type="English")
        initial_peg_count = game_ortho.count_pegs()

        result_ortho = game_ortho.make_move((4, 2), (4, 4))

        self.assertTrue(result_ortho)
        self.assertEqual(game_ortho.board[4][2], "EMPTY")
        self.assertEqual(game_ortho.board[4][3], "EMPTY")
        self.assertEqual(game_ortho.board[4][4], "PEG")
        self.assertEqual(game_ortho.count_pegs(), initial_peg_count - 1)

        # Test diagonal jump (Hexagon board)
        game_diag = make_custom_board(9, [(2, 2), (3, 3)], board_type="Hexagon")
        diag_initial_count = game_diag.count_pegs()

        result_diag = game_diag.make_move((2, 2), (4, 4))

        self.assertTrue(result_diag)
        self.assertEqual(game_diag.board[2][2], "EMPTY")
        self.assertEqual(game_diag.board[3][3], "EMPTY")
        self.assertEqual(game_diag.board[4][4], "PEG")
        self.assertEqual(game_diag.count_pegs(), diag_initial_count - 1)

    # AC 4.3: Rejecting an illegal destination.
    def test_ac_4_3_illegal_move_leaves_board_unchanged(self):
        """Verifies that attempting an illegal move leaves the board and peg counts completely unchanged"""
        game = make_custom_board(9, [(4, 2), (4, 3)])
        original_board = [row[:] for row in game.board]
        initial_peg_count = game.count_pegs()

        result = game.make_move((4, 2), (4, 5))

        self.assertFalse(result)
        self.assertEqual(game.board, original_board)
        self.assertEqual(game.count_pegs(), initial_peg_count)

    # AC 4.4: Rejecting an empty hole or a peg with no legal moves.
    def test_ac_4_4_empty_or_immobile_position_has_no_legal_moves(self):
        """Verifies that empty holes and isolated pegs yield no legal moves."""
        game = make_custom_board(9, [(0, 4)])

        # The empty hole is not a valid starting peg.
        self.assertEqual(game.get_legal_moves((4, 4)), [])

        # The isolated peg cannot jump because no other pegs are present.
        self.assertEqual(game.get_legal_moves((0, 4)), [])
        self.assertEqual(game.count_pegs(), 1)

    # AC 4.5: Deselecting a selected peg.
    @unittest.skip(
        "GUI-only: manually verify selection and destination highlights disappear."
    )
    def test_ac_4_5_deselect_selected_peg(self):
        pass

    # AC 4.6: Selecting another legal peg while one is selected.
    @unittest.skip(
        "GUI-only: manually verify the new selection and its highlights replace the old ones."
    )
    def test_ac_4_6_select_another_legal_peg(self):
        pass


# Story 5 ======================
class TestGameOver(unittest.TestCase):
    """Unit tests for game over conditions, win evaluation, and ratings."""

    # AC 5.1: Game ends when no legal moves remain.
    def test_ac_5_1_no_legal_moves_remain(self):
        """Verifies game state evaluation when no legal moves remain."""
        game = make_custom_board(9, [(0, 4), (4, 0)])

        self.assertFalse(game.game_over_check())
        self.assertFalse(game.check_win())
        self.assertEqual(game.count_pegs(), 2)
        self.assertEqual(game.get_rating(), "Rating: Very Good (2 marbles left)")

    # AC 5.2: Winning the game with one peg remaining.
    def test_ac_5_2_one_peg_remaining_is_a_win(self):
        """Verifies that leaving exactly one peg results in a win and outstanding rating."""
        game = make_custom_board(9, [(4, 2), (4, 3)])

        result = game.make_move((4, 2), (4, 4))

        self.assertTrue(result)
        self.assertEqual(game.count_pegs(), 1)
        self.assertTrue(game.check_win())
        self.assertFalse(game.game_over_check())
        self.assertEqual(game.get_rating(), "Rating: Outstanding (1 marble left)")

    # AC 5.3: Game continues while legal moves exist.
    def test_ac_5_3_game_continues_when_legal_moves_remain(self):
        """Verifies that the game continues when valid moves are still available."""
        game = make_custom_board(9, [(4, 2), (4, 3), (4, 6), (4, 7)])

        result = game.make_move((4, 2), (4, 4))

        self.assertTrue(result)
        self.assertTrue(game.game_over_check())
        self.assertFalse(game.check_win())

    # AC 5.4: Moves are disabled after the game ends.
    @unittest.skip(
        "GUI-only: manually verify board clicks cannot select pegs or make moves after game over."
    )
    def test_ac_5_4_moves_disabled_after_game_over(self):
        pass

    # AC 5.5: Starting a new game after game over.
    @unittest.skip(
        "GUI-only: manually verify restarting creates a fresh board and clears the game over message."
    )
    def test_ac_5_5_restart_after_game_over(self):
        pass


# Claude Generated test for a playthrough - Story 5
class TestWinningPlaythrough(unittest.TestCase):
    """Plays a complete, known-valid solution on English 7 and checks for a win."""

    # Each entry is (start (row, col), end (row, col)); 31 moves total
    ENGLISH_7_SOLUTION = [
        ((1, 3), (3, 3)),
        ((2, 1), (2, 3)),
        ((0, 2), (2, 2)),
        ((0, 4), (0, 2)),
        ((2, 3), (2, 1)),
        ((2, 0), (2, 2)),
        ((2, 4), (0, 4)),
        ((2, 6), (2, 4)),
        ((3, 2), (1, 2)),
        ((0, 2), (2, 2)),
        ((3, 0), (3, 2)),
        ((3, 2), (1, 2)),
        ((3, 4), (3, 2)),
        ((3, 6), (3, 4)),
        ((3, 4), (1, 4)),
        ((0, 4), (2, 4)),
        ((4, 2), (2, 2)),
        ((1, 2), (3, 2)),
        ((4, 0), (4, 2)),
        ((4, 3), (4, 1)),
        ((5, 4), (3, 4)),
        ((4, 6), (4, 4)),
        ((6, 2), (4, 2)),
        ((3, 2), (5, 2)),
        ((6, 4), (6, 2)),
        ((6, 2), (4, 2)),
        ((4, 1), (4, 3)),
        ((4, 3), (4, 5)),
        ((2, 4), (4, 4)),
        ((4, 5), (4, 3)),
        ((4, 3), (6, 3)),
    ]

    def test_english_7_full_winning_game(self):
        """Executes a full 31-step winning playthrough and verifies the final win condition."""
        game = Board("English", 7)
        self.assertEqual(game.count_pegs(), 32)

        for move_number, (start, end) in enumerate(self.ENGLISH_7_SOLUTION, 1):
            with self.subTest(move=move_number, start=start, end=end):
                self.assertTrue(
                    game.make_move(start, end),
                    f"Move {move_number} {start} -> {end} was rejected",
                )

        # Exactly one peg left = win (position doesn't matter)
        self.assertEqual(game.count_pegs(), 1)
        self.assertTrue(game.check_win())
        self.assertFalse(game.game_over_check())
        self.assertEqual(game.get_rating(), "Rating: Outstanding (1 marble left)")


# Sprint 3
class TestAutomatedMoves(unittest.TestCase):
    """Unit test for testing automatic move selection, execution, and automated game flow"""

    def test_selected_random_move_is_valid(self):
        game = Board("English", 7)
        move = game.select_random_move()
        self.assertIsNotNone(move)  # check if a move was selected
        start, end = move
        self.assertTrue(
            game.is_valid_move(start, end)
        )  # check if that random move is valid

    def test_automated_move_updates_board(self):
        game = Board("Hexagon", 9)
        initial_pegs = game.count_pegs()

        move = game.make_automated_move()
        self.assertIsNotNone(move)
        self.assertEqual(game.count_pegs(), initial_pegs - 1)

    def test_automated_game_loop_until_over(self):
        """Verifies that an automated game can loop until no more moves remain or win condition is met."""
        game = Board("Diamond", 5)
        max_moves = 50
        move_count = 0

        while game.game_over_check() and move_count < max_moves:
            move = game.make_automated_move()
            self.assertIsNotNone(move)
            move_count += 1

        # The game should have terminated via game over or win
        self.assertFalse(game.game_over_check())


class TestGamePersistence(unittest.TestCase):
    """Unit tests for saving, loading, and replaying game action history and grid snapshots."""

    def setUp(self):
        """Set up a temporary test save file path."""
        self.test_filename = "test_persistence_temp.json"
        self.test_filepath = os.path.join("saved_games", self.test_filename)

    def tearDown(self):
        """Clean up temporary files after each test."""
        if os.path.exists(self.test_filepath):
            os.remove(self.test_filepath)

    def test_save_game_creates_valid_json(self):
        """Verifies that save_game correctly writes board type, size, and action history to a JSON file."""
        action_history = [{"type": "move", "from": [1, 3], "to": [3, 3]}]
        saved_path = GameLogger.save_game(
            "English", 7, action_history, custom_filename=self.test_filename
        )

        self.assertTrue(os.path.exists(saved_path))
        with open(saved_path, "r") as f:
            data = json.load(f)

        self.assertEqual(data["board_type"], "English")
        self.assertEqual(data["size"], 7)
        self.assertEqual(len(data["action_history"]), 1)

    def test_load_game_restores_action_history_and_tuples(self):
        """Verifies that load_game reads back files and correctly parses coordinate lists back into tuples."""
        action_history = [{"type": "move", "from": (1, 3), "to": (3, 3)}]
        GameLogger.save_game(
            "Diamond", 5, action_history, custom_filename=self.test_filename
        )

        loaded_data = GameLogger.load_game(self.test_filepath)

        self.assertEqual(loaded_data["board_type"], "Diamond")
        self.assertEqual(loaded_data["size"], 5)
        self.assertEqual(loaded_data["action_history"][0]["from"], (1, 3))
        self.assertEqual(loaded_data["action_history"][0]["to"], (3, 3))

    def test_replay_with_shuffle_and_randomize_snapshots(self):
        """Verifies that replaying a game action history with mid-game shuffle/randomize snapshots restores the grid."""
        game = Board("Hexagon", 7)

        # Perform a shuffle and capture snapshot
        game.shuffle_board()
        snapshot_grid = [row[:] for row in game.board]

        actions = [{"type": "shuffle", "grid_snapshot": snapshot_grid}]

        GameLogger.save_game("Hexagon", 7, actions, custom_filename=self.test_filename)
        loaded_data = GameLogger.load_game(self.test_filepath)

        # Re-initialize board and replay action history
        replayed_board = Board(loaded_data["board_type"], loaded_data["size"])
        for action in loaded_data["action_history"]:
            if action.get("type") in ["shuffle", "randomize"]:
                replayed_board.board = action["grid_snapshot"]

        self.assertEqual(replayed_board.board, snapshot_grid)


# =========== Run the tests=================
if __name__ == "__main__":
    unittest.main()
