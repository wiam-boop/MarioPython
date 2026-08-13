import pygame
from pathlib import Path

from game.enemy import Enemy
from game.coin import Coin
from game.goal import Goal


class Level:

    def __init__(self):

        # =========================
        # Level Size
        # =========================

        self.width = 2800

        # =========================
        # Asset Paths
        # =========================

        project_folder = Path(
            __file__
        ).resolve().parent.parent

        assets_folder = (
            project_folder
            / "assets"
            / "images"
        )

        # =========================
        # Ground Image
        # =========================

        self.ground_image = pygame.image.load(
            str(
                assets_folder
                / "ground_tile.png"
            )
        ).convert_alpha()

        self.ground_image = pygame.transform.scale(
            self.ground_image,
            (300, 80)
        )

        # =========================
        # Castle Image
        # =========================

        self.castle_image = pygame.image.load(
            str(
                assets_folder
                / "castle.png"
            )
        ).convert_alpha()

        self.castle_image = pygame.transform.smoothscale(
            self.castle_image,
            (400, 420)
        )

        # =========================
        # Castle Position
        # =========================
        # Computed from its size so it sits
        # flush on the ground and never spills
        # past the end of the level, no matter
        # what size is chosen above.
        #
        # If the castle still looks slightly
        # above or below the ground, adjust
        # CASTLE_GROUND_OFFSET below:
        # - positive number -> moves it DOWN
        # - negative number -> moves it UP

        CASTLE_GROUND_OFFSET = 0

        castle_width = self.castle_image.get_width()
        castle_height = self.castle_image.get_height()

        ground_top = 520
        level_margin = 0

        self.castle_x = 2820

        self.castle_y = (
            ground_top
            - castle_height
            + CASTLE_GROUND_OFFSET
        )

        # =========================
        # Make sure the level is long
        # enough for the castle to fully
        # fit, however big it is
        # =========================

        min_width = (
            self.castle_x
            + castle_width
            + level_margin
        )

        if min_width > self.width:

            self.width = min_width

        # =========================
        # Platforms
        # =========================
        # NOTE: the castle sits at x=2620
        # (see draw() below), so no floating
        # platform should extend past that
        # point or it will visually clip
        # through the castle.

        self.platforms = [

            # Main ground
            pygame.Rect(
                0,
                520,
                self.width,
                80
            ),

            pygame.Rect(
                300,
                420,
                150,
                30
            ),

            pygame.Rect(
                550,
                350,
                150,
                30
            ),

            pygame.Rect(
                800,
                450,
                180,
                30
            ),

            pygame.Rect(
                1100,
                380,
                150,
                30
            ),

            pygame.Rect(
                1350,
                300,
                180,
                30
            ),

            pygame.Rect(
                1650,
                420,
                150,
                30
            ),

            pygame.Rect(
                1900,
                350,
                200,
                30
            ),

            pygame.Rect(
                2250,
                430,
                150,
                30
            ),

            # Shortened + moved so it ends
            # well before the castle (2620)
            pygame.Rect(
                2450,
                330,
                150,
                30
            ),
        ]

        # =========================
        # Enemies
        # =========================

        self.enemies = [

            Enemy(
                650,
                475,
                500,
                750
            ),

            Enemy(
                1150,
                335,
                1100,
                1250
            ),

            Enemy(
                1750,
                475,
                1600,
                1850
            ),

            Enemy(
                2300,
                385,
                2200,
                2450
            ),
        ]

        # =========================
        # Coins
        # =========================

        self.coins = [

            Coin(350, 380),
            Coin(600, 310),
            Coin(850, 410),
            Coin(1150, 340),
            Coin(1400, 260),
            Coin(1700, 380),
            Coin(1950, 310),
            Coin(2300, 390),
            Coin(2550, 290),
        ]

        # =========================
        # Goal
        # =========================

        self.goal = Goal(
            2920,
            400
        )

    # =========================
    # Update
    # =========================

    def update(self):

        for enemy in self.enemies:

            if enemy.alive:

                enemy.update()

    # =========================
    # Draw
    # =========================

    def draw(self, screen, camera):

        # =========================
        # Draw Repeating Ground
        # =========================

        ground_y = 520

        tile_width = self.ground_image.get_width()

        for x in range(
            0,
            self.width,
            tile_width
        ):

            ground_rect = pygame.Rect(
                x,
                ground_y,
                tile_width,
                80
            )

            screen_rect = camera.apply(
                ground_rect
            )

            screen.blit(
                self.ground_image,
                screen_rect
            )

        # =========================
        # Draw Platforms
        # (using the same ground texture
        # instead of a plain green rect)
        # =========================

        tile_w = self.ground_image.get_width()
        tile_h = self.ground_image.get_height()

        for platform in self.platforms[1:]:

            screen_rect = camera.apply(
                platform
            )

            # =========================
            # Clip so the texture doesn't
            # spill outside the platform
            # =========================

            old_clip = screen.get_clip()
            screen.set_clip(screen_rect)

            # =========================
            # Tile the texture, aligned to
            # the bottom of the platform so
            # it visually matches the ground
            # =========================

            start_y = screen_rect.bottom - tile_h

            for tx in range(
                screen_rect.left,
                screen_rect.right,
                tile_w
            ):

                screen.blit(
                    self.ground_image,
                    (tx, start_y)
                )

            screen.set_clip(old_clip)

        # =========================
        # Draw Enemies
        # =========================

        for enemy in self.enemies:

            if enemy.alive:

                enemy.draw(
                    screen,
                    camera
                )

        # =========================
        # Draw Coins
        # =========================

        for coin in self.coins:

            coin.draw(
                screen,
                camera
            )

        # =========================
        # Draw Castle
        # =========================

        castle_rect = pygame.Rect(
            self.castle_x,
            self.castle_y,
            self.castle_image.get_width(),
            self.castle_image.get_height()
        )

        screen_rect = camera.apply(
            castle_rect
        )

        screen.blit(
            self.castle_image,
            screen_rect
        )