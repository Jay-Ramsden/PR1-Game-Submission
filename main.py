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
    fire_timer = 0
    arrow_position = [0, 0]
    dx, dy = 0, 0  # actually arrow velocities

    enemies = []
    spawn_timer = 0

    while not done:
        screen.fill((0, 0, 0))  # clear the screen - if any black peeks through, something's probably not rendering
        # add a proper background

        if spawn_timer == 100 or not random.randint(0, 100):
            spawns = [[0, tile_size * 7], [tile_size * 7, 0], [tile_size * 14, tile_size * 7],
                      [tile_size * 7, tile_size * 14]]
            spawn = random.randint(0, 3)
            # add offsets for enemy spawns
            enemies.append(spawns[spawn])
            spawn_timer = 0

        pieceImg = pygame.image.load("blue.jpg")
        pieceImg = pygame.transform.scale(pieceImg, (tile_size, tile_size))
        for enemy in enemies:
            enemy_x, enemy_y = enemy[0], enemy[1]
            x_dist = enemy_x - player_x
            y_dist = enemy_y - player_y

            if abs(x_dist) > 15:
                if x_dist > 0:
                    enemy_x -= 1.5
                else:
                    enemy_x += 1.5

            if abs(y_dist) > 15:
                if y_dist > 0:
                    enemy_y -= 1.5
                else:
                    enemy_y += 1.5

            # bounding box collision, arrow to enemy
            if arrow_position[0] - (tile_size // 2) <= enemy_x <= arrow_position[0] + tile_size and \
                    arrow_position[1] - tile_size <= enemy_y <= arrow_position[1] + (tile_size // 2):
                arrow_position = [0, 0]
                enemies.remove(enemy)
            else:
                screen.blit(pieceImg, (int(enemy_x), int(enemy_y)))
                enemy[0], enemy[1] = enemy_x, enemy_y

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_x -= 2
        if keys[pygame.K_d]:
            player_x += 2
        if keys[pygame.K_w]:
            player_y -= 2
        if keys[pygame.K_s]:
            player_y += 2
        if not fire_timer:
            if not arrow_position[0] and \
                    (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                fire_timer = 30
                arrow_position = [player_x + (tile_size // 4), player_y + (tile_size // 4)]
                dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
                dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 5
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

        # rendering for the player
        pieceImg = pygame.image.load("red.jpg")
        pieceImg = pygame.transform.scale(pieceImg, (tile_size, tile_size))
        screen.blit(pieceImg, (player_x, player_y))

        if arrow_position[0]:
            arrow_position[0] += dx
            arrow_position[1] += dy

            if arrow_position[0] < 0 or arrow_position[0] > display_width:
                arrow_position[0] = 0

            if arrow_position[1] < 0 or arrow_position[1] > display_height:
                arrow_position[0] = 0

            if arrow_position[0]:
                pieceImg = pygame.image.load("yellow.jpg")
                pieceImg = pygame.transform.scale(pieceImg, (tile_size // 2, tile_size // 2))
                screen.blit(pieceImg, (arrow_position[0], arrow_position[1]))

        # update at end of frame
        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    main()
