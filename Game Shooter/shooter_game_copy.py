#Create your own shooter

from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)

img_back = "galaxy.jpg"
img_hero = "fighting_jet_up.png"
img_bullet = "bullet.png"
img_enemy = "fighting_jet_down.png"
img_enemy2 = "bomber_aircraft.png"

score = 0
goal = 100
lost = 0
max_lost = 5


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, enemy_type=1):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.enemy_type = enemy_type
        self.health = 2 if enemy_type == 1 else 4

    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

ufos = sprite.Group()
for i in range(1, 6):
    fighting_jet_down = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 7))
    ufos.add(fighting_jet_down)

bullets = sprite.Group()

finish = False
run = True

spawn_timer = 0
spawn_interval = 100

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background, (0,0))
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        ufos.update()
        bullets.update()

        ship.reset()
        ufos.draw(window)
        bullets.draw(window)

        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            special_enemy = Enemy(img_enemy2, randint(80, win_width - 80), -40, 200, 160, randint(2, 4), enemy_type=2)
            ufos.add(special_enemy)

        collides = sprite.groupcollide(ufos, bullets, True, True)
        for c in collides:
            c.health -= 1
            if c.health <= 0:
                if c.enemy_type == 1:
                    score += 1
                elif c.enemy_type == 2:
                    score += 3
                c.kill()
                if randint(1, 4) == 1:
                    new_enemy = Enemy(img_enemy2, randint(80, win_width - 80), -40, 200, 160, randint(2, 4), enemy_type=2)
                else:
                    new_enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(2, 4), enemy_type=1)
                ufos.add(new_enemy)

        if sprite.spritecollide(ship, ufos, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

#test
        display.update()
    time.delay(50)
