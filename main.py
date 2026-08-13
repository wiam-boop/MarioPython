import pygame
import sys

from settings import (
    WIDTH,
    HEIGHT,
    FPS,
    TITLE
)

from game.player import Player
from game.level import Level
from game.camera import Camera
from game.game_state import GameState
from game.background import Background
from game.sound_manager import SoundManager


# =========================
# Initialize Pygame
# =========================

pygame.init()

# =========================
# Window
# =========================

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    TITLE
)

clock = pygame.time.Clock()


# =========================
# Sound Manager
# =========================

sound = SoundManager()

# Start background music
sound.play_background()


# =========================
# Create Game
# =========================

def create_game():

    player = Player(
        100,
        400
    )

    level = Level()

    camera = Camera(
        level.width
    )

    background = Background(
        level.width,
        HEIGHT
    )

    return (
        player,
        level,
        camera,
        background
    )


# =========================
# Game Objects
# =========================

player, level, camera, background = create_game()

game_state = GameState()

running = True


# =========================
# Main Game Loop
# =========================

while running:

    # =========================
    # Events
    # =========================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # =========================
        # Restart
        # =========================

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:

                if (
                    game_state.game_over
                    or game_state.won
                ):

                    (
                        player,
                        level,
                        camera,
                        background
                    ) = create_game()

                    game_state.reset()

                    # Restart background music
                    sound.play_background()

    # =========================
    # WIN SCREEN
    # =========================

    if game_state.won:

        screen.fill(
            (50, 180, 100)
        )

        font = pygame.font.Font(
            None,
            80
        )

        text = font.render(
            "YOU WIN!",
            True,
            (255, 255, 255)
        )

        text_rect = text.get_rect(
            center=(
                WIDTH // 2,
                HEIGHT // 2 - 40
            )
        )

        screen.blit(
            text,
            text_rect
        )

        restart_font = pygame.font.Font(
            None,
            40
        )

        restart_text = restart_font.render(
            "Press R to Restart",
            True,
            (255, 255, 255)
        )

        restart_rect = restart_text.get_rect(
            center=(
                WIDTH // 2,
                HEIGHT // 2 + 50
            )
        )

        screen.blit(
            restart_text,
            restart_rect
        )

        pygame.display.flip()

        clock.tick(FPS)

        continue

    # =========================
    # GAME OVER SCREEN
    # =========================

    if game_state.game_over:

        screen.fill(
            (20, 20, 20)
        )

        font = pygame.font.Font(
            None,
            80
        )

        text = font.render(
            "GAME OVER",
            True,
            (255, 255, 255)
        )

        text_rect = text.get_rect(
            center=(
                WIDTH // 2,
                HEIGHT // 2 - 40
            )
        )

        screen.blit(
            text,
            text_rect
        )

        restart_font = pygame.font.Font(
            None,
            40
        )

        restart_text = restart_font.render(
            "Press R to Restart",
            True,
            (255, 255, 255)
        )

        restart_rect = restart_text.get_rect(
            center=(
                WIDTH // 2,
                HEIGHT // 2 + 50
            )
        )

        screen.blit(
            restart_text,
            restart_rect
        )

        pygame.display.flip()

        clock.tick(FPS)

        continue

    # =========================
    # UPDATE
    # =========================

    player.update(
        level.platforms
    )

    # =========================
    # Enemy Collision
    # =========================

    # Remember enemy states
    enemies_before = [
        enemy.alive
        for enemy in level.enemies
    ]

    player_hit = player.check_enemy_collision(
        level.enemies
    )

    # =========================
    # Enemy Stomp Sound
    # =========================

    enemies_after = [
        enemy.alive
        for enemy in level.enemies
    ]

    for before, after in zip(
        enemies_before,
        enemies_after
    ):

        if before and not after:

            sound.stomp_enemy.play()

    # =========================
    # Player Hit Enemy
    # =========================

    if player_hit:

        # Play hit sound
        sound.enemy_hit.play()

        game_state.lose_life()

        # =========================
        # Respawn Player
        # =========================

        player.rect.x = 100
        player.rect.y = 400

        player.velocity_y = 0

        # =========================
        # Game Over Sound
        # =========================

        if game_state.game_over:

            # Stop background music
            pygame.mixer.music.stop()

            # Play lose sound
            sound.lose.play()

    # =========================
    # Update Level
    # =========================

    level.update()

    # =========================
    # Collect Coins
    # =========================

    coins_collected = player.collect_coins(
        level.coins
    )

    if coins_collected > 0:

        game_state.add_score(
            coins_collected * 10
        )

        # Play coin sound
        for _ in range(coins_collected):

            sound.coin.play()

    # =========================
    # Goal
    # =========================

    if level.goal.check_collision(
        player
    ):

        # Only play once
        if not game_state.won:

            game_state.win()

            # Stop background music
            pygame.mixer.music.stop()

            # Play win sound
            sound.win.play()

    # =========================
    # Camera
    # =========================

    camera.update(
        player
    )

    # =========================
    # DRAW
    # =========================

    # Background
    background.draw(
        screen,
        camera
    )

    # Level
    level.draw(
        screen,
        camera
    )

    # Player
    player.draw(
        screen,
        camera
    )

    # HUD
    game_state.draw_hud(
        screen
    )

    # =========================
    # Update Display
    # =========================

    pygame.display.flip()

    # =========================
    # FPS
    # =========================

    clock.tick(FPS)


# =========================
# Quit
# =========================

pygame.mixer.music.stop()

pygame.quit()

sys.exit()