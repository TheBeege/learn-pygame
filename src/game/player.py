import pygame

from game.coin import Coin
from game.constants import WINDOW_HEIGHT, WINDOW_WIDTH


class Player:
    def __init__(
            self,
            x: int,
            y: int,
            get_coin_sound: pygame.mixer.Sound,
            move_speed: int,
            lives: int,
            enable_horizontal_movement: bool = False,
    ):
        self.player_image = pygame.image.load("src/assets/dragon_right.png")
        self.player_rect = self.player_image.get_rect()
        self.player_rect.topleft = (x, y)
        self.x_velocity = 0
        self.y_velocity = 0
        self.move_speed = move_speed
        self.height = self.player_rect.height
        self.width = self.player_rect.width
        self.get_coin_sound = get_coin_sound
        self.lives = lives
        self.enable_horizontal_movement = enable_horizontal_movement

    def render(self, display_surface):
        display_surface.blit(
            self.player_image,
            self.player_rect,
        )

    def update(self, coin: Coin, score: int):
        if self.player_rect.x + self.x_velocity >= 0 and \
                self.player_rect.x + self.width + self.x_velocity < WINDOW_WIDTH:
            self.player_rect.x += self.x_velocity

        if self.player_rect.y + self.y_velocity >= 0 and \
                self.player_rect.y + self.height + self.y_velocity < WINDOW_HEIGHT:
            self.player_rect.y += self.y_velocity

        if self.player_rect.colliderect(coin.coin_rect):
            self.get_coin_sound.play()
            coin.reset(is_success=True)
            score += 10

        return score

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.y_velocity = -self.move_speed
        elif keys[pygame.K_DOWN]:
            self.y_velocity = self.move_speed
        else:
            self.y_velocity = 0

        if self.enable_horizontal_movement:
            if keys[pygame.K_LEFT]:
                self.x_velocity = -self.move_speed
            elif keys[pygame.K_RIGHT]:
                self.x_velocity = self.move_speed
            else:
                self.x_velocity = 0
