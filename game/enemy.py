import pygame


class Enemy:

    def __init__(
        self,
        x,
        y,
        left_limit,
        right_limit
    ):

        self.width = 45
        self.height = 45

        self.rect = pygame.Rect(
            x,
            y,
            self.width,
            self.height
        )

        self.speed = 2

        self.direction = 1

        self.left_limit = left_limit
        self.right_limit = right_limit

        self.alive = True

    def update(self):

        self.rect.x += (
            self.speed *
            self.direction
        )

        if self.rect.left <= self.left_limit:

            self.rect.left = self.left_limit

            self.direction = 1

        if self.rect.right >= self.right_limit:

            self.rect.right = self.right_limit

            self.direction = -1

    def draw(self, screen, camera):

        screen_rect = camera.apply(
            self.rect
        )

        # Body
        pygame.draw.rect(
            screen,
            (130, 70, 35),
            screen_rect,
            border_radius=10
        )

        # Eyes
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (
                screen_rect.x + 13,
                screen_rect.y + 15
            ),
            6
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (
                screen_rect.x + 32,
                screen_rect.y + 15
            ),
            6
        )

        pygame.draw.circle(
            screen,
            (20, 20, 20),
            (
                screen_rect.x + 13,
                screen_rect.y + 15
            ),
            3
        )

        pygame.draw.circle(
            screen,
            (20, 20, 20),
            (
                screen_rect.x + 32,
                screen_rect.y + 15
            ),
            3
        )

        # Feet
        pygame.draw.rect(
            screen,
            (80, 40, 20),
            (
                screen_rect.x + 5,
                screen_rect.bottom - 8,
                15,
                8
            )
        )

        pygame.draw.rect(
            screen,
            (80, 40, 20),
            (
                screen_rect.right - 20,
                screen_rect.bottom - 8,
                15,
                8
            )
        )