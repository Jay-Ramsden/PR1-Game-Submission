# CO452 Programming Concepts PR1 - Demilich's Retreat
# Art and Design by Jay Ramsden
# Programming by Alex Walker

import pygame
import random


def smallRender(player_x, player_y, wave, tile_size, bg, screen, clock):  # render and load the bg + aster each frame
    screen.fill((0, 0, 0))
    img = pygame.image.load(bg[wave])
    img = pygame.transform.scale(img, (tile_size * 15, tile_size * 15))
    screen.blit(img, (0, 0))
    img = pygame.image.load("red.jpg")
    img = pygame.transform.scale(img, (tile_size, tile_size))
    screen.blit(img, (int(player_x), int(player_y)))
    pygame.display.flip()
    clock.tick(60)


def waveTransition(player_x, player_y, wave, tile_size, bg, screen, clock):
    transition_backgrounds = ["entrance.png",
                              "dark terrain to light terrain.png",
                              "light to light.png",
                              "light terrain to dark terrain.png",
                              "to the demilich.png"]
    # move aster to the exit
    if wave >= 0:
        while player_y < tile_size * 14:
            player_y += tile_size / 16
            smallRender(player_x, player_y, wave, tile_size, bg, screen, clock)

    # walk aster through the transition between areas
    if wave == 0:
        player_x = 0
        player_y = tile_size * 7 // 2
        while player_x < tile_size * 14:
            player_x += tile_size / 16
            smallRender(player_x, player_y, wave, tile_size, transition_backgrounds, screen, clock)
    elif wave == 4:
        player_x = tile_size * 5
        player_y = 0
        while player_y < tile_size * 19 // 2:
            player_y += tile_size / 16
            smallRender(player_x, player_y, wave, tile_size, transition_backgrounds, screen, clock)
        while player_x < tile_size * 14:
            player_x += tile_size / 16
            smallRender(player_x, player_y, wave, tile_size, transition_backgrounds, screen, clock)
    else:
        player_x = tile_size * 7
        player_y = 0
        while player_y < tile_size * 14:
            player_y += tile_size / 16
            smallRender(player_x, player_y, wave, tile_size, transition_backgrounds, screen, clock)

    # move aster to the center of the new area
    wave += 1
    if wave == 5:
        player_x = 0
        player_y = tile_size * 4
        while player_x < tile_size * 3:
            player_x += tile_size / 16
            player_y += tile_size / 16
            smallRender(player_x, player_y, wave, tile_size, bg, screen, clock)
    else:
        player_y = 0
        while player_y < tile_size * 7:
            player_y += tile_size / 16
            smallRender(player_x, player_y, wave, tile_size, bg, screen, clock)
    return player_x, player_y  # and return control to the player


def main():
    # make a pygame window updating at 60 FPS
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    done = False

    tile_size = 40
    display_width = tile_size * 15
    display_height = tile_size * 15
    screen = pygame.display.set_mode((display_width, display_height))

    # list the backgrounds of each area, and the images for each magic spell
    backgrounds = ["",
                   "wave 1 - goblins 'the alley'.png",
                   "wave 2 - skeletons 'the catacombs'.png",
                   "wave 3 - gargoyles 'the standing stones'.png",
                   "wave 4 - bugbears 'the blacksmith's quarters'.png",
                   "wave 5 - demilich 'the retreat'.png"]

    magic_images = ["firebolt powerup tile.png",
                    "frostbite powerup tile.png",
                    "shocking grasp powerup tile.png",
                    "thunderclap powerup tile.png",
                    "cure wounds powerup tile.png",
                    "meteor swarm powerup tile.png"]

    # set attributes for the player
    player_x = tile_size * 7
    player_y = tile_size * 7
    walk_speed = tile_size / 16
    player_hp = 12
    max_hp = player_hp
    immunity_frames = 0

    # set attributes for the magic (-1 means no powerup)
    magic_type = -1
    magic_x, magic_y = 0, 0
    magic_collected = False

    # set attributes for aster's arrow
    fire_timer = 0
    arrow_position = [0, 0]
    arrow_vx, arrow_vy = 0, 0  # arrow velocities

    # set variables for enemies and waves
    living_enemies = []
    spawn_timer = 0
    spawns = 0
    wave_totals = [0, 15, 10, 8, 4, 1]
    wave = 1
    wave_length = wave_totals[wave]
    wave_done = False
    health_pools = [0, 1, 2, 5, 10, 20]

    # "constants" for enemies
    ENEMY_X = 0
    ENEMY_Y = 1
    HP = 2

    while not done:
        screen.fill((0, 0, 0))  # clear the screen
        img = pygame.image.load(backgrounds[wave])  # and load the background for this wave
        img = pygame.transform.scale(img, (display_width, display_height))
        screen.blit(img, (0, 0))  # blits start at the top corner

        spawn_timer += 1
        if spawns < wave_length and (spawn_timer == 75 + (wave * 10) or not random.randint(0, 300)):  # spawn an enemy
            spawn_points = [  # each line holds the data for a wave, each item holds a spawn point
                [],
                [[tile_size, tile_size * 3], [tile_size * 2, tile_size * 13], [tile_size * 14, tile_size * 7]],
                [[tile_size, tile_size * 3]],
                [[tile_size, tile_size * 3]],
                [[tile_size, tile_size * 9 // 2], [tile_size, tile_size * 19 // 2], [tile_size * 13, tile_size * 9 // 2], [tile_size * 13, tile_size * 19 // 2]],
                [[tile_size, tile_size * 3]]
            ]
            new_spawn = spawn_points[wave]  # get the spawn points for the wave
            new_spawn = new_spawn[random.randint(0, len(new_spawn) - 1)]  # and pick a random one from them
            new_spawn.append(health_pools[wave])
            living_enemies.append(new_spawn)
            spawn_timer = 0
            spawns += 1

        for enemy in living_enemies:
            img = pygame.image.load("blue.jpg")
            img = pygame.transform.scale(img, (tile_size, tile_size))
            x_dist = enemy[ENEMY_X] - player_x
            y_dist = enemy[ENEMY_Y] - player_y

            # make the enemy move - will move into a function to refactor
            if abs(x_dist) > tile_size * 3//5:
                enemy[ENEMY_X] += -1.5 if x_dist > 0 else 1.5

            if abs(y_dist) > tile_size * 3//5:
                enemy[ENEMY_Y] += -1.5 if y_dist > 0 else 1.5

            # if the player and enemy are colliding, damage the player and make aster immune for a short time
            if abs(x_dist) <= tile_size and abs(y_dist) <= tile_size and not immunity_frames:
                player_hp -= 1
                immunity_frames = 75
                done = (player_hp <= 0)
                player_x += -25 if x_dist > 0 else 25
                player_y += -25 if y_dist > 0 else 25

            # if the arrow hits the enemy, damage the enemy and remove the arrow
            if arrow_position[0] - tile_size <= enemy[ENEMY_X] <= arrow_position[0] + (tile_size // 2) and \
                    arrow_position[1] - tile_size <= enemy[ENEMY_Y] <= arrow_position[1] + (tile_size // 2):
                arrow_position = [0, 0]
                enemy[HP] -= 1
                if enemy[HP] <= 0:
                    living_enemies.remove(enemy)
                    wave_done = (spawns == wave_length and not living_enemies)  # if all the enemies have been killed

                    # if the player doesn't have a power up, roll for a power up being spawned
                    if not random.randint(0, 8 - wave) and not magic_collected:
                        magic_type = random.randint(0, 12) // 2
                        if magic_type > 4:  # make cure wounds appears twice as often as the damaging magic spells
                            magic_type -= 1
                        magic_x, magic_y = enemy[ENEMY_X], enemy[ENEMY_Y]

            else:
                screen.blit(img, (int(enemy[ENEMY_X]), int(enemy[ENEMY_Y])))

        if immunity_frames:
            immunity_frames -= 1

        # render power up if the player has one
        if magic_type > -1:
            img = pygame.image.load(magic_images[magic_type])
            img = pygame.transform.scale(img, (tile_size, tile_size))
            screen.blit(img, (int(magic_x), int(magic_y)))
            if magic_x - tile_size <= player_x <= magic_x + tile_size and \
                    magic_y - tile_size <= player_y <= magic_y + tile_size:
                magic_x, magic_y = (tile_size * 14, 0)
                magic_collected = True

        if wave_done:  # load and render the exit sign
            if wave != 5:
                img = pygame.image.load("exit arrow.png")
                img = pygame.transform.scale(img, (tile_size * 2, tile_size * 2))
                screen.blit(img, (tile_size * 13 // 2, tile_size * 25 // 2))
                if player_y >= tile_size * 23 // 2 and \
                        tile_size * 11 // 2 <= player_x <= tile_size * 17 // 2:  # move to the next map
                    player_x, player_y = waveTransition(player_x, player_y, wave, tile_size, backgrounds, screen, clock)
                    wave += 1
                    wave_length += 5
                    spawns = 0
                    wave_done = False
            else:
                pass  # note to self: make a cutscene here of aster getting the bow

        # render aster's health
        for i in range(max_hp // 2):
            if i*2 <= player_hp-2:
                img = pygame.image.load("heart.png")
            elif i*2 < player_hp:
                img = pygame.image.load("half heart.png")
            else:
                break
            img = pygame.transform.scale(img, (tile_size, tile_size))
            screen.blit(img, (2*i*tile_size//3, 0))

        # player movement + rendering
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_x -= walk_speed
        if keys[pygame.K_d]:
            player_x += walk_speed
        if keys[pygame.K_w]:
            player_y -= walk_speed
        if keys[pygame.K_s]:
            player_y += walk_speed

        if not fire_timer:  # check to see if an arrow can be fired
            if not arrow_position[0] and \
                    (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                fire_timer = 30
                arrow_position = [player_x + (tile_size // 4), player_y + (tile_size // 4)]
                arrow_vx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * walk_speed * 4
                arrow_vy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * walk_speed * 4
                if arrow_vx and arrow_vy:
                    arrow_vx /= 2**0.5
                    arrow_vy /= 2**0.5
        else:
            fire_timer -= 1

        # collision with the borders of the map
        if player_x < tile_size * 1.5:
            player_x = int(tile_size * 1.5)
        if player_x > display_width - tile_size * 2.5:
            player_x = int(display_height - tile_size * 2.5)

        if player_y < tile_size * 1.5:
            player_y = int(tile_size * 1.5)
        if player_y > display_height - tile_size * 2.5:
            player_y = int(display_height - tile_size * 2.5)

        # render the player - possibly have animations?
        img = pygame.image.load("red.jpg")
        img = pygame.transform.scale(img, (tile_size, tile_size))
        screen.blit(img, (int(player_x), int(player_y)))

        # arrow movement
        if arrow_position[0]:
            arrow_position[0] += arrow_vx
            arrow_position[1] += arrow_vy

            if arrow_position[0] < 0 or arrow_position[0] > display_width:
                arrow_position = [0, 0]

            if arrow_position[1] < 0 or arrow_position[1] > display_height:
                arrow_position = [0, 0]

            if arrow_position[0]:
                img = pygame.image.load("yellow.jpg")
                img = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
                screen.blit(img, (int(arrow_position[0]), int(arrow_position[1])))

        if magic_collected:
            if keys[pygame.K_SPACE]:
                magic_type = -1
                magic_collected = False
                pass  # power ups will go here

        # update at end of frame
        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    main()
