from random import randint

import pygame

from game import constants


class Coin:
    def __init__(
            self,
            miss_coin_sound: pygame.mixer.Sound,
            offscreen_buffer_distance: int,
            move_speed: int,
            acceleration: float,
    ):
        self.coin_image = pygame.image.load("src/assets/coin.png")
        self.coin_rect = self.coin_image.get_rect()
        self.move_speed = move_speed
        self.miss_coin_sound = miss_coin_sound
        self.offscreen_buffer_distance = offscreen_buffer_distance
        self.acceleration = acceleration
        self.reset()

    def render(self, display_surface):
        display_surface.blit(
            self.coin_image,
            self.coin_rect,
        )

    def update(self, lives):
        self.coin_rect.x -= self.move_speed
        if self.coin_rect.right < 0:
            self.miss_coin_sound.play()
            self.reset()
            lives -= 1
        return lives

    def reset(self, is_success: bool = False):
        self.coin_rect.right = constants.WINDOW_WIDTH + self.offscreen_buffer_distance
        self.coin_rect.y = randint(50, constants.WINDOW_HEIGHT - self.coin_rect.height)
        if is_success:
            self.move_speed += self.acceleration
