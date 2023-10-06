import pygame
import pickle
from os import path
from pygame.locals import *

# Initialize program
pygame.init()

# Assign FPS a value
clock = pygame.time.Clock()  # adjust frame rate to 60 fps.
fps = 60

# Set up a 1000x1000 pixel display with caption
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

# define game variables
tile_size = 50
main_menu = True
controls = False
dead_state = 0
level = 1
max_levels = 8
score = 0
timer = 10800
luigi_char = False
boy_char = False
char = False


# load images
menu_bg = pygame.image.load('img/bg.jpg')
sun_img = pygame.image.load('img/sun.png')
gameplay_bg = pygame.image.load('img/sky.png')
gameplay_bg = pygame.transform.scale(gameplay_bg, (1000, 1000))
display_controls = pygame.image.load('img/controls.jpg')

start_img = pygame.image.load('img/start_btn.png')
start_img = pygame.transform.scale(start_img, (279, 126))
exit_img = pygame.image.load('img/exit_btn.png')
exit_img = pygame.transform.scale(exit_img, (279, 126))
controls_image = pygame.image.load('img/controls_btn.png')
controls_image = pygame.transform.scale(controls_image, (279, 126))
mute_on_img = pygame.image.load('img/mute_on.png')
mute_on_img = pygame.transform. scale(mute_on_img, (40, 40))
mute_off_img = pygame.image.load('img/mute_off.png')
mute_off_img = pygame.transform. scale(mute_off_img, (40, 40))
restart_img = pygame.image.load('img/restart_btn.png')
restart_img = pygame.transform.scale(restart_img, (110, 55))
back_img = pygame.image.load('img/back.btn.png')
back_img = pygame.transform.scale(back_img, (70, 70))
end_exit_img = pygame.image.load('img/exit_btn.png')
end_exit_img = pygame.transform.scale(end_exit_img, (110, 77))
luigi_img = pygame.image.load('img/luigi1.PNG')
luigi_img = pygame.transform.scale(luigi_img, (150, 150))
boy_img = pygame.image.load('img/boy1.png')
boy_img = pygame.transform.scale(boy_img, (150, 150))
char_bg = pygame.image.load('img/background1.png')
char_bg = pygame.transform.scale(char_bg, (1000, 1000))

# set colours
white = (255, 255, 255)
blue = (0, 0, 255)
Purple = (100, 50, 200)
red = (200, 0, 0)

# set fonts
font = pygame.font.SysFont('couriernew', 100)  #couriernew,constantia
font2 = pygame.font.SysFont('couriernew', 30)
font3 = pygame.font.SysFont('Bauhaus', 100)
font_score = pygame.font.SysFont('Bauhaus 93', 30)


# load sounds
pygame.mixer.music.load('img/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)

level_up_fx = pygame.mixer.Sound('img/level_up.wav')
click_fx = pygame.mixer.Sound('img/click.wav')
coin_fx = pygame.mixer.Sound('img/coin.wav')  # loads coin's sound
coin_fx.set_volume(0.5)  # volume of coin effect is now 50% of ir.
jump_fx = pygame.mixer.Sound('img/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('img/game_over.wav')
game_over_fx.set_volume(0.5)

#pygame.mixer.music.load('img/music.wav')
#pygame.mixer.music.play(-1, 0.0, 5000)



# set functions
def reset_level(level):
    player.reset(100, screen_height - 130)
    blob_group.empty()
    lava_group.empty()
    door_group.empty()
    coin_group.empty()
    platform_group.empty()
    #load in level data and create world
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    # create another instance to represent the score when level is reset
    score_coin = Coin(tile_size // 2, tile_size // 2)
    coin_group.add(score_coin)

    return world

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))



#Classes
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        screen.blit(self.image, self.rect)

        return action

class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')

        row_count = 0
        for row in data:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 2:
                        img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 3:
                        blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
                        blob_group.add(blob)
                    if tile == 4:
                        platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                        platform_group.add(platform)
                    if tile == 5:
                        platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                        platform_group.add(platform)
                    if tile == 6:
                        lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                        lava_group.add(lava)
                    if tile == 7:
                        coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                        coin_group.add(coin)
                    if tile == 8:
                        door = Door(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                        door_group.add(door)
                    col_count += 1
                row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Player():
    def __init__(self, x, y):
        self.reset(x, y)


    def update(self, dead_state):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if dead_state == 0:
            #get keypresses
            key = pygame.key.get_pressed()
            if (key[pygame.K_SPACE] or key[pygame.K_w] or key[pygame.K_UP]) and self.jumped == False and self.in_air == False:
                self.vel_y = -15
                self.jumped = True
                jump_fx.play()
            if key[pygame.K_SPACE] or key[pygame.K_w] or key[pygame.K_UP] == False:
                self.jumped = False
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT] or key[pygame.K_d]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if (key[pygame.K_LEFT] or key[pygame.K_a]) == False and (key[pygame.K_RIGHT] or key[pygame.K_d]) == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]


            #handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]


            #add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y += 0.5
                if self.vel_y > 15:
                    self.vel_y = 15
            dy += self.vel_y


            #check for collision
            self.in_air = True
            for tile in world.tile_list:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if player is jumping and hitting a block above
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if player is falling and hitting a block below
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                dead_state = -1
                game_over_fx.play()

            # check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                dead_state = -1
                game_over_fx.play()

            # check for collision with doors
            if pygame.sprite.spritecollide(self, door_group, False):
                dead_state = 1
                level_up_fx.play()
            # check for collision with platforms
            for platform in platform_group:
                # collision in the x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # collision in the y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < 30:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    # check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < 30:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    # move sideways with the platform
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction
            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        # death animation
        elif dead_state == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 4


        #draw player onto screen
        screen.blit(self.image, self.rect)

        return dead_state

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        if luigi_char == True:
            for num in range(1, 5):
                img_right = pygame.image.load(f'img/luigi{num}.PNG')
                img_right = pygame.transform.scale(img_right, (40, 80))
                img_left = pygame.transform.flip(img_right, True, False)
                self.images_right.append(img_right)
                self.images_left.append(img_left)
                self.dead_image = pygame.image.load('img/ghost.png')
                self.image = self.images_right[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.width = self.image.get_width()
                self.height = self.image.get_height()
                self.vel_y = 0
                self.jumped = False
                self.direction = 0
        if boy_char == True:
            for num in range(1, 5):
                img_right = pygame.image.load(f'img/boy{num}.png')
                img_right = pygame.transform.scale(img_right, (40, 80))
                img_left = pygame.transform.flip(img_right, True, False)
                self.images_right.append(img_right)
                self.images_left.append(img_left)
                self.dead_image = pygame.image.load('img/ghost.png')
                self.image = self.images_right[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.width = self.image.get_width()
                self.height = self.image.get_height()
                self.vel_y = 0
                self.jumped = False
                self.direction = 0





class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/door.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/coin.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size //2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/platform.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y


    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if self.move_counter > 50:
            self.move_direction *= -1
            self.move_counter *= -1


# instances and related to classes

platform_group = pygame.sprite.Group()
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()

# Create another instance of coin to represent score in screen
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

#load in level data and create world

if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)




# create button instances
start_button = Button(screen_width // 2 - (279//2), screen_height // 2 - 163, start_img)
exit_button = Button(screen_width // 2 - (279//2), screen_height // 2 + 220, exit_img)
controls_button = Button(screen_width // 2 - (279//2), screen_height // 2 + 28, controls_image)
mute_on_button = Button(screen_width // 2 + 455, screen_height // 2 + 455, mute_on_img)
mute_off_button = Button(screen_width // 2 + 400, screen_height // 2 + 455, mute_off_img)
restart_button = Button(screen_width // 2 - 50, screen_height // 2 - 50, restart_img)
back_button = Button(50, screen_height - 75, back_img)
end_exit_button = Button(screen_width // 2 - 50, screen_height // 2 + 25, end_exit_img)
boy_button = Button(250, 500 , boy_img)
luigi_button = Button(600, 500 , luigi_img)

# beginning game loop
run = True
while run:
    clock.tick(fps)

    screen.blit(menu_bg, (0, 0))
    screen.blit(sun_img, (850, 50))

    if main_menu == True and controls == False and char == False:
        if exit_button.draw():
            click_fx.play()
            run = False

        if controls_button.draw():
            click_fx.play()
            #controls should be displayed
            controls = True

        if start_button.draw():
            char = True
            click_fx.play()


        if mute_on_button.draw():
            click_fx.play()
            # music should be muted
            pygame.mixer.music.pause()


        if mute_off_button.draw():
            click_fx.play()
            # music should be unmuted
            pygame.mixer.music.unpause()

    if controls == True:
        # controls display
        screen.blit(display_controls, (0, 0))
        if back_button.draw():
            click_fx.play()
            main_menu = True
            controls = False
        # when clicked character buttons appear and when clicked game starts.
    if char == True:
        screen.blit(char_bg, (0, 0))
        draw_text('Select Character', font3, white,screen_width // 2 - (279//2) - 150, screen_height // 2 -200)
        if back_button.draw():
            click_fx.play()
            main_menu = True
            char = False
        if luigi_button.draw():
            click_fx.play()
            luigi_char = True
            player = Player(100, screen_height - 130) # Now instance of player is created only when luigi  character is chosen, just after setting 'luigi_char' as true.
            main_menu = False
        if boy_button.draw():
            click_fx.play()
            boy_char = True
            player = Player(100, screen_height - 130)
            main_menu = False

    #mute and unmute music with keys.
    key = pygame.key.get_pressed()
    if key[pygame.K_m] == True:
        pygame.mixer.music.pause()

    if key[pygame.K_n] ==  True:
        pygame.mixer.music.unpause()



    if main_menu == False:
        screen.blit(gameplay_bg, (0, 0))

        world.draw()

        blob_group.draw(screen)
        lava_group.draw(screen)
        door_group.draw(screen)
        coin_group.draw(screen)
        platform_group.draw(screen)




        dead_state = player.update(dead_state)



        if mute_on_button.draw():
            click_fx.play()
            # music should be muted
            pygame.mixer.music.pause()


        if mute_off_button.draw():
            click_fx.play()
            # music should be unmuted
            pygame.mixer.music.unpause()

        # if player is alive
        if dead_state == 0:
            blob_group.update()
            platform_group.update()
            draw_text('Level:' + str(level), font2, white, screen_width // 2 - 65, 10)
            draw_text('X ' + str(score), font_score, (255, 215, 0), tile_size - 10, 9)
            draw_text('Time left:' + str(timer // 60), font2, white, screen_width // 2 + 250, 10)
            timer -= 1
            if timer <= 0:
                game_over_fx.play()
                dead_state = -1




            # Score updates instantly
            # check if coin has been collected by player
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                coin_fx.play()




        # if player has died
        if dead_state == -1:
            draw_text('Game Over!', font, Purple, (screen_width // 2) - 275, 300)
            draw_text('SCORE: ' + str(score), font_score, Purple, 445, 500)
            draw_text('Level:' + str(level), font2, white, screen_width // 2 - 65, 10)
            pygame.mixer.music.pause()
            if timer <= 0:
                draw_text("Time's Up", font2, red, screen_width // 2 - 75, 550)
            if restart_button.draw():
                click_fx.play()
                pygame.mixer.music.unpause()
                world = reset_level(level)
                dead_state = 0
                score = 0
                if timer <= 0:
                    timer = 10800



        # if player has completed the level
        if dead_state == 1:
            # reset game and go to next level
            level += 1
            score += 1
            if level <= max_levels:
                # reset level
                world = reset_level(level)
                dead_state = 0
                timer = 10800
            # if player has completed all levels
            else:
                draw_text('YOU WIN!', font, blue, (screen_width // 2) - 200, 350)
                if restart_button.draw():
                    click_fx.play()
                    level = 1
                    # reset level
                    world = reset_level(level)
                    dead_state = 0
                    score = 0
                    timer = 10800
                if end_exit_button.draw():
                    run = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()