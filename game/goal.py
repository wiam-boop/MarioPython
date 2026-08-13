import pygame


class Goal:

    def __init__(self, x, y):

        # =========================
        # Visual Flag Pole
        # (this is only used for drawing)
        # =========================

        self.rect = pygame.Rect(
            x,
            y,
            30,
            120
        )

        # =========================
        # Collision Area
        # =========================
        # This is intentionally much taller than
        # the visible screen (extends far above
        # the sky and below the ground). This way,
        # reaching this x position ALWAYS triggers
        # the win, no matter how high the player
        # jumps when passing it - no more missed
        # collisions / glitches.

        self.collision_rect = pygame.Rect(
            x,
            -3000,
            30,
            6000
        )

        self.reached = False

    def check_collision(self, player):

        if self.collision_rect.colliderect(
            player.rect
        ):

            self.reached = True

            return True

        return False

    def draw(self, screen, camera):

        screen_rect = camera.apply(
            self.rect
        )

        # Pole
        pygame.draw.rect(
            screen,
            (230, 230, 230),
            screen_rect
        )

        # Pole top
        pygame.draw.circle(
            screen,
            (255, 220, 50),
            (
                screen_rect.centerx,
                screen_rect.top
            ),
            6
        )

        # Flag
        flag_points = [

            (
                screen_rect.right,
                screen_rect.top
            ),

            (
                screen_rect.right + 55,
                screen_rect.top + 20
            ),

            (
                screen_rect.right,
                screen_rect.top + 40
            )
        ]

        pygame.draw.polygon(
            screen,
            (220, 50, 50),
            flag_points
        )