import os
import pygame


class SoundManager:
    """Manages background music across all screens"""

    def __init__(self, music_filename):
        # Enable the music automatically
        self.music_enabled = True

        # Get the file path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Point to sub folder
        self.music_path = os.path.join(script_dir, "music", music_filename)

        # Load
        if os.path.exists(self.music_path):
            pygame.mixer.music.load(self.music_path)
            # make it play indefinite
            pygame.mixer.music.play(-1)
        else:
            print(f"Warning: Music file not found at {self.music_path}")

    def toggle_music(self):
        """Mutes or unmutes the music instantly without resetting its position by adjusting volume."""
        self.music_enabled = not self.music_enabled  # toggle
        if self.music_enabled:
            pygame.mixer.music.set_volume(1.0)  # Full volume
        else:
            pygame.mixer.music.set_volume(
                0.0
            )  # Muted (silenced, but keeps playing in background)
        return self.music_enabled
