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
    hp = 30
    max_hp = hp
    immunity_frames = 0

    fire_timer = 0
    arrow_position = [0, 0]
    dx, dy = 0, 0  # actually arrow velocities

    enemies = []
    spawn_timer = 0
    spawns = 0
    wave_length = 20
    wave = 1

    while not done:
        screen.fill((0, 0, 0))  # clear the screen - if any black peeks through, something's probably not rendering
        # add a proper background
        """img = pygame.image.load("lattice.jpg")
        img = pygame.transform.scale(img, (display_width, display_height))
        screen.blit(img, (0, 0))"""

        spawn_timer += 1
        if spawns < wave_length and (spawn_timer == 70 or not random.randint(0, 300)):
            spawn_points = [[0, tile_size * 7],
                            [tile_size * 7, 0],
                            [tile_size * 14, tile_size * 7],
                            [tile_size * 7, tile_size * 14]]
            new_spawn = spawn_points[random.randint(0, 3)]
            new_spawn.append(6)  # replace with enemy hp once more types are added
            # add offsets for enemy spawns
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
                hp -= random.randint(2, 8)
                immunity_frames = 45
                done = (hp <= 0)
                player_x += -25 if x_dist > 0 else 25
                player_y += -25 if y_dist > 0 else 25

            # bounding box collision, arrow to enemy
            if arrow_position[0] - tile_size <= enemy_x <= arrow_position[0] + (tile_size // 2) and \
                    arrow_position[1] - tile_size <= enemy_y <= arrow_position[1] + (tile_size // 2):
                arrow_position = [0, 0]
                fire_timer = 30
                enemy_hp -= random.randint(4, 10)
                if enemy_hp <= 0:
                    enemies.remove(enemy)
                if spawns == wave_length and not enemies:  # starts the next wave
                    spawns = 0
                    wave_length += 5
                    wave += 1
            else:
                screen.blit(img, (int(enemy_x), int(enemy_y)))
                enemy[0], enemy[1], enemy[2] = enemy_x, enemy_y, enemy_hp

        for i in range(max_hp // 5):
            if i*5 <= hp-5:
                img = pygame.image.load("heart.png")
            elif i*5 < hp:
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

        if not fire_timer:  # arrow checks
            if not arrow_position[0] and \
                    (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                arrow_position = [player_x + (tile_size // 4), player_y + (tile_size // 4)]
                dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * walk_speed * 4
                dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * walk_speed * 4
                if dx and dy:
                    dx /= 2**0.5
                    dy /= 2**0.5
        else:
            fire_timer -= 1

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

        # janky arrow movement
        if arrow_position[0]:
            arrow_position[0] += dx
            arrow_position[1] += dy

            if arrow_position[0] < 0 or arrow_position[0] > display_width:
                arrow_position = [0, 0]
                fire_timer = 30

            if arrow_position[1] < 0 or arrow_position[1] > display_height:
                arrow_position = [0, 0]
                fire_timer = 30

            if arrow_position[0]:
                img = pygame.image.load("yellow.jpg")
                img = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
                screen.blit(img, (int(arrow_position[0]), int(arrow_position[1])))

        # update at end of frame
        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    main()
