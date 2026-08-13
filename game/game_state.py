import pygame


class GameState:

    def __init__(self):

        self.font = pygame.font.Font(None, 36)

        self.reset()

    def reset(self):

        self.lives = 3
        self.score = 0

        self.game_over = False
        self.won = False

    def lose_life(self):

        self.lives -= 1

        if self.lives <= 0:

            self.game_over = True

    def add_score(self, points):

        self.score += points

    def win(self):

        self.won = True

    def draw_hud(self, screen):

        lives_text = self.font.render(
            f"Lives: {self.lives}",
            True,
            (255, 255, 255)
        )

        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            (255, 255, 255)
        )

        screen.blit(
            lives_text,
            (20, 20)
        )

        screen.blit(
            score_text,
            (20, 60)
        )