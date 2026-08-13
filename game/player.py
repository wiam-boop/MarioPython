import pygame
from pathlib import Path

from game.image_utils import get_bottom_padding


class Player:

    def __init__(self, x, y):

        # =========================
        # Player Collision Size
        # =========================

        self.width = 50
        self.height = 70

        self.rect = pygame.Rect(
            x,
            y,
            self.width,
            self.height
        )

        # =========================
        # Movement
        # =========================

        self.speed = 5
        self.velocity_x = 0

        # =========================
        # Physics
        # =========================

        self.velocity_y = 0

        self.gravity = 0.5
        self.jump_strength = -12

        self.on_ground = False

        # =========================
        # Direction
        # =========================

        self.facing_right = True

        # =========================
        # Paths
        # =========================

        project_folder = Path(
            __file__
        ).resolve().parent.parent

        player_folder = (
            project_folder
            / "assets"
            / "images"
            / "player"
        )

        # =========================
        # Load Animations
        # =========================
        # Each animation returns both the frames
        # AND how many transparent pixels sit below
        # the actual artwork in each frame, so we
        # can cancel out that gap when drawing.

        self.idle_frames, self.idle_paddings = self.load_animation(
            player_folder / "idle"
        )

        self.run_frames, self.run_paddings = self.load_animation(
            player_folder / "run"
        )

        self.jump_frames, self.jump_paddings = self.load_animation(
            player_folder / "jump"
        )

        self.fall_frames, self.fall_paddings = self.load_animation(
            player_folder / "fall"
        )

        # =========================
        # Animation
        # =========================

        self.animation_frame = 0
        self.animation_timer = 0

    # =========================
    # Load Animation
    # =========================

    def load_animation(self, folder):

        frames = []
        paddings = []

        files = sorted(
            folder.glob("*.png"),
            key=lambda file: int(file.stem)
        )

        for file in files:

            image = pygame.image.load(
                str(file)
            ).convert_alpha()

            image = pygame.transform.smoothscale(
                image,
                (75, 100)
            )

            frames.append(image)

            paddings.append(
                get_bottom_padding(image)
            )

        return frames, paddings

    # =========================
    # Input
    # =========================

    def handle_input(self):

        keys = pygame.key.get_pressed()

        self.velocity_x = 0

        # Move left
        if keys[pygame.K_LEFT]:

            self.velocity_x = -self.speed

            self.facing_right = False

        # Move right
        if keys[pygame.K_RIGHT]:

            self.velocity_x = self.speed

            self.facing_right = True

        # Horizontal movement
        self.rect.x += self.velocity_x

        # =========================
        # Jump
        # =========================

        if (
            keys[pygame.K_SPACE]
            and self.on_ground
        ):

            self.velocity_y = self.jump_strength

            self.on_ground = False

            # Start jump animation
            self.animation_frame = 0
            self.animation_timer = 0

    # =========================
    # Gravity
    # =========================

    def apply_gravity(self):

        self.velocity_y += self.gravity

        if self.velocity_y > 15:

            self.velocity_y = 15

        self.rect.y += self.velocity_y

    # =========================
    # Platform Collision
    # =========================

    def check_collision(self, platforms):

        was_on_ground = self.on_ground

        self.on_ground = False

        for platform in platforms:

            if self.rect.colliderect(platform):

                # =========================
                # Falling
                # =========================

                if self.velocity_y > 0:

                    self.rect.bottom = platform.top

                    self.velocity_y = 0

                    self.on_ground = True

                # =========================
                # Hitting from Below
                # =========================

                elif self.velocity_y < 0:

                    self.rect.top = platform.bottom

                    self.velocity_y = 0

        # =========================
        # Just Landed
        # =========================

        if (
            self.on_ground
            and not was_on_ground
        ):

            self.animation_frame = 0
            self.animation_timer = 0

    # =========================
    # Enemy Collision
    # =========================

    def check_enemy_collision(self, enemies):

        for enemy in enemies:

            if not enemy.alive:

                continue

            if self.rect.colliderect(
                enemy.rect
            ):

                # =========================
                # Jump on Enemy
                # =========================

                if (
                    self.velocity_y > 0
                    and self.rect.bottom
                    <= enemy.rect.centery
                ):

                    enemy.alive = False

                    self.rect.bottom = enemy.rect.top

                    self.velocity_y = -8

                    self.on_ground = False

                    self.animation_frame = 0
                    self.animation_timer = 0

                # =========================
                # Hit From Side
                # =========================

                else:

                    return True

        return False

    # =========================
    # Collect Coins
    # =========================

    def collect_coins(self, coins):

        collected = 0

        for coin in coins:

            if coin.collected:

                continue

            if self.rect.colliderect(
                coin.rect
            ):

                coin.collect()

                collected += 1

        return collected

    # =========================
    # Get Current Animation
    # =========================

    def get_animation(self):

        # =========================
        # Jump
        # =========================

        if self.velocity_y < 0:

            return self.jump_frames, self.jump_paddings

        # =========================
        # Fall
        # =========================

        if self.velocity_y > 2:

            return self.fall_frames, self.fall_paddings

        # =========================
        # Run
        # =========================

        if self.velocity_x != 0:

            return self.run_frames, self.run_paddings

        # =========================
        # Idle
        # =========================

        return self.idle_frames, self.idle_paddings

    # =========================
    # Update Animation
    # =========================

    def update_animation(self):

        # =========================
        # Air Animation
        # =========================
        # Keep jump/fall on one frame

        if not self.on_ground:

            self.animation_frame = 0

            self.animation_timer = 0

            return

        # =========================
        # Ground Animation
        # =========================

        frames, paddings = self.get_animation()

        if len(frames) <= 1:

            self.animation_frame = 0

            return

        self.animation_timer += 1

        if self.animation_timer >= 8:

            self.animation_timer = 0

            self.animation_frame += 1

            if self.animation_frame >= len(frames):

                self.animation_frame = 0

    # =========================
    # Update
    # =========================

    def update(self, platforms):

        self.handle_input()

        self.apply_gravity()

        self.check_collision(
            platforms
        )

        self.update_animation()

    # =========================
    # Draw
    # =========================

    def draw(self, screen, camera):

        frames, paddings = self.get_animation()

        if not frames:

            return

        # =========================
        # Select Frame
        # =========================

        # While in the air:
        # always use the first frame

        if not self.on_ground:

            index = 0

        else:

            index = (
                self.animation_frame % len(frames)
            )

        image = frames[index]
        padding = paddings[index]

        # =========================
        # Face Left
        # =========================

        if not self.facing_right:

            image = pygame.transform.flip(
                image,
                True,
                False
            )

        # =========================
        # Camera
        # =========================

        screen_rect = camera.apply(
            self.rect
        )

        image_rect = image.get_rect(
            midbottom=screen_rect.midbottom
        )

        # =========================
        # Cancel out transparent padding
        # below the artwork so the feet
        # visually touch the ground instead
        # of floating above it
        # =========================

        image_rect.y += padding

        # =========================
        # Draw
        # =========================

        screen.blit(
            image,
            image_rect
        )