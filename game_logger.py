import json
import os
from datetime import datetime


class GameLogger:
    """Class that can save a board position and load them"""

    # Save the game
    @staticmethod
    def save_game(board_type, size, action_history, custom_filename=None):
        """Saves game metadata and action history (moves + grid snapshots)"""
        save_dir = "saved_games"
        os.makedirs(save_dir, exist_ok=True)

        if not custom_filename:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{board_type}_Size_{size}_({timestamp}).json"
        else:
            filename = custom_filename

        filepath = os.path.join(save_dir, filename)

        # Format actions to make sure coordinate tuples become lists for JSON
        formatted_actions = []
        for action in action_history:
            if action.get("type") == "move":
                formatted_actions.append(
                    {
                        "type": "move",
                        "from": list(action["from"]),
                        "to": list(action["to"]),
                    }
                )
            else:
                # Passes through grid snapshots (shuffle/randomize) safely
                formatted_actions.append(action)

        data = {
            "board_type": board_type,
            "size": size,
            "action_history": formatted_actions,
        }

        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Game successfully saved to {filepath}")
        return filepath

    # load the game
    @staticmethod
    def load_game(filepath):
        """Loads a game data from a json/text file for replaying"""
        # Error check for file path
        if not os.path.exists(filepath):
            # Raise an error
            raise FileNotFoundError(f"Filepath: {filepath} was not found.")
        # Open and load the data
        with open(filepath, "r") as file:
            data = json.load(file)

        # Convert move coordinates back to tuples
        for action in data.get("action_history", []):
            if action.get("type") == "move":
                action["from"] = tuple(action["from"])
                action["to"] = tuple(action["to"])

        return data
