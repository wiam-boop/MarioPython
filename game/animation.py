import pygame


class Animation:

    def __init__(self, frames, speed=0.1):

        self.frames = frames
        self.speed = speed

        self.current_frame = 0
        self.timer = 0

    def update(self, dt):

        if len(self.frames) <= 1:
            return

        self.timer += dt

        if self.timer >= self.speed:

            self.timer = 0

            self.current_frame += 1

            if self.current_frame >= len(self.frames):

                self.current_frame = 0

    def get_frame(self):

        return self.frames[self.current_frame]