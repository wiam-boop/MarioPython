import pygame
from pathlib import Path


class SoundManager:

    def __init__(self):

        # =========================
        # Project Path
        # =========================

        project_folder = (
            Path(__file__)
            .resolve()
            .parent
            .parent
        )

        sounds_folder = (
            project_folder
            / "assets"
            / "sounds"
        )

        # =========================
        # Sound Effects
        # =========================

        self.coin = pygame.mixer.Sound(
            str(sounds_folder / "coin.wav")
        )

        self.enemy_hit = pygame.mixer.Sound(
            str(sounds_folder / "enemy_hit.wav")
        )

        self.stomp_enemy = pygame.mixer.Sound(
            str(sounds_folder / "stomp_enemy.wav")
        )

        self.win = pygame.mixer.Sound(
            str(sounds_folder / "win.wav")
        )

        self.lose = pygame.mixer.Sound(
            str(sounds_folder / "lose.wav")
        )

        # =========================
        # Volume
        # =========================

        self.coin.set_volume(0.5)

        self.enemy_hit.set_volume(0.6)

        self.stomp_enemy.set_volume(0.6)

        self.win.set_volume(0.7)

        self.lose.set_volume(0.7)

        # =========================
        # Background Music
        # =========================

        self.background_music = (
            sounds_folder
            / "background.wav"
        )

    # =========================
    # Start Background Music
    # =========================

    def play_background(self):

        pygame.mixer.music.load(
            str(self.background_music)
        )

        pygame.mixer.music.set_volume(0.25)

        pygame.mixer.music.play(
            loops=-1
        )