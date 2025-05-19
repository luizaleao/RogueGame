import pgzrun
from pgzero.actor import Actor
from pgzero.builtins import sounds, music
from pygame import Rect
from pgzero.clock import schedule

import random
import math

WIDTH = 800
HEIGHT = 480

# variaveis
game_state = "menu"
sound_on = True
game_over = False
game_won = False
delay_reset_scheduled = False

# Música
music.set_volume(0.5)
music.play('background_music')

# Botões do menu
menu_buttons = [
    {"text": "Start Game", "rect": Rect(300, 190, 200, 60), "action": "start"},
    {"text": "Exit", "rect": Rect(300, 300, 200, 60), "action": "exit"},
]

# Plataforma
platforms = [
    Rect(100, 400, 200, 20),
    Rect(320, 350, 200, 20),
    Rect(480, 300, 200, 20),
    Rect(200, 250, 150, 20),
    Rect(150, 150, 150, 20),
    Rect(360, 100, 150, 20),
    Rect(500, 50, 150, 20)
]

# Animação
def animate_sprite(images, index):
    return images[(index // 10) % len(images)]

# Classes
class Player:
    def __init__(self):
        self.actor = Actor("player_idle1")
        self.actor.pos = (120, 360)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.idle_images = ["player_idle1", "player_idle2"]
        self.run_images = ["player_run1", "player_run2"]
        self.anim_index = 0

    def update(self):
        self.vy += 0.5  # gravidade
        self.actor.x += self.vx
        self.actor.y += self.vy
        self.on_ground = False

        for plat in platforms:
            if self.actor.colliderect(plat) and self.vy >= 0:
                if self.actor.bottom <= plat.top + 10:
                    self.actor.bottom = plat.top
                    self.vy = 0
                    self.on_ground = True
                    break

        self.anim_index += 1

    def draw(self):
        images = self.run_images if abs(self.vx) > 0.5 else self.idle_images
        self.actor.image = animate_sprite(images, self.anim_index)
        self.actor.draw()

    def jump(self):
        if self.on_ground:
            self.vy = -10
            if sound_on:
                sounds.jump.play()

    @property
    def rect(self):
        return Rect(
            self.actor.left,
            self.actor.top,
            self.actor.width,
            self.actor.height
        )

    @property
    def x(self):
        return self.actor.x

    @property
    def y(self):
        return self.actor.y

class Enemy:
    def __init__(self, x, y, area_left, area_right):
        self.x = x
        self.y = y
        self.vx = 1.5
        self.area_left = area_left
        self.area_right = area_right
        self.images = [Actor("enemy1"), Actor("enemy2"), Actor("enemy3") , Actor("enemy4")]
        self.anim_index = 0
        self.rect = Rect(self.x, self.y, 32, 48)

    def update(self):
        self.x += self.vx
        if self.x < self.area_left or self.x > self.area_right:
            self.vx *= -1
        self.rect.topleft = (self.x, self.y)
        self.anim_index += 1

    def draw(self):
        sprite = animate_sprite(self.images, self.anim_index)
        sprite.topleft = (self.x, self.y)
        sprite.draw()

# Instâncias
player = Player()
enemies = [
    Enemy(100, 352, 100, 280),
    Enemy(400, 252, 400, 580),
    Enemy(150, 102, 150, 300),
    Enemy(435, 52, 360, 510),
    # Novo inimigo na plataforma intermediária
]

# ===== DRAW =====
def draw():
    global game_state
    screen.clear()
    if game_state == "menu":
        draw_menu()
    elif game_state == "running":
        draw_game()
    elif game_state == "exit":
        exit()

def draw_menu():
    screen.fill((30, 30, 50))
    screen.draw.text("Sky Jumper", center=(WIDTH // 2, 80), fontsize=60, color="white")
    for button in menu_buttons:
        screen.draw.filled_rect(button["rect"], (100, 100, 200))
        screen.draw.text(button["text"], center=button["rect"].center, fontsize=30, color="white")

def draw_game():
    screen.fill((50, 160, 255))
    for plat in platforms:
        screen.draw.filled_rect(plat, (120, 80, 40))
    player.draw()
    screen.draw.rect(player.rect, (255, 0, 0))
    for enemy in enemies:
        enemy.draw()
    if game_over:
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=80, color="red")
    elif game_won:
        screen.draw.text("YOU WIN!", center=(WIDTH // 2, HEIGHT // 2), fontsize=80, color="green")


# ===== UPDATE =====
def update():
    global game_state , game_over , game_won , delay_reset_scheduled
    if game_state == "running":
        if game_over or game_won:
            return
        player.update()
        if player.y > HEIGHT:
            reset_game()
        for enemy in enemies:
            enemy.update()
            if player.actor.colliderect(enemy.rect):
                if sound_on:
                    sounds.hit.play()
                game_over = True
                if not delay_reset_scheduled:
                    delay_reset_scheduled = True
                    schedule(reset_game, 2.0)
        highest_platform = platforms[-1]
        plat_top = highest_platform.top
        plat_left = highest_platform.left
        plat_right = highest_platform.right

        # Verifica se player está em cima da plataforma (acima dela e dentro dos limites horizontais)
        if (player.actor.bottom <= plat_top + 5 and
                plat_left <= player.actor.centerx <= plat_right):
            game_won = True
            if not delay_reset_scheduled:
                delay_reset_scheduled = True
                schedule(reset_game, 2.0)


def on_mouse_down(pos):
    global game_state, sound_on, player
    if game_state == "menu":
        for button in menu_buttons:
            if button["rect"].collidepoint(pos):
                if button["action"] == "start":
                    start_game()
                elif button["action"] == "sound":
                    sound_on = not sound_on
                    if not sound_on:
                        music.pause()
                    else:
                        music.unpause()
                elif button["action"] == "exit":
                    game_state = "exit"

def on_key_down(key):
    if game_state != "running" or game_over:
        return
    if key == keys.LEFT:
        player.vx = -3
    elif key == keys.RIGHT:
        player.vx = 3
    elif key == keys.SPACE:
        player.jump()

def on_key_up(key):
    if game_state != "running" or game_over:
        return
    if key in [keys.LEFT, keys.RIGHT]:
        player.vx = 0

# ===== GAME CONTROL =====
def start_game():
    global game_state, player , game_over , game_won
    game_over = False
    game_won = False
    game_state = "running"
    player = Player()
    player.actor.pos = (300, 360)

def reset_game():
    global game_state, game_over , game_won , delay_reset_scheduled
    game_state = "menu"
    game_over = False
    game_won = False
    delay_reset_scheduled = False


pgzrun.go()
