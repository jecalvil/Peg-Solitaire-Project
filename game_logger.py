import json
import os


class game_logger:
    """Class that can save a board position and load them"""

    # Save the game
    @staticmethod
    def save_game(self, filepath, board_type, size, move_list):
        """Saves game meta data and move history"""
        self.filepath = filepath
        self.board_type = board_type
        self.size = size
        self.move_list = move_list

        # Save it is json format
        data = {
            "filepath": filepath,
            "board_type": board_type,
            "size": size,
            "move_list": move_list,
        }

        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)

    # load the game
    @staticmethod
    def load_game(filepath):
        """Loads a game data from a json/text file for replaying"""
        # Error check for file path
        if not os.path.exist(filepath):
            # Raise an error
            raise FileNotFoundError(f"Filepath: {filepath} was not found.")
        # Open and load the data
        with open(filepath, "r") as file:
            return json.load(file)
