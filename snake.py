import pygame
import random
import math


pygame.init()


FPS = 60
UPS = 12
TABLO_HEIGHT = 47

fieldsize = field_width, field_height = 50, 40
size = width, height = 16 * field_width, 16 * field_height + TABLO_HEIGHT
block_size = block_width, block_height = 16, 16
clock = pygame.time.Clock()
window = pygame.display.set_mode((size))
score = 0
font = pygame.font.SysFont(
    ',sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheadingbolditalicsitkadisplaybolditalicsitkabannerbolditalic', 54)
sound = pygame.mixer.Sound('sounds/eat.wav')


class Background(pygame.sprite.Sprite):
    def __init__(self, size, color):
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.image.fill(color)
        self.image.blit(self.image, (0, 0))


class Block(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface((block_size))
        self.rect = self.image.get_rect()
        self.image.fill(color)
        self.image.blit(self.image, (10, 0))


class Head(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/head.png')
        self.image_up = self.image
        self.image_right = pygame.transform.rotate(self.image_up, 90)
        self.image_left = pygame.transform.rotate(self.image_up, 270)
        self.image_down = pygame.transform.rotate(self.image_up, 180)
        self.rect = self.image.get_rect()
        self.rect.x = 13 * block_width
        self.rect.y = 18 * block_height
        self.direction = 0

    def update(self, snake):
        if self.direction == 0:
            self.rect.y -= self.rect.height
            self.image = self.image_up
        if self.direction == 1:
            self.rect.x -= self.rect.width
            self.image = self.image_right
        if self.direction == 2:
            self.rect.y += self.rect.height
            self.image = self.image_down
        if self.direction == 3:
            self.rect.x += self.rect.width
            self.image = self.image_left

        for body_el in snake.sprites():
            if self != body_el and self.rect.colliderect(body_el.rect):
                exit()
        if not 0 <= self.rect.x < block_width * field_width or not 0 <= self.rect.y < block_height * field_height:
            exit()


class Body(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/body.png')
        self.image_turn_dr = pygame.image.load('images/body_turn_right.png')
        self.image_turn_ld = pygame.transform.rotate(self.image_turn_dr, -90)
        self.image_turn_ul = pygame.transform.rotate(self.image_turn_dr, -180)
        self.image_turn_ru = pygame.transform.rotate(self.image_turn_dr, -270)
        self.image_turn_dl = pygame.transform.flip(self.image_turn_dr, True, False)
        self.image_turn_lu = pygame.transform.flip(self.image_turn_ru, True, False)
        self.image_turn_ur = pygame.transform.flip(self.image_turn_ul, True, False)
        self.image_turn_rd = pygame.transform.flip(self.image_turn_ld, True, False)
        self.image_up = self.image
        self.image_right = pygame.transform.rotate(self.image_up, -90)
        self.image_left = pygame.transform.rotate(self.image_up, -270)
        self.image_down = pygame.transform.rotate(self.image_up, -180)
        self.image_tail_up = pygame.image.load('images/tail.png')
        self.image_tail_left = pygame.transform.rotate(self.image_tail_up, 90)
        self.image_tail_down = pygame.transform.rotate(self.image_tail_up, 180)
        self.image_tail_right = pygame.transform.rotate(self.image_tail_up, 270)
        self.direction = 0
        self.is_curved = 0
        self.next_direction = 0
        self.is_tail = 0

        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100

    def get_direction_to_body(self, body_part):
        if self.rect.y > body_part.rect.y:
            return 0
        if self.rect.y < body_part.rect.y:
            return 2
        if self.rect.x > body_part.rect.x:
            return 1
        if self.rect.x < body_part.rect.x:
            return 3


    def update(self, snake, *args):
        if self.is_tail:
            if self.direction == 0:
                self.image = self.image_tail_up
            if self.direction == 1:
                self.image = self.image_tail_left
            if self.direction == 2:
                self.image = self.image_tail_down
            if self.direction == 3:
                self.image = self.image_tail_right
            return
            
        if self.direction == self.next_direction:
            if self.direction == 0:
                self.image = self.image_up
            if self.direction == 1:
                self.image = self.image_left
            if self.direction == 2:
                self.image = self.image_down
            if self.direction == 3:
                self.image = self.image_right
        else:
            if self.direction == 0:
                if self.next_direction == 1:
                    self.image = self.image_turn_ru
                elif self.next_direction == 3:
                    self.image = self.image_turn_lu
            if self.direction == 1:
                if self.next_direction == 0:
                    self.image = self.image_turn_dl
                elif self.next_direction == 2:
                    self.image = self.image_turn_ul
            if self.direction == 2:
                if self.next_direction == 1:
                    self.image = self.image_turn_rd
                elif self.next_direction == 3:
                    self.image = self.image_turn_ld
            if self.direction == 3:
                if self.next_direction == 2:
                    self.image = self.image_turn_ur
                elif self.next_direction == 0:
                    self.image = self.image_turn_dr


class Snake(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.head = Head()
        self.head.add(self)
        body_el1 = Body()
        body_el1.rect.x = self.head.rect.x
        body_el1.rect.y = self.head.rect.y + self.head.rect.height
        body_el1.add(self)
        self.length = 2
        self.__direction = 0
        self.__new_direction = 0

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        if direction == 0 and self.__direction != 2:
            self.__new_direction = 0
        if direction == 1 and self.__direction != 3:
            self.__new_direction = 1
        if direction == 2 and self.__direction != 0:
            self.__new_direction = 2
        if direction == 3 and self.__direction != 1:
            self.__new_direction = 3

    def update(self, snake):
        self.__direction = self.__new_direction
        self.head.direction = self.__new_direction
        for num in range(len(self.sprites()) - 1, 0, -1):
            self.sprites()[num].rect = self.sprites()[num - 1].rect.copy()
        self.sprites()[1].direction = self.sprites()[0].direction
        for i in range(2, len(self.sprites())):
            self.sprites()[i].direction = self.sprites()[i].get_direction_to_body(self.sprites()[i - 1])
        for i in range(1, len(self.sprites()) - 1):
            self.sprites()[i].next_direction = self.sprites()[i + 1].direction
            self.sprites()[i].is_tail = 0
        self.sprites()[-1].is_tail = 1
        super().update(snake)

    def eat(self):
        global score
        sound.play()
        self.length += 1
        self.add(Body())
        score += 1


class InfoTablo(pygame.sprite.Sprite):
    def __init__(self, color, text_color):
        super().__init__()
        self.image = pygame.Surface((width, TABLO_HEIGHT))
        self.rect = self.image.get_rect()
        self.color = color
        self.text_color = text_color
        self.rect.y = field_height * block_height

    def update(self, score):
        self.image.fill(self.color)
        myhha = 1
        myha_txt = font.render('', True, (self.text_color))
        while myhha:
            myhha = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    myha_txt = font.render('R.I.P', True, (self.text_color))
                    break
        score_text = font.render('Score: {}'.format(
            score), True, (self.text_color))
        self.image.blit(score_text, (0, 0))
        self.image.blit(myha_txt, (300, 0))


apple = pygame.image.load('images/food.png')
myha_img = pygame.image.load('images/myha.png')


class Food(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = (field_width // 2 + field_width % 2) * block_width
        self.rect.y = (field_height // 2 + field_height % 2 - 3) * block_height

    def place_for(self, snake):
        collide = 1
        while collide:
            collide = 0
            self.rect.x = random.randrange(0, field_width) * block_width
            self.rect.y = random.randrange(0, field_height) * block_height
            for body_el in snake.sprites():
                if self.rect.colliderect(body_el.rect):
                    collide = 1
                    break

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, snake):
        if snake.head.rect.colliderect(self.rect):
            snake.eat()
            self.place_for(snake)


field = list()
# field[18][13]

# for i in range(0, field_height):
#     field.append([0] * field_width)
# from pprint import pprint
# pprint(field)
bg = Background(size, (0, 100, 0))
bg_group = pygame.sprite.Group(bg)
block = Block((50, 50, 255))
block_group = pygame.sprite.Group(block)
snake = Snake()
tablo_group = pygame.sprite.Group(InfoTablo((20, 10, 1), (124, 120, 184)))
food = Food(apple)
ttablo = InfoTablo((20, 10, 1), (124, 120, 184))

frame = 0

while True:
    frame += 1
    if frame == FPS:
        frame = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                food = Food(myha_img)
            if event.key == pygame.K_a:
                food = Food(apple)
            if event.key == pygame.K_RIGHT:
                snake.direction = 3
            if event.key == pygame.K_LEFT:
                snake.direction = 1
            if event.key == pygame.K_UP:
                snake.direction = 0
            if event.key == pygame.K_DOWN:
                snake.direction = 2
            if event.key == pygame.K_ESCAPE:
                exit()

    bg_group.draw(window)
    snake.draw(window)
    food.draw(window)
    tablo_group.draw(window)

    for i in range(1, UPS + 1):
        if frame == math.floor((FPS / UPS) * i):
            snake.update(snake)
            tablo_group.update(score)
            food.update(snake)

    clock.tick(FPS)
    pygame.display.update()
