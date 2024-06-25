# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 20:58:17 2024

@author: Félix Madrigal
"""
import pygame
import random
import time
from pygame.locals import *

class Config:
    ANCHO_PANTALLA = 800
    ALTURA_PANTALLA = 600
    VELOCIDAD_SALTO = 20
    GRAVEDAD = 2.5
    VELOCIDAD_JUEGO = 20

    ANCHO_SUELO = 2 * ANCHO_PANTALLA
    ALTURA_SUELO = 100

    ANCHO_TUBERIA = 80
    ALTURA_TUBERIA = 500
    DISTANCIA_TUBERIAS = 150

    INCREMENTO_VELOCIDAD = 5 
    PUNTAJE_ACTUAL = 5  

    WING_SOUND = 'assets/audio/wing.wav'
    HIT_SOUND = 'assets/audio/hit.wav'

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
                         pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
                         pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()]
        self.velocidad = Config.VELOCIDAD_SALTO
        self.current_image = 0
        self.image = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = Config.ANCHO_PANTALLA / 6
        self.rect[1] = Config.ALTURA_PANTALLA / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.imagenes[self.current_image]
        self.velocidad += Config.GRAVEDAD
        self.rect[1] += self.velocidad

    def bump(self):
        self.velocidad = -Config.VELOCIDAD_SALTO

    def begin(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.imagenes[self.current_image]

class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (Config.ANCHO_TUBERIA, Config.ALTURA_TUBERIA))
        self.rect = self.image.get_rect()
        self.rect[0] = x_pos
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = -(self.rect[3] - y_pos)
        else:
            self.rect[1] = Config.ALTURA_PANTALLA - y_pos
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= velocidad_actual

class Ground(pygame.sprite.Sprite):
    def __init__(self, x_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (Config.ANCHO_SUELO, Config.ALTURA_SUELO))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = x_pos
        self.rect[1] = Config.ALTURA_PANTALLA - Config.ALTURA_SUELO

    def update(self):
        self.rect[0] -= velocidad_actual

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(x_pos):
    tamano = random.randint(100, 300)
    pipe = Pipe(False, x_pos, tamano)
    pipe_inverted = Pipe(True, x_pos, Config.ALTURA_PANTALLA - tamano - Config.DISTANCIA_TUBERIAS)
    return pipe, pipe_inverted

class FlappyBirdGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.ANCHO_PANTALLA, Config.ALTURA_PANTALLA))
        pygame.display.set_caption('Flappy Bird')
        self.background = pygame.image.load('assets/sprites/background-day.png')
        self.background = pygame.transform.scale(self.background, (Config.ANCHO_PANTALLA, Config.ALTURA_PANTALLA))
        self.begin_image = pygame.image.load('assets/sprites/message.png').convert_alpha()
        self.bird_group = pygame.sprite.Group()
        self.bird = Bird()
        self.bird_group.add(self.bird)
        self.ground_group = pygame.sprite.Group()
        for i in range(2):
            ground = Ground(Config.ANCHO_SUELO * i)
            self.ground_group.add(ground)
        self.pipe_group = pygame.sprite.Group()
        for i in range(2):
            pipes = get_random_pipes(Config.ANCHO_PANTALLA * i + 800)
            self.pipe_group.add(pipes[0])
            self.pipe_group.add(pipes[1])
        self.clock = pygame.time.Clock()
        self.begin = True
        self.velocidad_actual = Config.VELOCIDAD_JUEGO
        self.next_threshold = Config.PUNTAJE_ACTUAL
        pygame.font.init()
        self.score_font = pygame.font.Font('freesansbold.ttf', 32)
        self.passed_pipe = False
        self.puntaje = 0

    def run(self):
        while self.begin:
            self.clock.tick(15)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE or event.key == K_UP:
                        self.bird.bump()
                        pygame.mixer.music.load(Config.WING_SOUND)
                        pygame.mixer.music.play()
                        self.begin = False
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.begin_image, (120, 150))
            if is_off_screen(self.ground_group.sprites()[0]):
                self.ground_group.remove(self.ground_group.sprites()[0])
                new_ground = Ground(Config.ANCHO_SUELO - 20)
                self.ground_group.add(new_ground)
            self.bird.begin()
            self.ground_group.update()
            self.bird_group.draw(self.screen)
            self.ground_group.draw(self.screen)
            pygame.display.update()

        while True:
            self.clock.tick(15)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE or event.key == K_UP:
                        self.bird.bump()
                        pygame.mixer.music.load(Config.WING_SOUND)
                        pygame.mixer.music.play()
            self.screen.blit(self.background, (0, 0))
            if is_off_screen(self.ground_group.sprites()[0]):
                self.ground_group.remove(self.ground_group.sprites()[0])
                new_ground = Ground(Config.ANCHO_SUELO - 20)
                self.ground_group.add(new_ground)
            if is_off_screen(self.pipe_group.sprites()[0]):
                self.pipe_group.remove(self.pipe_group.sprites()[0])
                self.pipe_group.remove(self.pipe_group.sprites()[0])
                pipes = get_random_pipes(Config.ANCHO_PANTALLA * 2)
                self.pipe_group.add(pipes[0])
                self.pipe_group.add(pipes[1])
                self.passed_pipe = False
            for pipe in self.pipe_group:
                if self.bird.rect.left > pipe.rect.right and not self.passed_pipe:
                    self.puntaje += 1
                    self.passed_pipe = True
                if self.puntaje >= self.next_threshold:
                    self.velocidad_actual += Config.INCREMENTO_VELOCIDAD
                    self.next_threshold += Config.PUNTAJE_ACTUAL
            self.bird_group.update()
            self.ground_group.update()
            self.pipe_group.update()
            self.bird_group.draw(self.screen)
            self.pipe_group.draw(self.screen)
            self.ground_group.draw(self.screen)
            score_surface = self.score_font.render(f'{self.puntaje}', True, (255, 215, 0))
            score_rect = score_surface.get_rect(center=(Config.ANCHO_PANTALLA / 2, 50))
            self.screen.blit(score_surface, score_rect)
            pygame.display.update()
            if (pygame.sprite.groupcollide(self.bird_group, self.ground_group, False, False, pygame.sprite.collide_mask) or
                pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False, pygame.sprite.collide_mask)):
                pygame.mixer.music.load(Config.HIT_SOUND)
                pygame.mixer.music.play()
                time.sleep(1)
                final_score_surface = self.score_font.render(f'Puntaje final: {self.puntaje}', True, (255, 215, 0))
                self.screen.blit(final_score_surface, (Config.ANCHO_PANTALLA // 2 - final_score_surface.get_width() // 2, Config.ALTURA_PANTALLA // 2))
                pygame.display.update()
                time.sleep(3)
                break
        pygame.quit()

if __name__ == "__main__":
    FlappyBirdGame().run()
