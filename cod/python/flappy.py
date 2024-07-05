
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
#iniciliza el contadpor
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

    def __init__(self,  x_pos, y_pos, images):
        #esta parte permite que use todas las funciones de pygame
        pygame.sprite.Sprite.__init__(self)
        #imagenes del pajaro (alas)
        self.imagenes =  images

        self.velocidad = velocidad_salto
        
        #se busca cual de las tres imagenes del pajaro se deben de usar
        self.current_image = 0
        self.image = images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        

        #posicion y tamano del pajaro 
        self.rect = self.image.get_rect()
        self.rect[0] = x_pos
        self.rect[1] = y_pos
        
    def update(self):
        #se crea una animacion de aleteo
        self.current_image = (self.current_image + 1) % 3
        self.image = self.imagenes[self.current_image]
        #simula el efecto de caer, aumenta la velocidad del pajaro
        self.velocidad += gravedad
        self.rect[1] += self.velocidad

    def bump(self):
        #se mueve hacia arriba
        self.velocidad = -velocidad_salto

    def begin(self):
        #Se cambia las imagenes en la pantalla de inicio, para que se vea un aleteo
        self.current_image = (self.current_image + 1) % 3
        self.image = self.imagenes[self.current_image]




class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)

        #carga las imagenes de los tubos con las dimensiones ya especificadas
        self. image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ancho_tuberia, altura_tuberia))


        self.rect = self.image.get_rect()
        self.rect[0] = x_pos

        #Si inverted es true se coloca el tubo arriba y si no abajo
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - y_pos)
        else:
            self.rect[1] = altura_pantalla - y_pos

        #Se crea una mascara de colision (entender bien como funciona)
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        #mueve el tubo hacia la izquierda, simulando que el pajaro avance
        #Cambio: velocidad_actual en vez de velocidad_juego
        self.rect[0] -= velocidad_actual

        

class Ground(pygame.sprite.Sprite):
    
    def __init__(self, x_pos):
    
        pygame.sprite.Sprite.__init__(self)
        
        #se acomoda la imagen del suelo para que tenga las dimensiones necesarias
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ancho_suelo, altura_suelo))

        # se crea una mascara, asi si pega con el suelo el juego se detiene
        self.mask = pygame.mask.from_surface(self.image)

        # se colocan las imagenes y dimensiones
        self.rect = self.image.get_rect()
        self.rect[0] = x_pos
        self.rect[1] = altura_pantalla - altura_suelo
        
        
    def update(self):
        #mueve el suelo hacia la izquierda
        #Cambio: velocidad_actual en vez de velocidad_juego
        self.rect[0] -= velocidad_actual

def is_off_screen(sprite):
    #verifica si el sprite(en este casos las tuerias) se salio por completo de la pantalla, es decir si la coordenada
    #X es menor que el negatico del ancho, asi se puede eliminar o reciclar
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(x_pos):
    #xpos es donde se colocan las tuberias(posible cambio)
    #genera un numero entre 100 y 300 donde se va a generar la tuberia
    tamano = random.randint(100, 300)
    #False indic a que la tuberia no esta invertida, xpos donde se va a colocar y size la altura
    pipe = Pipe(False, x_pos, tamano)
    #lo mismo que la anterior pero invertida y considerando un espacio
    pipe_inverted = Pipe(True, x_pos, altura_pantalla - tamano - distancia_tuberias)
    return pipe, pipe_inverted

#inicializa todos los modulos pygame
pygame.init()
#crea la consola
screen = pygame.display.set_mode((ancho_pantalla, altura_pantalla))
#Titulo del juego
pygame.display.set_caption('Flappy Bird')

#assets/sprites/background-day.png




#carga la imagen de fondo y la ajusta a las dimensiones
BACKGROUND = pygame.image.load('assets/sprites/imagen-fondo.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (ancho_pantalla, altura_pantalla))
#carga la imagen de inicio
BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha()


bird1_images = [
    pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
    pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
    pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()
]

# Se cargan imagenes para un segundo pajaro
bird2_images = [
    pygame.image.load('assets/sprites/redbird-upflap.png').convert_alpha(),
    pygame.image.load('assets/sprites/redbird-midflap.png').convert_alpha(),
    pygame.image.load('assets/sprites/redbird-downflap.png').convert_alpha()
]


#crea un grupo para manejar distintos sprites que se van a utilizar para el pajaro
bird_group = pygame.sprite.Group()
#se crea una instancia de la clase Bird y se annade el pajaro
bird1 = Bird(ancho_pantalla / 6, altura_pantalla / 2, bird1_images)
bird2 = Bird(ancho_pantalla / 6, altura_pantalla / 3, bird2_images)
bird_group.add(bird1)
bird_group.add(bird2)

#crea un grupo para manejar distintos sprites para el suelo
ground_group = pygame.sprite.Group()

#se itera dos veces para colocar el suelo
for i in range (2):
    ground = Ground(ancho_suelo * i)
    #se guarda y se coloca le suelo
    ground_group.add(ground)

#crea un grupo para manejar distintos sprites para las tuberias
pipe_group = pygame.sprite.Group()
#se crean dos tubos el de arriba y el de abajo
for i in range (2):
    pipes = get_random_pipes(ancho_pantalla * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])


#permite controlar la velocidad de actalizacion del juego
clock = pygame.time.Clock()

begin = True

#CAMBIOS
# Variables para controlar la velocidad del juego
velocidad_actual = velocidad_juego
next_threshold = puntaje_acutual
#FIN DE CAMBIOS

# Carga la fuente para mostrar el puntaje
pygame.font.init()
score_font = pygame.font.Font('freesansbold.ttf', 32)


#s eva a ejecutar siempre que begin siga siendo TRUE
while begin:

    clock.tick(15)
    # va a ietrar sobre todos los eventos que se definiendo en pygame
    for event in pygame.event.get():
        #si se pide cerrar la ventana se quita
        if event.type == QUIT:
            pygame.quit()
        #se revisa si se presiona alguna tecla
        if event.type == KEYDOWN:
            #se revisa si se presiona la flecha de arriba o el espaciado
            if event.key == K_SPACE or event.key == K_UP:
                bird1.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()
                #el juego comienza
                begin = False
                #se revisa si se presiona W
            if event.key == K_w:
                bird2.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()
                begin = False
  
                
                
                
    #dibuja los fondos
    screen.blit(BACKGROUND, (0, 0))
    screen.blit(BEGIN_IMAGE, (120, 150))

    #se va actualizando el suelo
    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(ancho_suelo - 20)
        ground_group.add(new_ground)

#se inicia el primer y segundo pajaro
    bird1.begin()
    bird2.begin()
    ground_group.update()

    bird_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()
    


# Variable para rastrear cuándo se incrementa el puntaje
passed_pipe = False

while True:

    clock.tick(15)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            #controla el primer pajaro
            if event.key == K_SPACE or event.key == K_UP:
                bird1.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()
                #controla el segundo pajaro
            if event.key == K_w:
                bird2.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()


    screen.blit(BACKGROUND, (0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(ancho_suelo - 20)
        ground_group.add(new_ground)

    #si los primero tubos ya salieron de oantalla se eliminan y se annaden nuevso
    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])
        
        #se annaden nuevos tubos a la derecha
        pipes = get_random_pipes(ancho_pantalla * 2)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
        
        passed_pipe = False

    #CAMBIOS
    # Verifica si el pájaro pasó las tuberías
    for pipe in pipe_group:
        if bird1.rect.left > pipe.rect.right and not passed_pipe:
            puntaje += 1
            passed_pipe = True
        if bird2.rect.left > pipe.rect.right and not passed_pipe:
            puntaje += 1
            passed_pipe = True
            
        # Verifica si el puntaje ha alcanzado el umbral para aumentar la velocidad
        if puntaje >= next_threshold:
            velocidad_actual += incremento_velocidad
            next_threshold += puntaje_acutual
    #FIN DE CAMBIOS
            
    #se catualizan los grupps
    bird_group.update()
    ground_group.update()
    pipe_group.update()

    #se dibuja
    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)
    
    #Acomoda el puntaje en la pantalla
    score_surface = score_font.render(f'{puntaje}', True, (255, 215, 0))
    score_rect = score_surface.get_rect(center=(ancho_pantalla / 2, 50))  # Centra el puntaje
    screen.blit(score_surface, score_rect)

    #se actualiza la pantalla
    pygame.display.update()

    #se verifica si el pajaro pego con el suelo o tuberias
    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        pygame.mixer.music.load(hit)
        pygame.mixer.music.play()
        time.sleep(1)
     
    #CAMBIOS
     # Mostrar el puntaje final
        final_score_surface = score_font.render(f'Puntaje final: {puntaje}', True, (255, 215, 0))
        screen.blit(final_score_surface, (ancho_pantalla // 2 - final_score_surface.get_width() // 2, altura_pantalla // 2))
        pygame.display.update()
        time.sleep(3)
    #FIN DE CAMBIOS
    
        break
pygame.quit()