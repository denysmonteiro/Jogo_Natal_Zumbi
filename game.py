import pgzrun
import math
import random
from pygame import Rect

WIDTH = 800
HEIGHT = 600
TITLE = "Minha Aventura de Natal"

modo_jogo = "menu"
som_ligado = True

class Button:
    def __init__(self, x, y, texto, tipo="normal"):
        self.rect = Rect(0, 0, 220, 50)
        self.rect.center = (x, y)
        self.text = texto
        self.tipo = tipo 

    def draw(self):
        cor_fundo = (50, 50, 150)
        if self.tipo == "toggle" and not som_ligado:
            cor_fundo = (150, 50, 50)
            texto_botao = "SOM: OFF"
        elif self.tipo == "toggle" and som_ligado:
            cor_fundo = (50, 150, 50)
            texto_botao = "SOM: ON"
        else:
            texto_botao = self.text

        screen.draw.filled_rect(self.rect, cor_fundo)
        screen.draw.rect(self.rect, (255, 255, 255))
        screen.draw.text(texto_botao, center=self.rect.center, fontsize=30, color="white")

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Hero:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.sprites_andar = ['hero1', 'hero2'] 
        self.frame_atual = 0
        self.tempo_animacao = 0
        
        try:
            self.actor = Actor(self.sprites_andar[0], center=(self.x, self.y))
            self.usar_sprite = True
        except:
            self.usar_sprite = False
        
        self.target_x = self.x
        self.target_y = self.y
        self.speed = 3
        self.moving = False

    def update(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distancia = math.sqrt(dx**2 + dy**2)

        if distancia > 5:
            self.moving = True
            self.x += (dx / distancia) * self.speed
            self.y += (dy / distancia) * self.speed
            self.animar()
        else:
            self.moving = False
            self.x = self.target_x
            self.y = self.target_y
            if self.usar_sprite:
                self.actor.image = self.sprites_andar[0]

        if self.usar_sprite:
            self.actor.pos = (self.x, self.y)

    def animar(self):
        if not self.usar_sprite: return
        self.tempo_animacao += 1
        if self.tempo_animacao > 10:
            self.tempo_animacao = 0
            self.frame_atual += 1
            if self.frame_atual >= len(self.sprites_andar):
                self.frame_atual = 0
            self.actor.image = self.sprites_andar[self.frame_atual]

    def draw(self):
        if self.usar_sprite:
            self.actor.draw()
        else:
            screen.draw.filled_rect(Rect(self.x-20, self.y-40, 40, 80), (255, 0, 0))

    def set_target(self, pos):
        self.target_x = pos[0]
        self.target_y = pos[1]

class Enemy:
    def __init__(self):
        self.spawn_longe()
        
        self.sprites = ['enemy1', 'enemy2']
        self.frame_atual = 0
        self.tempo_animacao = 0
        try:
            self.actor = Actor(self.sprites[0], center=(self.x, self.y))
            self.usar_sprite = True
        except:
            self.usar_sprite = False
        self.speed = 1.2

    def spawn_longe(self):
        while True:
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(0, HEIGHT)
            dist_centro = math.sqrt((self.x - 400)**2 + (self.y - 300)**2)
            if dist_centro > 200: 
                break

    def update(self, player_x, player_y):
        if self.x < player_x: self.x += self.speed
        if self.x > player_x: self.x -= self.speed
        if self.y < player_y: self.y += self.speed
        if self.y > player_y: self.y -= self.speed
        
        self.animar()
        if self.usar_sprite:
            self.actor.pos = (self.x, self.y)

    def animar(self):
        if not self.usar_sprite: return
        self.tempo_animacao += 1
        if self.tempo_animacao > 15:
            self.tempo_animacao = 0
            self.frame_atual += 1
            if self.frame_atual >= len(self.sprites):
                self.frame_atual = 0
            self.actor.image = self.sprites[self.frame_atual]

    def draw(self):
        if self.usar_sprite:
            self.actor.draw()
        else:
            screen.draw.filled_rect(Rect(self.x-20, self.y-20, 40, 40), (100, 0, 100))

botao_start = Button(400, 250, "JOGAR")
botao_som = Button(400, 320, "SOM: ON", tipo="toggle")
botao_sair = Button(400, 390, "SAIR")

player = Hero()
inimigos = [] 

def iniciar_jogo():
    global modo_jogo
    modo_jogo = "jogo"
    
    player.x = 400
    player.y = 300
    player.target_x = 400
    player.target_y = 300
    
    inimigos.clear()
    for i in range(4):
        inimigos.append(Enemy())

    if som_ligado:
        try:
            music.play('musica_fundo')
            music.set_volume(0.3)
        except:
            print("Erro ao carregar musica")

def update():
    global modo_jogo
    
    if modo_jogo == "jogo":
        player.update()
        for inimigo in inimigos:
            inimigo.update(player.x, player.y)
            
            dist = math.sqrt((inimigo.x - player.x)**2 + (inimigo.y - player.y)**2)
            if dist < 30:
                print("GAME OVER")
                modo_jogo = "menu"
                music.stop() 

def draw():
    screen.clear()
    
    if modo_jogo == "menu":
        screen.fill((30, 30, 30))
        screen.draw.text("Zumbis no Natal", center=(400, 100), fontsize=60, color="yellow")
        botao_start.draw()
        botao_som.draw()
        botao_sair.draw()
        
    elif modo_jogo == "jogo":
        try:
            screen.blit("fundo_natal", (0, 0))
        except:
            screen.fill((50, 100, 50))
        
        player.draw()
        for inimigo in inimigos:
            inimigo.draw()
        
        if som_ligado:
            screen.draw.text("Som: ON", (10, 10), fontsize=20)
        else:
            screen.draw.text("Som: OFF", (10, 10), fontsize=20)

def on_mouse_down(pos):
    global modo_jogo, som_ligado
    
    if modo_jogo == "menu":
        if botao_start.is_clicked(pos):
            iniciar_jogo()
        elif botao_som.is_clicked(pos):
            som_ligado = not som_ligado
        elif botao_sair.is_clicked(pos):
            quit()
            
    elif modo_jogo == "jogo":
        player.set_target(pos)
        if som_ligado:
            try:
                sounds.click.play()
            except:
                pass

pgzrun.go()