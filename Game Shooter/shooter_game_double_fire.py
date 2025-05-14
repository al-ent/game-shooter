from pygame import *
from random import randint

# Load functions for working with fonts separately
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)

# Background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# We need these pictures:
img_back = "galaxy.jpg"  # Game background
img_bullet = "bullet.png"  # Bullet
img_hero = "fighting_jet_up.png"  # Character
img_enemy = "fighting_jet_down.png"  # Regular enemy
img_enemy2 = "bomber_aircraft.png"  # Special enemy

# Game variables
score = 0
goal = 150
lost = 0
max_lost = 10

# Parent class
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Player
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

# Enemy
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, enemy_type=1):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.enemy_type = enemy_type
        self.health = 1 if enemy_type == 1 else 3

    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

# Bullet
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

# Create window
win_width = 1200
win_height = 700
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# Create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 100, 80, randint(1, 5), enemy_type=1)
    monsters.add(monster)

bullets = sprite.Group()

finish = False
run = True

# Timer for special enemy
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
        window.blit(background, (0, 0))

        # Display score and missed
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # Update and draw sprites
        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        # Spawn special enemy
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            special_enemy = Enemy(img_enemy2, randint(80, win_width - 80), -40, 400, 240, randint(2, 4), enemy_type=2)
            monsters.add(special_enemy)

        # Collision: bullets hit enemies
        collides = sprite.groupcollide(monsters, bullets, False, True)
        for enemy in collides:
            enemy.health -= 1
            if enemy.health <= 0:
                if enemy.enemy_type == 1:
                    score += 1
                elif enemy.enemy_type == 2:
                    score += 3
                enemy.kill()

                # Respawn a new enemy
                if randint(1, 4) == 1:
                    new_enemy = Enemy(img_enemy2, randint(80, win_width - 80), -40, 400, 240, randint(2, 4), enemy_type=2)
                else:
                    new_enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 100, 80, randint(1, 5), enemy_type=1)
                monsters.add(new_enemy)

        # Lose condition
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (400, 300))

        # Win condition
        if score >= goal:
            finish = True
            window.blit(win, (400, 300))
        display.update()
    time.delay(50)
