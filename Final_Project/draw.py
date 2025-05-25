import random
import time
import pygame

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

from background import get_highscore, draw_text


def draw_menu(game):
    """Render the game menu before the game starts."""
    game.screen.fill((255, 255, 255))
    game.skyline.draw(game.screen)
    game.footpath.draw(game.screen)

    # Draw a semi-transparent rectangle to make text readable
    panel_width = 1000
    panel_height = 400
    panel_x = (WINDOW_WIDTH - panel_width) // 2
    panel_y = 90

    panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    panel_surface.fill((255, 255, 255, 205))  # White background with alpha transparency
    game.screen.blit(panel_surface, (panel_x, panel_y))

    draw_text(game.screen, "LATE FOR LECTURE", 72, 255, panel_y + 50, (230, 70, 38))

    if not game.character_chosen:
        draw_text(game.screen, "Oh no! You lost track of time!", 24, 350, panel_y + 140, (66, 66, 66))
        draw_text(game.screen, "You only have a few minutes left to reach Wallace Theatre.", 24, 180, panel_y + 170, (66, 66, 66))
        draw_text(game.screen, "Dodge magpies, jump over students, and sprint through the city...", 24, 160, panel_y + 200, (66, 66, 66))
        draw_text(game.screen, "... all before time runs out!", 24, 340, panel_y + 230, (66, 66, 66))
        draw_text(game.screen, "Can you make it in time?", 24, 400, panel_y + 260, (66, 66, 66))
        draw_text(game.screen, "Press [C] to choose your runner!", 30, 300, 420, (0, 0, 0))
    else:
        draw_text(game.screen, "Press [SPACEBAR] to jump over obstacles", 28, 270, 280, (0, 0, 0))
        draw_text(game.screen, "Press any key to begin your sprint!", 30, 275, 340, (0, 0, 0))
        draw_text(game.screen, "Good luck!", 40, 450, 420, (0, 0, 0))


def draw_character_select(game):
    """Render the character selection screen."""
    game.screen.fill((210, 210, 210))

    # Draw glass panel
    rect_width = int(WINDOW_WIDTH * 0.8)
    rect_height = int(WINDOW_HEIGHT * 0.75)
    rect_x = (WINDOW_WIDTH - rect_width) // 2
    rect_y = (WINDOW_HEIGHT - rect_height) // 2

    glass = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
    glass.fill((255, 255, 255, 60))
    game.screen.blit(glass, (rect_x, rect_y))

    pygame.draw.rect(game.screen, (200, 200, 200), (rect_x, rect_y, rect_width, rect_height), width = 4, border_radius = 20)

    # Draw circles behind characters
    pygame.draw.circle(game.screen, (180, 180, 180, 60), (395, 410), 100)
    pygame.draw.circle(game.screen, (180, 180, 180, 60), (795, 410), 100)

    draw_text(game.screen, "CHOOSE YOUR CHARACTER", 60, 220, 130, (230, 70, 38))

    # Draw animated previews
    game.preview_armin.animate()
    game.preview_karlos.animate()
    game.preview_armin.draw(game.screen)
    game.preview_karlos.draw(game.screen)

    draw_text(game.screen, "Armin", 30, 342, 520, (230, 70, 38))
    draw_text(game.screen, "Karlos", 30, 742, 520, (230, 70, 38))

    # Hover and click detection
    mouse_pos = pygame.mouse.get_pos()
    armin_rect = game.preview_armin.get_rect()
    karlos_rect = game.preview_karlos.get_rect()

    if armin_rect.collidepoint(mouse_pos) or karlos_rect.collidepoint(mouse_pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    if pygame.mouse.get_pressed()[0]:
        if armin_rect.collidepoint(mouse_pos):
            game.selected_runner = game.runner_armin
            game.character_chosen = True
            game.character_select = False
        elif karlos_rect.collidepoint(mouse_pos):
            game.selected_runner = game.runner_karlos
            game.character_chosen = True
            game.character_select = False


def draw_game(game):
    """Draw the main game screen during active gameplay."""
    current_time = time.time()
    game.screen.fill((255, 255, 255))

    game.skyline.draw(game.screen)
    game.footpath.draw(game.screen)
    game.runner.draw(game.screen)
    game.bird.draw(game.screen)

    draw_text(game.screen, f"Score: {game.score}", 35, 30, 30, (230, 70, 38))

    current_time = time.time()

    # If enough time has passed, schedule the first rain
    if game.next_rain_time is None and current_time - game.start_time > 30:
        game.next_rain_time = current_time + random.randint(10, 20)

    # Start rain if it's time
    if not game.weather_active and game.next_rain_time is not None and current_time >= game.next_rain_time:
        game.weather_active = True
        game.rain_fading_out = False
        game.rain_alpha = 0
        game.rain_start_time = current_time
        game.rain_end_time = current_time + random.randint(30, 40)

        game.spawned_umbrellas.clear()
        game.umbrella_spawn_times = [
            current_time + random.uniform(3, game.rain_end_time - current_time - 3)
            for _ in range(random.randint(2, 4))
        ]

    # Handle fade in
    if game.weather_active and not game.rain_fading_out:
        t = current_time - game.rain_start_time
        if t < game.rain_fade_duration:
            game.rain_alpha = int(255 * (t / game.rain_fade_duration))
        else:
            game.rain_alpha = 255

    # Handle fade out trigger
    if game.weather_active and not game.rain_fading_out and current_time >= game.rain_end_time:
        game.rain_fading_out = True
        game.rain_fade_start = current_time

    # Handle fade out
    if game.weather_active and game.rain_fading_out:
        t = current_time - game.rain_fade_start
        if t < game.rain_fade_duration:
            game.rain_alpha = int(255 * (1 - t / game.rain_fade_duration))
        else:
            game.rain_alpha = 0
            game.weather_active = False
            game.rain_fading_out = False
            game.next_rain_time = current_time + random.randint(30, 50)  # schedule next rain


def draw_game_over(game):
    """Draw the game over screen."""
    game.screen.fill((150, 150, 150))

    rect_width = int(WINDOW_WIDTH * 0.8)
    rect_height = int(WINDOW_HEIGHT * 0.75)
    rect_x = (WINDOW_WIDTH - rect_width) // 2
    rect_y = (WINDOW_HEIGHT - rect_height) // 2

    glass = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
    glass.fill((255, 255, 255, 60))
    game.screen.blit(glass, (rect_x, rect_y))

    pygame.draw.rect(game.screen, (180, 180, 180), (rect_x, rect_y, rect_width, rect_height), width=4, border_radius=20)

    draw_text(game.screen, "UH OH! IT LOOKS LIKE YOU'RE", 40, 260, 165, (230, 70, 38))
    draw_text(game.screen, "GOING TO BE LATE TO LECTURE...", 40, 240, 210, (230, 70, 38))
    draw_text(game.screen, "PRESS [ESC] TO QUIT (AND CANCEL CLASS)", 30, 250, 325, (255, 255, 255))
    draw_text(game.screen, "PRESS ANY KEY TO RUN AGAIN!", 30, 340, 380, (255, 255, 255))
    draw_text(game.screen, f"YOUR SCORE: {game.score}", 35, 240, 475, (230, 70, 38))
    draw_text(game.screen, f"HIGH SCORE: {get_highscore(game.score)}", 35, 660, 475, (230, 70, 38))

    if game.score == get_highscore(game.score):
        draw_text(game.screen, "CONGRATS ON BEATING THE HIGH SCORE!", 25, 330, 540, (255, 255, 255))
