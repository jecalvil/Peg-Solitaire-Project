Peg Solitaire (Sprint 3)

A Peg Solitaire game written in Python with Pygame, featuring automated gameplay, game persistence (save and replay), board shuffling, and customization.

Features

Choose a board type (English, Hexagon, or Diamond) and a size (5, 7, or 9)

Start a new game with every hole filled except the center

Click a peg to select it (turns yellow) and see its legal jump destinations highlighted with green rings

Toggle Autoplay to let the computer play automatically using random legal moves

Shuffle pegs or randomize the board layout mid-game

Save games to JSON and load them back for a step-by-step visual replay

Use the hint button to see which pegs currently have valid moves

Game ends when no jumps are left or one peg remains, showing a performance rating

Restart starts a fresh board of the same type and size, and Back returns to the menu

Running it
You need Python 3 and Pygame:
pip install pygame
python peg_solitaire_gui.py

Make sure the font, images, music, and saved_games folder are in the same directory as the scripts.

Running the tests
python -m unittest test_peg_solitiare.py -v

Files

board.py: core game logic, rule validation, automated move selection, shuffling, and board layouts.

peg_solitaire_gui.py: the Pygame application controller, menus, options, and main game loop.

components.py: reusable UI button classes (Menu, Radio, Audio, Theme, Hint).

game_logger.py: handles JSON save and load file persistence for action histories.

sound_manager.py: background music playback and volume toggles.

test_peg_solitiare.py: unit test suite for game logic and persistence.
