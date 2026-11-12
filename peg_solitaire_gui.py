import os
import sys
import copy

import pygame
import tkinter as tk
from tkinter import filedialog

import board
import components
from game_logger import GameLogger
import sound_manager

pygame.init()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Theme Paths

# Font Paths
FONT_PATH = os.path.join(SCRIPT_DIR, "PressStart2P-Regular.ttf")


class PegSolitaireApp:
    """Main application controller for the Peg Solitaire game, managing screens, settings, and game states"""

    def __init__(self):
        """Initializes Pygame Window, window caption, font assetss, and eventually themes"""
        # Create screen
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Peg Solitaire")

        # === Load Themes ===
        self.theme_index = 0  # 0: Green, 1: Red, 2: Wood
        theme_files = [
            "green_background.jpg",
            "red_background.jpg",
            "wood_background.jpg",
        ]
        self.themes = []

        for filename in theme_files:
            path = os.path.join(SCRIPT_DIR, "images", filename)
            try:
                img = pygame.image.load(path).convert()
                self.themes.append(pygame.transform.scale(img, (1280, 720)))
            except Exception as e:
                print(f"Warning: Could not load theme image {filename}: {e}")

        # Instantiate theme button on the bottom left
        self.theme_button = components.ThemeButton(50, 635, 60, 50)

        # === Audio ===
        # Load Audio
        self.sound_manager = sound_manager.SoundManager(
            "mondamusic-retro-arcade-game-music-512837.mp3"
        )
        # Icons for audio
        icon_size = (32, 32)
        vol_path = os.path.join(SCRIPT_DIR, "images", "volume.png")
        muted_path = os.path.join(SCRIPT_DIR, "images", "muted.png")
        try:
            self.volume_img = pygame.transform.scale(
                pygame.image.load(vol_path).convert_alpha(), icon_size
            )
            self.muted_img = pygame.transform.scale(
                pygame.image.load(muted_path).convert_alpha(), icon_size
            )
        except Exception as e:
            print(f"Warning: Could not load audio icons: {e}")
            self.volume_img = None
            self.muted_img = None
        # Instantiate
        self.audio_button = components.AudioButton(1170, 635, 60, 50)

        # Fonts
        self.font = pygame.font.Font(FONT_PATH, 40)
        self.title_font = pygame.font.Font(FONT_PATH, 70)
        self.small_font = pygame.font.Font(FONT_PATH, 20)

        # Hints
        self.show_hints_timer = 0
        self.hint_active = False

    def run(self):
        """Starts the application loop by launching the main menu."""
        self.menu_screen()

    def menu_screen(self):
        """Handles the main loop, rendering buttons, mouse input, and screen transitioning"""
        clock = pygame.time.Clock()

        # Menu buttons
        play_button = components.MenuButton(
            "PLAY", self.font, "White", "Yellow", (640, 300)
        )
        close_button = components.MenuButton(
            "CLOSE GAME", self.font, "White", "Yellow", (640, 420)
        )

        # Draw
        while True:

            # Current Mouse Position
            mouse_pos = pygame.mouse.get_pos()

            # Draw current theme background
            if self.themes:
                self.screen.blit(self.themes[self.theme_index], (0, 0))
            else:
                self.screen.fill((30, 30, 30))  # Fallback

            # Title Text
            title_surface = self.title_font.render("PEG SOLITAIRE", True, "White")
            title_rect = title_surface.get_rect(center=(640, 150))
            self.screen.blit(title_surface, title_rect)

            # Draw buttons
            play_button.draw(self.screen, mouse_pos)
            close_button.draw(self.screen, mouse_pos)
            self.audio_button.draw(
                self.screen,
                self.sound_manager.music_enabled,
                self.volume_img,
                self.muted_img,
            )

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the mouse click collided with the play button
                    if play_button.check_click(event.pos):
                        self.options_screen()
                    elif close_button.check_click(event.pos):
                        pygame.quit()
                        sys.exit()
                    # Audio button
                    elif self.audio_button.check_click(event.pos):
                        self.sound_manager.toggle_music()

                    # Theme button
                    elif self.theme_button.check_click(event.pos):
                        if self.themes:
                            self.theme_index = (self.theme_index + 1) % len(self.themes)

            self.theme_button.draw(self.screen, self.theme_index, self.small_font)
            pygame.display.update()
            clock.tick(60)

    def options_screen(self):
        """Manages settings menu where players select preferred board type and size."""
        clock = pygame.time.Clock()

        # Create settings buttons
        back_button = components.MenuButton(
            "BACK", self.font, "White", "Yellow", (200, 600)
        )
        start_game_button = components.MenuButton(
            "START", self.font, "White", "Yellow", (1080, 600)
        )

        # Track current selections
        selected_board_type = "English"
        selected_board_size = 7

        # Create buttons for board type
        board_type_buttons = [
            components.RadioButton(250, 380, 10, "English", "English", self.small_font),
            components.RadioButton(250, 440, 10, "Hexagon", "Hexagon", self.small_font),
            components.RadioButton(250, 500, 10, "Diamond", "Diamond", self.small_font),
        ]

        # Create buttons for board size
        board_size_buttons = [
            components.RadioButton(770, 380, 10, "Small (5x5)", 5, self.small_font),
            components.RadioButton(770, 440, 10, "Standard (7x7)", 7, self.small_font),
            components.RadioButton(770, 500, 10, "Large (9x9)", 9, self.small_font),
        ]

        # Draw
        while True:
            # Fill screen and mouse pos
            # Draw current theme background
            if self.themes:
                self.screen.blit(self.themes[self.theme_index], (0, 0))
            else:
                self.screen.fill((30, 30, 30))  # Fallback
            mouse_pos = pygame.mouse.get_pos()

            # Draw curent settings title
            current_settings_surface = self.title_font.render(
                "CURRENT SETTINGS", True, "White"
            )
            self.screen.blit(
                current_settings_surface,
                current_settings_surface.get_rect(center=(640, 150)),
            )

            # Board Type Title
            board_type_surface = self.font.render("BOARD TYPE", True, "White")
            self.screen.blit(
                board_type_surface, board_type_surface.get_rect(center=(380, 300))
            )
            # Board Size Title
            board_size_surface = self.font.render("BOARD SIZE", True, "White")
            self.screen.blit(
                board_size_surface, board_size_surface.get_rect(center=(900, 300))
            )

            # Draw Settings Radio Buttons
            for btn in board_type_buttons:
                btn.draw(self.screen, selected_board_type)

            for btn in board_size_buttons:
                btn.draw(self.screen, selected_board_size)

            # Draw Navigation Buttons
            back_button.draw(self.screen, mouse_pos)
            start_game_button.draw(self.screen, mouse_pos)

            # Draw Audio
            self.audio_button.draw(
                self.screen,
                self.sound_manager.music_enabled,
                self.volume_img,
                self.muted_img,
            )

            # Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    # Back Buttons
                    if back_button.check_click(mouse_pos):
                        return  # Exit and go back to main screen

                    # Star Game Button
                    elif start_game_button.check_click(mouse_pos):
                        self.game_screen(selected_board_type, selected_board_size)

                    # Audio button
                    elif self.audio_button.check_click(event.pos):
                        self.sound_manager.toggle_music()

                    # Theme
                    elif self.theme_button.check_click(event.pos):
                        if self.themes:
                            self.theme_index = (self.theme_index + 1) % len(self.themes)

                    # Check for clicks on board type buttons
                    for btn in board_type_buttons:
                        if btn.check_click(event.pos):
                            selected_board_type = btn.value

                    # Check for clicks onboard size buttons
                    for btn in board_size_buttons:
                        if btn.check_click(event.pos):
                            selected_board_size = btn.value

            self.theme_button.draw(self.screen, self.theme_index, self.small_font)
            pygame.display.update()
            clock.tick(60)

    def game_screen(self, board_type, size):
        """Controls active gameplay loop, board rendering, peg selection, move validation, and win/loss states"""
        clock = pygame.time.Clock()
        game_board = board.Board(board_type, size)
        selected_peg = None
        game_over_text = None
        message_text = None

        # Automated move variables
        autoplay_enabled = False
        last_auto_move_time = 0
        AUTO_MOVE_DELAY = 500
        pending_auto_move = None
        # Replay Variables
        replay_queue = []
        last_replay_time = 0
        REPLAY_DELAY = 500

        # Record moves
        self.action_history = []

        # Back Button
        back_button = components.MenuButton(
            "BACK", self.small_font, "White", "Yellow", (100, 50)
        )
        # Restart Button
        restart_button = components.MenuButton(
            "RESTART", self.small_font, "White", "Yellow", (1180, 50)
        )
        autoplay_button = components.MenuButton(
            "AUTOPLAY: OFF", self.small_font, "White", "Yellow", (1085, 350)
        )
        shuffle_button = components.MenuButton(
            "SHUFFLE PEGS", self.small_font, "White", "Yellow", (1085, 405)
        )
        random_layout_button = components.MenuButton(
            "RANDOM LAYOUT", self.small_font, "White", "Yellow", (1085, 455)
        )
        # Save Game Button
        save_game_button = components.MenuButton(
            "SAVE GAME", self.small_font, "White", "Yellow", (1085, 300)
        )
        # Load Game Button
        load_game_button = components.MenuButton(
            "LOAD GAME", self.small_font, "White", "Yellow", (1085, 250)
        )
        # Hint button
        hint_button = components.HintButton(1010, 510, 150, 45)

        # Draw
        while True:
            # Draw current theme background
            if self.themes:
                self.screen.blit(self.themes[self.theme_index], (0, 0))
            else:
                self.screen.fill((30, 30, 30))  # Fallback
            mouse_pos = pygame.mouse.get_pos()
            current_time = pygame.time.get_ticks()

            box_size = 500  # fixeed box size play area
            cell_size = box_size // size
            grid_width = size * cell_size
            grid_height = size * cell_size

            # Center grid on 1280x720 screen
            start_x = (1280 - grid_width) // 2
            start_y = (720 - grid_height) // 2

            # Draw audio
            self.audio_button.draw(
                self.screen,
                self.sound_manager.music_enabled,
                self.volume_img,
                self.muted_img,
            )

            # Hint timer
            # If hints are active, auto-turn them off after 2 seconds (2000 ms)
            if self.hint_active:
                if pygame.time.get_ticks() - self.show_hints_timer > 2000:
                    self.hint_active = False

            # Check for win/loss each fram
            if game_over_text is None and not replay_queue:
                if game_board.check_win():
                    game_over_text = "YOU WON!"
                    autoplay_enabled = False
                    autoplay_button.update_text("AUTOPLAY: OFF")
                elif not game_board.game_over_check():
                    game_over_text = "GAME OVER"
                    autoplay_enabled = False
                    autoplay_button.update_text("AUTOPLAY: OFF")

            # Step-by-step replay of a loaded game
            if replay_queue and current_time - last_replay_time > REPLAY_DELAY:
                action = replay_queue.pop(0)
                if action.get("type") == "move":
                    game_board.make_move(action["from"], action["to"])
                elif action.get("type") in ["shuffle", "randomize"]:
                    game_board.set_board_grid(
                        action["grid_snapshot"]
                    )  # Adjusted based on LLM feedback
                self.action_history.append(action)
                last_replay_time = current_time
                if not replay_queue:
                    message_text = "REPLAY FINISHED"
            # Autoplay functionality
            if autoplay_enabled and game_over_text is None:
                if current_time - last_auto_move_time > AUTO_MOVE_DELAY:

                    # Ask board for a move to highlight it
                    if pending_auto_move is None:
                        # select a move
                        pending_auto_move = game_board.select_random_move()
                        if pending_auto_move:
                            # select that peg
                            selected_peg = pending_auto_move[0]
                        else:
                            # no moves
                            autoplay_enabled = False
                            autoplay_button.update_text("AUTOPLAY: OFF")
                            selected_peg = None

                    # Pass move back to the board to execute it
                    else:
                        game_board.make_automated_move(pending_auto_move)
                        # Fix for bug: needs to record automated moves too
                        self.action_history.append(
                            {
                                "type": "move",
                                "from": pending_auto_move[0],
                                "to": pending_auto_move[1],
                            }
                        )
                        # remove selected peg highlight
                        selected_peg = None
                        # reset pending move
                        pending_auto_move = None

                    last_auto_move_time = current_time

            # Determine title text based on state
            title_text = game_over_text if game_over_text else "PEG SOLITAIRE"

            # Title Text
            title_surface = self.title_font.render(title_text, True, "White")
            title_rect = title_surface.get_rect(center=(640, 50))
            self.screen.blit(title_surface, title_rect)

            if game_over_text:
                rating_text = game_board.get_rating()
                rating_surface = self.small_font.render(rating_text, True, "Yellow")
                rating_rect = rating_surface.get_rect(center=(640, 90))
                self.screen.blit(rating_surface, rating_rect)

            # Display Board Type Title
            mode_surface = self.small_font.render("BOARD TYPE:", True, "White")
            mode_rect = mode_surface.get_rect(center=(start_x // 2, 360))
            self.screen.blit(mode_surface, mode_rect)

            # Display Board Value
            type_surface = self.small_font.render(f"{board_type}", True, "White")
            type_rect = type_surface.get_rect(center=(start_x // 2, 390))
            self.screen.blit(type_surface, type_rect)

            # Display Board Size Title
            size_title_surface = self.small_font.render("BOARD SIZE:", True, "White")
            size_title_rect = size_title_surface.get_rect(center=(start_x // 2, 420))
            self.screen.blit(size_title_surface, size_title_rect)

            # Display Board Size Value
            size_value_surface = self.small_font.render(f"{size}", True, "White")
            size_value_rect = size_value_surface.get_rect(center=(start_x // 2, 450))
            self.screen.blit(size_value_surface, size_value_rect)

            # Legal destinations for the selected peg
            legal_moves = []
            if selected_peg is not None:
                legal_moves = game_board.get_legal_moves(selected_peg)

            # Draw Board Grid
            for row in range(size):
                for col in range(size):
                    cell_type = game_board.get_cell(
                        row, col
                    )  # changed based on LLM feedback

                    # Box for each cell
                    rect = pygame.Rect(
                        start_x + col * cell_size,
                        start_y + row * cell_size,
                        cell_size - 4,
                        cell_size - 4,
                    )

                    # Skip if an invalid corner space
                    if cell_type == "INVALID":
                        continue
                    # Draw Valid Pegs
                    elif cell_type == "PEG":
                        # Selected Peg Color
                        if selected_peg == (row, col):
                            color = (255, 255, 0)
                        # Non Selected Peg Color
                        else:
                            color = (200, 200, 200)
                        # Set Color
                        pygame.draw.circle(
                            self.screen, color, rect.center, cell_size // 3
                        )

                        # Draw hint highlight ring if hint is active and this peg has legal moves
                        if self.hint_active and game_board.get_legal_moves((row, col)):
                            pygame.draw.circle(
                                self.screen,
                                (255, 165, 0),
                                rect.center,
                                cell_size // 3 + 4,
                                3,
                            )

                    # Empty Placeholders
                    elif cell_type == "EMPTY":
                        if (row, col) in legal_moves:
                            # Highlight legal destination
                            pygame.draw.circle(
                                self.screen, (0, 200, 0), rect.center, cell_size // 4, 4
                            )
                        else:
                            pygame.draw.circle(
                                self.screen,
                                (70, 70, 70),
                                rect.center,
                                cell_size // 4,
                                2,
                            )

            # Display message (illegal move, no moves available)
            if message_text:
                message_surface = self.small_font.render(message_text, True, "Red")
                message_rect = message_surface.get_rect(center=(640, 670))
                self.screen.blit(message_surface, message_rect)

            # Draw the Navigation buttons
            back_button.draw(self.screen, mouse_pos)
            restart_button.draw(self.screen, mouse_pos)
            if not replay_queue:
                save_game_button.draw(self.screen, mouse_pos)
                load_game_button.draw(self.screen, mouse_pos)

            # Draw Autoplay, Shuffle, Randomize if game is not over
            if game_over_text is None and not replay_queue:
                autoplay_button.draw(self.screen, mouse_pos)
                shuffle_button.draw(self.screen, mouse_pos)
                random_layout_button.draw(self.screen, mouse_pos)
                hint_button.draw(self.screen, self.small_font)

            # Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # quit button
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:  # Button clicks
                    # Back button
                    if back_button.check_click(event.pos) and not replay_queue:
                        return

                    # Restart button
                    if restart_button.check_click(event.pos) and not replay_queue:
                        game_board = board.Board(board_type, size)
                        selected_peg = None
                        game_over_text = None
                        message_text = None
                        self.action_history = []
                        replay_queue = []
                        continue

                    # Audio
                    elif self.audio_button.check_click(event.pos):
                        self.sound_manager.toggle_music()

                    # Theme
                    elif self.theme_button.check_click(event.pos):
                        if self.themes:
                            self.theme_index = (self.theme_index + 1) % len(self.themes)

                    # Save game
                    if save_game_button.check_click(event.pos) and not replay_queue:
                        try:
                            GameLogger.save_game(board_type, size, self.action_history)
                            message_text = "GAME SAVED TO /saved_games!"
                        except Exception as e:
                            message_text = "ERROR SAVING GAME"
                            print(f"CRITICAL SAVE ERROR: {e}")

                    # Load Game
                    if load_game_button.check_click(event.pos) and not replay_queue:
                        # try to open the folder/filepath
                        try:
                            # directory
                            saved_dir = os.path.abspath("saved_games")
                            os.makedirs(saved_dir, exist_ok=True)

                            # open fial dialog over pygame
                            root = tk.Tk()
                            root.withdraw()
                            root.attributes("-topmost", True)

                            file_path = filedialog.askopenfilename(
                                initialdir=saved_dir,
                                title="Select a Saved Game",
                                filetypes=[
                                    ("JSON Files", "*.json"),
                                    ("All Files", "*.*"),
                                ],
                            )

                            if file_path:
                                loaded_data = GameLogger.load_game(file_path)
                                board_type = loaded_data["board_type"]
                                size = loaded_data["size"]
                                self.action_history = loaded_data["action_history"]

                                # Re-initialize board and replay action history
                                game_board = board.Board(board_type, size)
                                replay_queue = list(loaded_data["action_history"])
                                self.action_history = (
                                    []
                                )  # refilled as each action is replayed
                                autoplay_enabled = False
                                autoplay_button.update_text("AUTOPLAY: OFF")
                                pending_auto_move = None
                                selected_peg = None
                                game_over_text = None
                                message_text = "REPLAYING SAVED GAME..."

                                selected_peg = None
                                game_over_text = None
                                message_text = "GAME LOADED SUCCESSFULLY!"
                        except Exception as e:
                            message_text = "ERROR LOADING GAME"
                            print(f"CRITICAL LOAD ERROR: {e}")

                    # Buttons for when game is off
                    if game_over_text is None or replay_queue:
                        # Automated play button
                        if autoplay_button.check_click(event.pos) and not replay_queue:
                            # toggle
                            autoplay_enabled = not autoplay_enabled
                            # update text
                            if autoplay_enabled:
                                autoplay_button.update_text("AUTOPLAY: ON")
                            else:
                                autoplay_button.update_text("AUTOPLAY: OFF")

                        # Shuffle Pegs Button
                        if shuffle_button.check_click(event.pos) and not replay_queue:
                            game_board.shuffle_board()
                            # Record shuffle event with a grid snapshot
                            self.action_history.append(
                                {
                                    "type": "shuffle",
                                    "grid_snapshot": copy.deepcopy(game_board.board),
                                }
                            )
                            # Deselect anything if selected
                            selected_peg = None
                            pending_auto_move = None
                            message_text = None

                        # Random Layout Button
                        if (
                            random_layout_button.check_click(event.pos)
                            and not replay_queue
                        ):
                            game_board.randomize_layout()
                            # Record randomize event with a grid snapshot
                            self.action_history.append(
                                {
                                    "type": "randomize",
                                    "grid_snapshot": copy.deepcopy(game_board.board),
                                }
                            )
                            # Deselect anything if selected
                            selected_peg = None
                            pending_auto_move = None
                            message_text = None

                        # Hints
                        # If hints are active, any click dismisses them first
                        if self.hint_active:
                            self.hint_active = False

                        # Check hint button click
                        if game_over_text is None and hint_button.check_click(
                            event.pos
                        ):
                            # Find all pegs that have legal moves
                            movable_pegs = []
                            for r in range(size):
                                for c in range(size):
                                    if game_board.get_cell(
                                        r, c
                                    ) == "PEG" and game_board.get_legal_moves((r, c)):
                                        movable_pegs.append((r, c))

                            if not movable_pegs:
                                message_text = "NO MORE LEGAL MOVES, GAME IS OVER!"
                            else:
                                self.hint_active = True
                                self.show_hints_timer = pygame.time.get_ticks()
                                message_text = (
                                    f"HINT: {len(movable_pegs)} PEGS CAN BE MOVED"
                                )

                    # Make sure grid clicks only active when game is not over
                    if game_over_text is not None and not replay_queue:
                        continue

                    # Block manual clicks while autoplay
                    if autoplay_enabled:
                        continue

                    # Grid click
                    mouse_x, mouse_y = event.pos
                    if (start_x <= mouse_x and mouse_x < start_x + grid_width) and (
                        start_y <= mouse_y and mouse_y < start_y + grid_height
                    ):
                        # Find the clicked column
                        clicked_col = (mouse_x - start_x) // cell_size
                        clicked_row = (mouse_y - start_y) // cell_size

                        # Check to make sure clicked col and row are within the size
                        if (clicked_col >= 0 and clicked_col < size) and (
                            clicked_row >= 0 and clicked_row < size
                        ):
                            # Select our corresponding gui cell to logi
                            cell_value = game_board.get_cell(
                                clicked_row, clicked_col
                            )  # adjusted based on feedback

                            # Selection and De-selection
                            if cell_value == "PEG":
                                if selected_peg == (
                                    clicked_row,
                                    clicked_col,
                                ):  # re-selected, so should deselect
                                    selected_peg = None
                                    message_text = None
                                elif game_board.get_legal_moves(
                                    (clicked_row, clicked_col)
                                ):
                                    selected_peg = (
                                        clicked_row,
                                        clicked_col,
                                    )  # new peg, select it2
                                    message_text = None
                                else:
                                    # peg with no legal jumps, nothing is selected
                                    selected_peg = None
                                    message_text = (
                                        "NO MOVE AVAILABLE FROM THAT POSITION"
                                    )

                            # Making a move
                            elif cell_value == "EMPTY":
                                if selected_peg is not None:
                                    if game_board.make_move(
                                        selected_peg, (clicked_row, clicked_col)
                                    ):
                                        self.action_history.append(
                                            {
                                                "type": "move",
                                                "from": selected_peg,
                                                "to": (clicked_row, clicked_col),
                                            }
                                        )
                                        selected_peg = (
                                            None  # Deselect peg after move is made
                                        )
                                        message_text = None
                                    else:
                                        # illegal destination, peg stays selected
                                        message_text = "MOVE NOT ALLOWED"
                                else:
                                    # empty hole as a starting point
                                    message_text = (
                                        "NO MOVE AVAILABLE FROM THAT POSITION"
                                    )

                            # Clicking outside the board shape while a peg is selected
                            elif selected_peg is not None:
                                message_text = "MOVE NOT ALLOWED"

            self.theme_button.draw(self.screen, self.theme_index, self.small_font)
            pygame.display.update()
            clock.tick(60)


if __name__ == "__main__":
    PegSolitaireApp().run()
