import pygame
from pathlib import Path


class Background:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        # =========================
        # Project Path
        # =========================

        project_folder = Path(__file__).resolve().parent.parent

        background_folder = (
            project_folder
            / "assets"
            / "images"
            / "background"
        )

        # =========================
        # Load Background
        # =========================

        self.background_image = pygame.image.load(
            str(
                background_folder
                / "full_background.png"
            )
        ).convert()

        self.background_image = pygame.transform.scale(
            self.background_image,
            (1636, 720)
        )

    def draw(self, screen, camera):

        # Sky
        screen.fill(
            (100, 180, 255)
        )

        # Parallax
        x = -camera.offset_x * 0.25

        screen.blit(
            self.background_image,
            (int(x), 0)
        )

        # Repeat background
        if (
            x
            + self.background_image.get_width()
            < screen.get_width()
        ):

            screen.blit(
                self.background_image,
                (
                    int(
                        x
                        + self.background_image.get_width()
                    ),
                    0
                )
            )