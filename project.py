from pygame import *
from random import *

font.init()
font = font.Font(None, 36)


win_width = 700
win_height = 500
FPS = 60

score = 0
points = []

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
        if self.rect.x < -self.width:
            self.rect.x = win_width + randint(0, 200)
            self.rect.y = randint(200, 350)
            for _ in range(randint(1, 2)):
                x = self.rect.x + randint(10, self.width-10)
                y = self.rect.y - 10
                points.add(Point(x, y))

class Point(GameSprite):
    def __init__(self, x, y):
        super().__init__((0, 0, 0), x, y, 14, 14) 
        self.radius = 7

    def draw(self):
        draw.circle(window, (0, 0, 0), (self.rect.x, self.rect.y), self.radius)


ground = GameSprite(colorb, 0, win_height - 120, win_width, 120)
player = Player(colorb, 100, win_height - 200, 50, 70, 5)

points = sprite.Group()
platforms = sprite.Group()

for p in range(3):
    x = win_width + randint(0, 200)  
    y = randint(300, 250)            
    width = randint(100, 350)
    new_platform = Platform(colorb, x, y, width, 30, 4)
    platforms.add(new_platform)

clock = time.Clock()

run = True
while run:
    window.fill((255, 255, 255))
    for e in event.get():
        if e.type == QUIT:
            run = False

    for p in points:
        if player.rect.colliderect(p.rect):
            points.remove(p)
            score += 1

    platforms.update()
    platforms.draw(window)
    for p in points:
        p.draw()
    player.update()
    ground.reset()
    player.reset()
    window.blit(font.render(f"Score: {score}", True, (0,0,0)), (10,10))
    display.update()
    clock.tick(FPS)
