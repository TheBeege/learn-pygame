#!/usr/bin/env python

import pygame

from game.coin import Coin
from game.colors import BLACK, GREEN
from game.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, COIN_STARTING_VELOCITY, PLAYER_STARTING_LIVES, \
    COIN_OFFSCREEN_BUFFER_DISTANCE, COIN_ACCELERATION, PLAYER_VELOCITY
from game.player import Player


def prepare_assets():
    # Prepare background music
    pygame.mixer.music.load('src/assets/music.wav')
    pygame.mixer.music.play(-1, 0.0)

    # Prepare fonts
    title_font = pygame.font.Font('src/assets/AttackGraffiti.ttf', 32)

    get_coin_sound = pygame.mixer.Sound('src/assets/sound_1.wav')
    miss_coin_sound = pygame.mixer.Sound('src/assets/sound_2.wav')
    miss_coin_sound.set_volume(0.9)

    return title_font, get_coin_sound, miss_coin_sound


def main():
    pygame.init()
    clock = pygame.time.Clock()

    score = 0
    player_lives = PLAYER_STARTING_LIVES

    # Prepare display
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Feed the dragon!')

    (
        title_font,
        get_coin_sound,
        miss_coin_sound
    ) = prepare_assets()

    title_text = title_font.render(
        'Feed the dragon!',
        True,
        GREEN,
    )
    title_text_rect = title_text.get_rect()
    title_text_rect.centerx = WINDOW_WIDTH // 2
    title_text_rect.y = 10

    player = Player(
        x=0,
        y=WINDOW_HEIGHT//2,
        get_coin_sound=get_coin_sound,
        move_speed=PLAYER_VELOCITY,
        lives=PLAYER_STARTING_LIVES,
    )
    coin = Coin(
        miss_coin_sound,
        COIN_OFFSCREEN_BUFFER_DISTANCE,
        COIN_STARTING_VELOCITY,
        COIN_ACCELERATION,
    )

    # Run game loop
    running = True
    while running:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

        if player_lives > 0:
            display_surface.fill(BLACK)

            player.move()
            score = player.update(coin, score)
            player.render(display_surface)

            player_lives = coin.update(player_lives)
            coin.render(display_surface)

            score_text = title_font.render(
                f'Score: {score}',
                True,
                GREEN,
            )
            score_text_rect = score_text.get_rect()
            score_text_rect.topleft = (10, 10)

            lives_text = title_font.render(
                f'Lives: {player_lives}',
                True,
                GREEN,
            )
            lives_text_rect = lives_text.get_rect()
            lives_text_rect.left = WINDOW_WIDTH - 125
            lives_text_rect.top = 10

            display_surface.blit(title_text, title_text_rect)
            display_surface.blit(score_text, score_text_rect)
            display_surface.blit(lives_text, lives_text_rect)
        else:
            game_over_text = title_font.render(
                'GAME OVER',
                True,
                GREEN,
            )
            game_over_text_rect = game_over_text.get_rect()
            game_over_text_rect.centerx = WINDOW_WIDTH//2
            game_over_text_rect.centery = WINDOW_HEIGHT//2
            display_surface.blit(game_over_text, game_over_text_rect)

            final_score_text = title_font.render(
                f'You scored {score} points',
                True,
                GREEN,
            )
            final_score_text_rect = final_score_text.get_rect()
            final_score_text_rect.centerx = WINDOW_WIDTH//2
            final_score_text_rect.centery = WINDOW_HEIGHT * 2 // 3
            display_surface.blit(final_score_text, final_score_text_rect)

            restart_text = title_font.render(
                'Press spacebar to restart',
                True,
                GREEN,
            )
            restart_text_rect = restart_text.get_rect()
            restart_text_rect.y = WINDOW_HEIGHT * 3 // 4
            restart_text_rect.centerx = WINDOW_WIDTH//2
            display_surface.blit(restart_text, restart_text_rect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                coin.reset()
                player_lives = 5
                score = 0

        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
