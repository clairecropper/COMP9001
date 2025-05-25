import os
import random
import pygame
import speed

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700


class ScrollingBackground:
    """
    A base class for parallax-scrolling background layers
    like the skyline or footpath.
    """
    def __init__(self, texture, y, speed_factor=1.2, scale=1.5):
        """
        Initialize the background with scaled image, scroll speed, and vertical position.
        """
        self.image = pygame.transform.scale(texture, (int(texture.get_width() * scale), int(texture.get_height() * scale)))
        self.width = self.image.get_width()
        self.y = y
        self.speed_factor = speed_factor
        self.x1 = 0
        self.x2 = self.width

    def update(self):
        """
        Scroll the background based on current speed.
        Resets position to create a continuous loop.
        """
        current_speed = speed.SPEED * self.speed_factor
        self.x1 += current_speed
        self.x2 += current_speed

        # Wrap images when they move out of view
        if self.x1 < -self.width:
            self.x1 = self.width
        if self.x2 < -self.width:
            self.x2 = self.width

    def draw(self, screen):
        """
        Draw both images side-by-side to simulate scrolling.
        """
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))


class Skyline(ScrollingBackground):
    """
    A slow-scrolling skyline background layer for parallax effect.
    """
    def __init__(self, texture):
        super().__init__(texture, y = -60, speed_factor = 1/5, scale = 0.6)


class Footpath(ScrollingBackground):
    """
    The midground footpath layer the runner runs on.
    """
    def __init__(self, texture):
        super().__init__(texture, y = WINDOW_HEIGHT - 170, speed_factor = 1/3, scale = 0.65)


class Rain:
    """
    Rain drop class.
    """
    def __init__(self, num_drops):
        """
        Initialize a list of raindrops with random positions and speeds.
        """
        self.drops = [
            [pygame.Vector2(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)), random.randint(10, 25)] for _ in range(num_drops)
        ]

    def update(self):
        """
        Move raindrops downward. Wrap them to the top if they go off screen.
        """
        for drop in self.drops:
            drop[0].y += drop[1]
            if drop[0].y > WINDOW_HEIGHT:
                drop[0].y = 0
                drop[0].x = random.randint(0, WINDOW_WIDTH)

    def draw(self, screen, alpha = 255):
        """
        Draw all raindrops as semi-transparent lines.
        """
        rain_layer = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        for drop in self.drops:
            pygame.draw.line(rain_layer, (0, 35, 102, alpha), drop[0], (drop[0].x, drop[0].y + 10), 2)
        screen.blit(rain_layer, (0, 0))


# Path to custom font
font_path = os.path.join("font", "ApercuMonoProBold.ttf")


def draw_text(screen, text, size, x, y, color=(255, 255, 255)):
    """
    Draw text using a custom font.
    """
    font = pygame.font.Font(font_path, size)
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def get_highscore(current_score):
    """
    Load the high score from file, update if current score is higher,
    and save it back to the file.
    """
    path = "highscore.txt"
    try:
        with open(path, 'r') as file:
            high = int(file.read().strip())
    except Exception:
        high = 0

    high = max(high, current_score)

    with open(path, 'w') as file:
        file.write(str(high))

    return high


def load_scaled_images(directory, prefix, indices, scale):
    """
    Load and scale multiple images from a given directory with a filename prefix.
    """
    return [
        pygame.transform.scale(
            pygame.image.load(f"{directory}/{prefix}{i}.png").convert_alpha(),
            (
                int(pygame.image.load(f"{directory}/{prefix}{i}.png").get_width() * scale),
                int(pygame.image.load(f"{directory}/{prefix}{i}.png").get_height() * scale)
            )
        ) for i in indices
    ]
