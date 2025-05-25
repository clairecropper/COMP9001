import random
import time
import pygame
import speed

from draw import draw_menu, draw_character_select, draw_game, draw_game_over
from sprites import Runner, Bird, Student, Umbrella
from background import Footpath, Rain, Skyline, load_scaled_images

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
RUNNER_X = 100
RUNNER_Y = WINDOW_HEIGHT - 200


class Game:
    """
    Main Game class that manages initialization, game state,
    asset loading, screen rendering, and gameplay logic.
    """

    def __init__(self):
        """Initialize the game and its default state."""
        pygame.init()
        icon = pygame.image.load("img/window_icon.jpg")
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("LATE FOR LECTURE - COMP9001 Final Project by Claire Cropper")
        self.clock = pygame.time.Clock()

        # Game control flags
        self.speed_multiplier = 1.0
        self.last_speedup_score = 0
        self.running = True
        self.game_start = False
        self.game_over = False
        self.character_chosen = False
        self.character_select = False
        self.score = 0
        self.font = pygame.font.Font(pygame.font.get_default_font(), 30)

        # Weather and rain handling
        self.weather_active = False
        self.rain = Rain(150)
        self.rain_alpha = 0
        self.rain_fade_duration = 3
        self.next_rain_time = None
        self.rain_end_time = None
        self.rain_fading_out = False

        self.load_assets()


    def load_assets(self):
        """Load all images, characters, and background elements."""
        # Characters
        self.runner_armin = load_scaled_images("img/characters", "armin_running_", range(1, 9), 3)
        self.runner_karlos = load_scaled_images("img/characters", "karlos_running_", range(1, 9), 3)
        self.runner_armin_preview = self.runner_armin[0]
        self.runner_karlos_preview = self.runner_karlos[0]
        self.preview_armin = Runner(self.runner_armin, 350, RUNNER_Y - 160)
        self.preview_karlos = Runner(self.runner_karlos, 750, RUNNER_Y - 160)
        self.selected_runner = None

        # Bird enemy
        self.bird = Bird(load_scaled_images("img/obstacles", "magpie_", range(1, 9), 0.4), 1300, random.randint(290, 350))

        # Student obstacles (3 sets)
        self.student_textures = [
            load_scaled_images("img/obstacles", "student1_", range(1, 9), 2.55),
            load_scaled_images("img/obstacles", "student2_", range(1, 9), 2.55),
            load_scaled_images("img/obstacles", "student3_", range(1, 9), 2.55)
        ]
        self.students = []

        # Umbrella hazards
        self.umbrella_textures = load_scaled_images("img/obstacles", "umbrella_", range(1, 3), 0.35)
        self.spawned_umbrellas = []
        self.umbrella_spawn_times = []

        # Background layers
        self.skyline = Skyline(pygame.image.load("img/background/pt.png").convert_alpha())
        self.footpath = Footpath(pygame.image.load("img/background/footpath.jpg").convert_alpha())


    def reset_game(self):
        """Reset game state for a new run."""
        self.runner = Runner(self.selected_runner, RUNNER_X, RUNNER_Y)
        self.bird.x, self.bird.y, self.bird.counter = 1300, random.randint(290, 350), 0

        self.speed_multiplier = 1.0
        speed.SPEED = -7

        self.score = 0
        self.start_time = time.time()

        self.students.clear()
        self.spawned_umbrellas.clear()
        self.umbrella_spawn_times.clear()
        self.weather_active = False


    def update_score(self):
        """Update the score based on elapsed time."""
        self.score = int(time.time() - self.start_time)


    def game_loop(self):
        """Main update and draw loop during gameplay."""
        current_time = time.time()
        self.game_over = False

        self.update_score()
        self.skyline.update()
        self.footpath.update()

        keys = pygame.key.get_pressed()
        self.runner.update(keys[pygame.K_SPACE], WINDOW_HEIGHT - 220)
        self.bird.update()

        self.runner.animate()
        self.bird.animate()
        draw_game(self)

        # Spawn student if none present
        if not self.students:
            student = Student(self.student_textures, x=1300, y=RUNNER_Y + 15)
            self.students.append(student)

        # Update and draw all students
        for student in self.students[:]:
            student.update()
            if student.active:
                student.draw(self.screen)
            else:
                self.students.remove(student)

        # Additional runner animation if grounded
        if self.runner.y >= WINDOW_HEIGHT - 220:
            self.runner.animate()

        # Speed increases as score increases
        if self.score % 50 == 0 and self.score != self.last_speedup_score:
            self.speed_multiplier += 0.7
            speed.SPEED = int(-7 * self.speed_multiplier)
            self.last_speedup_score = self.score

        # Handle weather and fog effect
        if self.weather_active or self.rain_alpha > 0:
            self.rain.update()
            self.rain.draw(self.screen, alpha=self.rain_alpha)

            # Grey hue overlay
            grey_hue = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            fog_alpha = int(self.rain_alpha * 0.3)
            grey_hue.fill((100, 100, 100, fog_alpha))
            self.screen.blit(grey_hue, (0, 0))

        # Spawn umbrella hazard during rain
        if not self.spawned_umbrellas and self.umbrella_spawn_times:
            next_spawn_time = self.umbrella_spawn_times[0]
            if current_time >= next_spawn_time:
                umbrella = Umbrella(self.umbrella_textures, 1300, RUNNER_Y + 40)
                self.spawned_umbrellas.append(umbrella)
                self.umbrella_spawn_times.pop(0)

        # Update and draw umbrellas, handle collision
        for umbrella in self.spawned_umbrellas[:]:
            umbrella.update()
            if self.runner.get_rect().colliderect(umbrella.get_rect()):
                self.spawned_umbrellas.remove(umbrella)
                self.game_over = True
            if umbrella.active:
                umbrella.draw(self.screen)
            else:
                self.spawned_umbrellas.remove(umbrella)

        # Collision with bird
        if self.runner.get_rect().colliderect(self.bird.get_rect()):
            self.game_over = True

        # Collision with student
        for student in self.students:
            if self.runner.get_rect().colliderect(student.get_rect()):
                self.game_over = True


    def handle_events(self):
        """Process key presses and quit events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # Menu controls
                if not self.game_start and not self.character_select:
                    if event.key == pygame.K_c:
                        self.character_select = True
                    elif self.character_chosen:
                        self.game_start = True
                        self.reset_game()
                # Game over controls
                elif self.game_over:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    else:
                        self.game_over = False
                        self.reset_game()

    def run(self):
        """Main game execution loop."""
        while self.running:
            if self.character_select:
                draw_character_select(self)
            elif not self.game_start:
                draw_menu(self)
            elif self.game_over:
                draw_game_over(self)
            else:
                self.game_loop()

            pygame.display.flip()
            self.handle_events()
            self.clock.tick(60)


# Entry point of the game
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
