import random
import pygame
import speed

class Runner:
    """
    Runner class.
    """
    def __init__(self, textures, x, y):
        """
        Initialize the runner with texture frames and position.
        """
        self.textures = textures
        self.index = 0
        self.image = textures[0]
        self.x = x
        self.y = y
        self.dy = 0  # vertical velocity
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 95  # milliseconds between animation frames

    def update(self, jump, ground_y):
        """
        Apply gravity and jump logic.
        """
        if jump and self.y >= ground_y:
            self.dy = -13
            self.x += 35  # visually move forward on jump
        self.dy += 0.35  # gravity
        self.y += self.dy
        if self.y > ground_y:
            self.y = ground_y
            self.dy = 0
            self.x = 100  # reset horizontal position when landing

    def animate(self):
        """
        Iterate to the next animation frame.
        """
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.index = (self.index + 1) % len(self.textures)
            self.image = self.textures[self.index]

    def draw(self, screen):
        """
        Render the runner.
        """
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        """
        Return the collision rectangle.
        """
        return self.image.get_rect(topleft = (self.x, self.y))


class Bird:
    """
    Bird class.
    """
    def __init__(self, textures, start_x, start_y):
        """
        Initialize the bird.
        """
        self.textures = textures
        self.index = 0
        self.image = textures[0]
        self.x = start_x
        self.y = start_y
        self.counter = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 100

    def update(self):
        """
        Move the bird and have it move on wraparound.
        """
        self.x += int(speed.SPEED * 0.6)
        if self.x < 0:
            self.counter += 1
            self.y += 100 * (-1) ** self.counter
            self.x = 1300

    def animate(self):
        """
        Cycle through animation frames.
        """
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.index = (self.index + 1) % len(self.textures)
            self.image = self.textures[self.index]

    def draw(self, screen):
        """
        Draw the bird on screen.
        """
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        """
        Return hitbox with reduced dimensions.
        """
        return self.image.get_rect(topleft = (self.x, self.y)).inflate(-self.image.get_width() * 0.4, -self.image.get_height() * 0.4)


class Student:
    """
    Student class.
    """
    def __init__(self, texture_sets, x, y):
        """
        Randomly choose a student sprite set and initialize it.
        """
        self.textures = random.choice(texture_sets)
        self.index = 0
        self.image = self.textures[0]
        self.x = x
        self.y = y
        self.active = True
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 100

    def update(self):
        """
        Move left and update animation frame.
        """
        self.x += int(speed.SPEED * 0.5)
        if self.x < -100:
            self.active = False

        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.index = (self.index + 1) % len(self.textures)
            self.image = self.textures[self.index]


    def draw(self, screen):
        """
        Draw the student sprite.
        """
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        """
        Return hitbox with reduced dimensions.
        """
        return self.image.get_rect(topleft = (self.x, self.y)).inflate(-self.image.get_width() * 0.4, -self.image.get_height() * 0.3)


class Umbrella:
    """
    Umbrella class.
    """
    def __init__(self, textures, x, y):
        """
        Initialize umbrella animation.
        """
        self.textures = textures
        self.index = 0
        self.image = textures[0]
        self.x = x
        self.y = y
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 500
        self.active = True

    def update(self):
        """
        Move the umbrella and animate its frame.
        """
        self.x += speed.SPEED * 0.5
        if self.x < -100:
            self.active = False

        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.index = (self.index + 1) % len(self.textures)
            self.image = self.textures[self.index]

    def draw(self, screen):
        """
        Render umbrella on the screen.
        """
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        """
        Return hitbox with reduced dimensions.
        """
        return self.image.get_rect(topleft = (self.x, self.y)).inflate(-self.image.get_width() * 0.4, -self.image.get_height() * 0.4)
