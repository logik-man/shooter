from pygame import *
from random import randint


class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed


    def fire(self):
        bullet = Bullet("coin.png", self.rect.centerx, self.rect.y, 12, 25, 15)
        bullets.add(bullet)



class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            global lost
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(0, WIDTH - self.rect.width)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


WIDTH = 800
HEIGHT = 600
lost = 0
score = 0

window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Space Shooter")

background = transform.scale(image.load("back.jpg"), (WIDTH, HEIGHT))

player = Player("rocket.png", 320, 500, 70, 100, 7)

enemies = sprite.Group()
enemy = Enemy("asteroid.png", 30, -120, 70, 70, 3)
enemies.add(enemy)
enemy = Enemy("asteroid.png", 200, 60, 70, 70, 3)
enemies.add(enemy)
enemy = Enemy("asteroid.png", 450, 0, 70, 70, 3)
enemies.add(enemy)

bullets = sprite.Group()

font.init()
font1 = font.SysFont("times new roman", 80)
font2 = font.SysFont("comic sans ms", 20)

game = True
run = True
delay = 0
clock = time.Clock()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    window.blit(background, (0, 0))
    if run:
        if delay > 0:
            delay -= 1
        keys = key.get_pressed()
        if keys[K_SPACE]:
            if delay == 0:
                player.fire()
                delay = 5
        player.update()
        enemies.update()
        bullets.update()
        text = font2.render("Рахунок: " + str(score), True, (255, 255, 255))
        window.blit(text, (10, 5))
        text = font2.render("Пропущено: " + str(lost), True, (255, 255, 255))
        window.blit(text, (10, 30))
        collides = len(sprite.groupcollide(enemies, bullets, True, True))
        for _ in range(collides):
            enemy = Enemy("asteroid.png", randint(0, WIDTH - 70), -50, 70, 70, 3)
            enemies.add(enemy)
            score += 1
        if lost > 5 or sprite.spritecollide(player, enemies, False):
            run = False
            lost_text = font1.render("Game over!", True, (180, 50, 50))
        if score > 15:
            run = False
            lost_text = font1.render("You win!", True, (50, 180, 50))
        enemies.draw(window)
        player.reset()
        bullets.draw(window)
    else:
        window.blit(lost_text, (240, 220))
    display.update()
    clock.tick(60)