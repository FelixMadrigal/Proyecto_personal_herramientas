# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 20:58:17 2024

@author: Félix Madrigal
"""
import pygame, random, time
from pygame.locals import *

#VARIABLES
ancho_pantalla = 800  #tamano de la consola
altura_pantalla = 600 #tamano de la consola
velocidad_salto = 20  #velocidad del salto
gravedad = 2.5 #gravedad del salto
velocidad_juego = 20 #velocidad del juego

#dimensiones del suelo
ancho_suelo = 2 * ancho_pantalla
altura_suelo= 100

#Dimensiones y separaciones de los tubos (posible cambio a generar mas tubos)
ancho_tuberia = 80
altura_tuberia = 500
distancia_tuberias = 150

#CAMBIOS
#inicializa el contador
puntaje = 0
#variables para aumentar la velocidad del juego segun cierta cantidad de puntos
incremento_velocidad = 5 
puntaje_acutual = 5  
#FIN DE CAMBIOS

#rutas del sonido
wing = 'assets/audio/wing.wav'
hit = 'assets/audio/hit.wav'

#inicializa el sonido
pygame.mixer.init()

class Bird(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos, images):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = images
        self.velocidad = velocidad_salto
        self.current_image = 0
        self.image = images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = x_pos
        self.rect[1] = y_pos

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.imagenes[self.current_image]
        self.velocidad += gravedad
        self.rect[1] += self.velocidad

    def bump(self):
        self.velocidad = -velocidad_salto

    def begin(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.imagenes[self.current_image]

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ancho_tuberia, altura_tuberia))
        self.rect = self.image.get_rect()
        self.rect[0] = x_pos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - y_pos)
        else:
            self.rect[1] = altura_pantalla - y_pos

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= velocidad_actual

class Ground(pygame.sprite.Sprite):
    
    def __init__(self, x_pos):
    
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ancho_suelo, altura_suelo))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = x_pos
        self.rect[1] = altura_pantalla - altura_suelo
        
    def update(self):
        self.rect[0] -= velocidad_actual

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(x_pos):
    tamano = random.randint(100, 300)
    pipe = Pipe(False, x_pos, tamano)
    pipe_inverted = Pipe(True, x_pos, altura_pantalla - tamano - distancia_tuberias)
    return pipe, pipe_inverted

pygame.init()
screen = pygame.display.set_mode((ancho_pantalla, altura_pantalla))
pygame.display.set_caption('Flappy Bird')

BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (ancho_pantalla, altura_pantalla))
BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha()

bird1_images = [
    pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
    pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
    pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()
]

# Load different images for the second bird (e.g., red bird)
bird2_images = [
    pygame.image.load('assets/sprites/redbird-upflap.png').convert_alpha(),
    pygame.image.load('assets/sprites/redbird-midflap.png').convert_alpha(),
    pygame.image.load('assets/sprites/redbird-downflap.png').convert_alpha()
]

bird_group = pygame.sprite.Group()
bird1 = Bird(ancho_pantalla / 6, altura_pantalla / 2, bird1_images)
bird2 = Bird(ancho_pantalla / 6, altura_pantalla / 3, bird2_images)
bird_group.add(bird1)
bird_group.add(bird2)

ground_group = pygame.sprite.Group()
for i in range (2):
    ground = Ground(ancho_suelo * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range (2):
    pipes = get_random_pipes(ancho_pantalla * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()
begin = True

velocidad_actual = velocidad_juego
next_threshold = puntaje_acutual

pygame.font.init()
score_font = pygame.font.Font('freesansbold.ttf', 32)

while begin:
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird1.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()
                begin = False
            if event.key == K_w:
                bird2.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()
                begin = False

    screen.blit(BACKGROUND, (0, 0))
    screen.blit(BEGIN_IMAGE, (120, 150))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(ancho_suelo - 20)
        ground_group.add(new_ground)

    bird1.begin()
    bird2.begin()
    ground_group.update()

    bird_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()

passed_pipe = False

while True:
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird1.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()
            if event.key == K_w:
                bird2.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()

    screen.blit(BACKGROUND, (0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(ancho_suelo - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])
        pipes = get_random_pipes(ancho_pantalla * 2)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
        passed_pipe = False

    for pipe in pipe_group:
        if bird1.rect.left > pipe.rect.right and not passed_pipe:
            puntaje += 1
            passed_pipe = True
        if bird2.rect.left > pipe.rect.right and not passed_pipe:
            puntaje += 1
            passed_pipe = True
            
        if puntaje >= next_threshold:
            velocidad_actual += incremento_velocidad
            next_threshold += puntaje_acutual

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    score_surface = score_font.render(f'Score: {puntaje}', True, (255, 215, 0))
    score_rect = score_surface.get_rect(center=(ancho_pantalla / 2, 50))
    screen.blit(score_surface, score_rect)

    pygame.display.update()

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        pygame.mixer.music.load(hit)
        pygame.mixer.music.play()
        time.sleep(1)
        
        final_score_surface = score_font.render(f'Final Score: {puntaje}', True, (255, 215, 0))
        screen.blit(final_score_surface, (ancho_pantalla // 2 - final_score_surface.get_width() // 2, altura_pantalla // 2))
        pygame.display.update()
        time.sleep(3)
        break

pygame.quit()

