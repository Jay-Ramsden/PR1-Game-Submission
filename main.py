import pygame
import random


def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    done = False

    tile_size = 40
    display_width = tile_size * 15
    display_height = tile_size * 15
    screen = pygame.display.set_mode((display_width, display_height))

    player_x = tile_size * 7
    player_y = tile_size * 7
    walk_speed = tile_size / 16
    hp = 12
    max_hp = hp
    immunity_frames = 0

    magic_images = ["firebolt powerup tile.png",
                    "frostbite powerup tile.png",
                    "shocking grasp powerup tile.png",
                    "thunderclap powerup tile.png",
                    "cure wounds powerup tile.png",
                    "meteor swarm powerup tile.png"]
    magic_type = -1
    magic_x, magic_y = 0, 0
    magic_collected = False

    fire_timer = 0
    arrow_position = [0, 0]
    arrow_vx, arrow_vy = 0, 0  # arrow velocities

    enemies = []
    spawn_timer = 0
    spawns = 0
    wave_length = 20
    wave = 1
    health_pools = [1, 1, 3, 5, 20]

    while not done:
        screen.fill((0, 0, 0))  # clear the screen
        # note to self: add a proper background
        """img = pygame.image.load("lattice.jpg")
        img = pygame.transform.scale(img, (display_width, display_height))
        screen.blit(img, (0, 0))"""

        spawn_timer += 1
        if spawns < wave_length and (spawn_timer == 75-(wave*5) or not random.randint(0, 300)):
            spawn_points = [[0, tile_size * 7],
                            [tile_size * 7, 0],
                            [tile_size * 14, tile_size * 7],
                            [tile_size * 7, tile_size * 14]]
            enemy_type = random.randint(0, wave-1)
            spawns = 1 if enemy_type else random.randint(1, wave)
            new_spawn = spawn_points[random.randint(0, 3)]
            for i in range(spawns):
                new_spawn = spawn_points[random.randint(0, 3)]
                new_spawn.append(health_pools[enemy_type])
            # note to self: add offsets for enemy spawns
            enemies.append(new_spawn)
            spawn_timer = 0
            spawns += 1

        img = pygame.image.load("blue.jpg")
        img = pygame.transform.scale(img, (tile_size, tile_size))
        for enemy in enemies:
            enemy_x, enemy_y, enemy_hp = enemy[0], enemy[1], enemy[2]
            x_dist = enemy_x - player_x
            y_dist = enemy_y - player_y

            if abs(x_dist) > 15:
                enemy_x += -1.5 if x_dist > 0 else 1.5

            if abs(y_dist) > 15:
                enemy_y += -1.5 if y_dist > 0 else 1.5

            # enemy to player collision
            if abs(x_dist) <= tile_size and abs(y_dist) <= tile_size and not immunity_frames:
                hp -= 1
                immunity_frames = 45
                done = (hp <= 0)
                player_x += -25 if x_dist > 0 else 25
                player_y += -25 if y_dist > 0 else 25

            # bounding box collision, arrow to enemy
            if arrow_position[0] - tile_size <= enemy_x <= arrow_position[0] + (tile_size // 2) and \
                    arrow_position[1] - tile_size <= enemy_y <= arrow_position[1] + (tile_size // 2):
                arrow_position = [0, 0]
                enemy_hp -= 1
                if enemy_hp <= 0:
                    enemies.remove(enemy)

                    # power up spawning
                    if not random.randint(0, 7):
                        magic_type = random.randint(0, 12) // 2
                        if magic_type > 4:  # make cure wounds appear twice as often
                            magic_type -= 1
                        magic_x, magic_y = enemy_x, enemy_y

                if spawns == wave_length and not enemies:  # starts the next wave
                    spawns = 0
                    wave_length += 5
                    wave += 1
            else:
                screen.blit(img, (int(enemy_x), int(enemy_y)))
                enemy[0], enemy[1], enemy[2] = enemy_x, enemy_y, enemy_hp

        # render power up
        if magic_type+1:
            img = pygame.image.load(magic_images[magic_type])
            img = pygame.transform.scale(img, (tile_size, tile_size))
            screen.blit(img, (int(magic_x), int(magic_y)))
            if magic_x - tile_size <= player_x <= magic_x + tile_size and \
                    magic_y - tile_size <= player_y <= magic_y + tile_size:
                magic_x, magic_y = (tile_size * 14, 0)
                magic_collected = True

        # heart rendering
        for i in range(max_hp // 2):
            if i*2 <= hp-2:
                img = pygame.image.load("heart.png")
            elif i*2 < hp:
                img = pygame.image.load("heart_fade.png")
            else:
                break
            img = pygame.transform.scale(img, (tile_size, tile_size))
            screen.blit(img, (2*i*tile_size//3, 0))

        if immunity_frames:
            immunity_frames -= 1

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
        if player_x < tile_size:
            player_x = tile_size
        if player_x > display_width - tile_size * 2:
            player_x = display_width - tile_size * 2

        if player_y < tile_size:
            player_y = tile_size
        if player_y > display_height - tile_size * 2:
            player_y = display_height - tile_size * 2

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
