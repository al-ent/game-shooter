from pygame import *
from random import randint

# Load fonts
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
boost_sound = mixer.Sound('fire.ogg')  # Tambahkan file boost.ogg
bonus_fly_sound = mixer.Sound('helicopter.ogg')  # Tambahkan file bonus_fly.ogg


# Images
img_back = "war_sky.jpg"
img_bullet = "bullet.png"
img_hero = "fighting_jet_up.png"
img_enemy = "fighting_jet_down.png"
img_enemy2 = "bomber_aircraft.png"
img_bonus = "chinook.png"

# Game variables
score = 0
goal = 125
lost = 0
max_lost = 10

# Sprite classes
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

class Player(GameSprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.default_speed = self.speed
        self.boost_end_time = 0

    def update(self):
        if time.get_ticks() > self.boost_end_time:
            self.speed = self.default_speed
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

    def boost_speed(self, duration):
        self.boost_end_time = time.get_ticks() + duration
        self.speed = self.default_speed + 15

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

class BonusEnemy(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width:
            self.kill()

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

# Window
win_width = 1200
win_height = 700
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# Helper functions
def draw_text(surface, text, font, color, x, y):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(x, y))
    surface.blit(rendered, rect)

def main_menu():
    menu = True
    while menu:
        window.blit(background, (0, 0))
        draw_text(window, "SKY SHOOTER", font1, (255, 255, 255), win_width // 2, 200)
        draw_text(window, "Press ENTER to Start", font2, (255, 255, 255), win_width // 2, 400)
        for e in event.get():
            if e.type == QUIT:
                quit()
            if e.type == KEYDOWN:
                if e.key == K_RETURN:
                    menu = False
        display.update()
        time.delay(50)

def game_over_screen(win_text):
    global score, lost, finish
    window.blit(background, (0, 0))
    window.blit(win_text, (400, 300))
    draw_text(window, "Press R to Restart or ESC to Quit", font2, (255, 255, 255), win_width // 2, 400)
    display.update()
    waiting = True
    while waiting:
        for e in event.get():
            if e.type == QUIT:
                quit()
            if e.type == KEYDOWN:
                if e.key == K_r:
                    score = 0
                    lost = 0
                    finish = False
                    monsters.empty()
                    bullets.empty()
                    for i in range(5):
                        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 100, 80, randint(1, 5), enemy_type=1)
                        monsters.add(monster)
                    waiting = False
                elif e.key == K_ESCAPE:
                    quit()
        time.delay(50)


# Start menu
main_menu()

# Create player and groups
ship = Player(img_hero, 5, win_height - 100, 80, 100, 20)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 100, 80, randint(1, 5), enemy_type=1)
    monsters.add(monster)
bullets = sprite.Group()
bonus_enemies = sprite.Group()

# Game loop variables
finish = False
run = True
paused = False
spawn_timer = 0
bonus_timer = 0
bonus_interval = 300

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not paused:
                fire_sound.play()
                ship.fire()
            if e.key == K_p:
                paused = not paused

    if not finish:
        if not paused:
            window.blit(background, (0, 0))

            
            draw_text(window, f"Score: {score}", font2, (255, 255, 255), 80, 20)
            draw_text(window, f"Missed: {lost}", font2, (255, 255, 255), 80, 50)
            draw_text(window, "Press P to Pause", font2, (200, 200, 200), win_width - 140, 30)

            ship.update()
            monsters.update()
            bullets.update()
            bonus_enemies.update()

            ship.reset()
            monsters.draw(window)
            bullets.draw(window)
            bonus_enemies.draw(window)

            #spawn_timer += 1
            #if spawn_timer >= spawn_interval:
            #    spawn_timer = 0
            #    special_enemy = Enemy(img_enemy2, randint(80, win_width - 80), -40, 400, 240, randint(2, 4), enemy_type=2)
            #    monsters.add(special_enemy)
            bonus_timer += 1
            if bonus_timer >= bonus_interval:
                bonus_timer = 0
                bonus_enemy = BonusEnemy(img_bonus, -60, randint(50, 300), 60, 60, 4)
                bonus_enemies.add(bonus_enemy)
                bonus_fly_sound.play(-1)

            if len(bonus_enemies) == 0:
                bonus_fly_sound.stop()

            collides = sprite.groupcollide(monsters, bullets, False, True)
            for enemy in collides:
                enemy.health -= 1
                if enemy.health <= 0:
                    score += 3 if enemy.enemy_type == 2 else 1
                    enemy.kill()

                    # Buat musuh baru
                    enemy_image = img_enemy2 if randint(1, 4) == 1 else img_enemy
                    enemy_size = 100 if enemy_image == img_enemy2 else 80
                    enemy_health = 2 if enemy_image == img_enemy2 else 1

                    new_enemy = Enemy(enemy_image, randint(80, win_width - 80), -40, enemy_size, 60, randint(2, 4), enemy_health)
                    monsters.add(new_enemy)

            bonus_hits = sprite.groupcollide(bonus_enemies, bullets, True, True)
            if bonus_hits:
                ship.boost_speed(10000)
                boost_sound.play()

            if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
                finish = True
                bonus_fly_sound.stop()
                game_over_screen(lose)

            if score >= goal:
                finish = True
                bonus_fly_sound.stop()
                game_over_screen(win)
        else:
            draw_text(window, "PAUSED", font1, (255, 255, 0), win_width // 2, win_height // 2)

        display.update()
    time.delay(50)
