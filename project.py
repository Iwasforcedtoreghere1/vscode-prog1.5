from pygame import *
from random import *

win_width = 700
win_height = 500
FPS = 60

colorb = (0, 0, 0)

window = display.set_mode((win_width, win_height))
display.set_caption("«Bad apple animation» ahh platformer")

class GameSprite(sprite.Sprite):
    def __init__(self, color, x, y, width, height, speed=0):
        super().__init__()
        self.image = Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, color, x, y, width, height, speed):
        super().__init__(color, x, y, width, height, speed)
        self.vel_y = 0
        self.on_ground = True

    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.on_ground:
            self.vel_y = -15
            self.on_ground = False
        self.vel_y += 1
        self.rect.y += self.vel_y
        if self.rect.bottom >= ground.rect.top:
            self.rect.bottom = ground.rect.top
            self.vel_y = 0
            self.on_ground = True
        for p in platforms:
            if sprite.collide_rect(self, p) and self.vel_y >= 0:
                if self.rect.bottom > p.rect.top and self.rect.bottom < p.rect.centery + 10:
                    self.rect.bottom = p.rect.top       
                    self.vel_y = 0
                    self.on_ground = True        

class Platform(GameSprite):
    def __init__(self, color, x, y, width, height, speed):
        super().__init__(color, x, y, width, height, speed)
        
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < 0 - self.width:
            self.rect.x = win_width + 10

ground = GameSprite(colorb, 0, win_height - 120, win_width, 120)
player = Player(colorb, 100, win_height - 200, 50, 70, 5)


platform_excist = False
platforms = sprite.Group()
    
def create_platform():
    platform = Platform(colorb, win_width, 290, 250, 30, 4)
    return platform

clock = time.Clock()

run = True
while run:
    window.fill((255, 255, 255))
    for e in event.get():
        if e.type == QUIT:
            run = False

    if platform_excist == False:
        new_platform = create_platform()
        platform_excist = True
        platforms.add(new_platform)
    if platform_excist:
        new_platform.update()
        new_platform.reset()

    
    player.update()
    ground.reset()
    player.reset()
    display.update()
    clock.tick(FPS)
