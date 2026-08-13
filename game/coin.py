import pygame


class Coin:

    def __init__(self, x, y):

        self.radius = 12

        self.rect = pygame.Rect(
            x - self.radius,
            y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

        self.collected = False

        self.animation_timer = 0

    def collect(self):

        self.collected = True

    def draw(self, screen, camera):

        if self.collected:
            return

        self.animation_timer += 1

        # Fake rotation
        phase = self.animation_timer % 60

        if phase < 30:

            width = 24

        else:

            width = 12

        screen_rect = camera.apply(
            self.rect
        )

        center = screen_rect.center

        pygame.draw.ellipse(
            screen,
            (255, 215, 0),
            (
                center[0] - width // 2,
                center[1] - self.radius,
                width,
                self.radius * 2
            )
        )

        pygame.draw.ellipse(
            screen,
            (255, 240, 100),
            (
                center[0] - width // 2 + 3,
                center[1] - self.radius + 3,
                max(width - 6, 2),
                self.radius * 2 - 6
            )
        )