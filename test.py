import pygame


pygame.init()


FPS = 60
size = 640, 480


class Background(pygame.sprite.Sprite):
    def __init__(self, size, color1, color2):
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        top_part = pygame.Surface((self.rect.width, self.rect.height // 2))
        bottom_part = pygame.Surface((self.rect.width, self.rect.height // 2))
        top_part.fill(color1)
        bottom_part.fill(color2)
        self.image.blit(top_part, (0, 0))
        self.image.blit(bottom_part, (0, self.rect.height // 2))

    def update(self):
        pass


font = pygame.font.SysFont('comicsansms', 36)
text = font.render('Hello', True, (255, 50, 50))
text_rect = text.get_rect()
clock = pygame.time.Clock()
window = pygame.display.set_mode((size))
bg = Background(size, (50, 50, 255), (255, 255, 0))
orc = pygame.image.load('img.png')
orc_rect = orc.get_rect()
orc = pygame.transform.smoothscale(
    orc, (orc_rect.width // 2, orc_rect.height // 2))
orc_rect = orc.get_rect()
orc_rect.x = 100
orc_rect.y = 100

bg_group = pygame.sprite.Group(bg)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    bg_group.draw(window)
    window.blit(text, text_rect)
    text_rect.x += 1
    orc_rect.x += 1
    # orc_rect.y += 1
    window.blit(orc, orc_rect)
    clock.tick(FPS)
    pygame.display.update()
    bg_group.update()
