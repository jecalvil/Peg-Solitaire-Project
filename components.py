import pygame


class MenuButton:
    """A clickable text button that changes color upon hovering over."""

    def __init__(self, text, font, text_color, hover_color, center_pos):
        """Initializes MenuButton, with text, font, text color, hover color, and position"""
        self.text = text
        self.font = font
        self.text_color = text_color
        self.hover_color = hover_color
        self.center_pos = center_pos
        self.surface = self.font.render(self.text, True, self.text_color)
        self.rect = self.surface.get_rect(center=self.center_pos)

    def draw(self, screen, mouse_pos):
        """Draws the button, using the hover color if the mouse is over it."""
        if self.rect.collidepoint(mouse_pos):
            hover_surface = self.font.render(self.text, True, self.hover_color)
            screen.blit(hover_surface, self.rect)
        else:
            screen.blit(self.surface, self.rect)

    def check_click(self, mouse_pos):
        """Returns True if mouse_pos is inside the button."""
        return self.rect.collidepoint(mouse_pos)

    def update_text(self, new_text):
        """Updates the button text and re-renders the surface"""
        self.text = new_text
        self.surface = self.font.render(self.text, True, self.text_color)
        self.rect = self.surface.get_rect(center=self.center_pos)


class RadioButton:
    """A circular radio button with a text label."""

    def __init__(self, x, y, radius, label, value, font):
        """Initializes Radio Button with location, radius, label, value, and font"""
        self.center = (x, y)
        self.radius = radius
        self.label = label
        self.value = value
        self.font = font
        self.label_surface = self.font.render(self.label, True, "White")
        self.label_rect = self.label_surface.get_rect(midleft=(x + 25, y))

    def draw(self, screen, selected_value):
        """Draws the button, filled in if its value is the selected one."""
        pygame.draw.circle(screen, "White", self.center, self.radius, 2)
        if selected_value == self.value:
            pygame.draw.circle(screen, "Yellow", self.center, self.radius - 4)
        screen.blit(self.label_surface, self.label_rect)

    def check_click(self, mouse_pos):
        """Returns True if mouse_pos is inside the radio button's circle."""
        return pygame.Vector2(mouse_pos).distance_to(self.center) <= self.radius
