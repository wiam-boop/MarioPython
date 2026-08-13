import pygame


class Camera:
    def __init__(self, width):
        self.offset_x = 0
        self.width = width

    def update(self, player):
        target_x = player.rect.centerx - 400

        self.offset_x = target_x

        # منع الكاميرا من الخروج عن بداية المرحلة
        if self.offset_x < 0:
            self.offset_x = 0

        # منعها من الخروج عن نهاية المرحلة
        max_offset = self.width - 1000

        if self.offset_x > max_offset:
            self.offset_x = max_offset

    def apply(self, rect):
        return rect.move(-self.offset_x, 0)