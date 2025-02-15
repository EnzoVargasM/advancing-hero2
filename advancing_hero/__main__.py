import pygame

import settings
import gamemodes
import os

pygame.init()

clock = pygame.time.Clock()
global current_gamemode
global game_admin
pygame.mixer.set_num_channels(10)

screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))

pygame.display.set_caption(settings.TITLE)

pygame.event.post(pygame.event.Event(pygame.USEREVENT, customType='title_screen'))

pygame.mixer.init()

run = True

while run:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.USEREVENT:
            if event.customType == 'init_level':
                current_gamemode = gamemodes.modes['level_main']
                game_admin = current_gamemode(screen, event.level, settings, event.scroll_mode)
            if event.customType == 'title_screen':
                # Change ost
                ost = os.path.abspath('advancing_hero/songs/title_screen_song.mp3')
                pygame.mixer.music.load(ost)
                pygame.mixer.music.set_volume(0.7)
                pygame.mixer.music.play(-1)

                current_gamemode = gamemodes.modes['title_screen']
                game_admin = current_gamemode(screen, settings)
            if event.customType == 'journey_select':
                current_gamemode = gamemodes.modes['journey_select']
                game_admin = current_gamemode(screen, settings)
            if event.customType == 'world_map':
                current_gamemode = gamemodes.modes['world_map']
                game_admin = current_gamemode(screen, settings)
            if event.customType == 'character_select':
                current_gamemode = gamemodes.modes['character_select']
                game_admin = current_gamemode(screen, settings)
            if event.customType == 'end_game':
                current_gamemode = gamemodes.modes['end_game']
                game_admin = current_gamemode(screen, settings)
            if event.customType == 'win_game':
                current_gamemode = gamemodes.modes['win_game']
                game_admin = current_gamemode(screen, settings)

    game_admin.loop(events)

    pygame.display.update()

    clock.tick(settings.FPS)

pygame.quit()
