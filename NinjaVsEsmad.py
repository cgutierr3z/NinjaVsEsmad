#Carlos Gutierrez
#Computacion Grafica
#Ingenieria de Sistemas y Computacion
#2do Semestre de 2015

import sys
import pygame
import random
from pygame.locals import *
from math import *

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

# Initialize the game engine
pygame.init()

SCREEN_WIDHT	= 800
SCREEN_HEIGHT 	= 600

SCREEN_SIZE = [SCREEN_WIDHT,SCREEN_HEIGHT]
screen =  pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("NinjaVsEsmad")
clock = pygame.time.Clock()

class Jugador( pygame.sprite.Sprite ):

	vel_x = 0
	vel_y = 0

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		ancho = 40
		alto = 60

		self.image = pygame.Surface([ancho,alto])
		self.image.fill(RED)

		self.rect = self.image.get_rect()


	def update(self):
		self.calc_grav()

		#mov izq der
		self.rect.x += self.vel_x

		#revisar colision
		bloque_col_list = pygame.sprite.spritecollide(self, self.nivel.plataforma_lista, False)

		for bloque in bloque_col_list:
				if self.vel_x > 0:
					self.rect.right = bloque.rect.left
				elif self.vel_x < 0:
					self.rect.left = bloque.rect.right



		#mover arriba y abajo

		self.rect.y += self.vel_y

		#se revisa el choque
		bloque_col_list = pygame.sprite.spritecollide(self,self.nivel.plataforma_lista,False)

		for bloque in bloque_col_list:
				if self.vel_y > 0:
					self.rect.bottom = bloque.rect.top
				elif self.vel_y < 0:
					self.rect.top = bloque.rect.bottom

				self.vel_y = 0


	def calc_grav(self):
		if self.vel_y == 0:
			self.vel_y = 1
		else:
			self.vel_y += 0.35

		#esta en el suelo
		if self.rect.y >= (SCREEN_HEIGHT - 70) - self.rect.height and self.vel_y >= 0:
			self.vel_y = 0
			self.rect.y = (SCREEN_HEIGHT - 70) - self.rect.height

	def salto(self):
		self.rect.y += 2
		plataforma_col_lista = pygame.sprite.spritecollide(self, self.nivel.plataforma_lista, False)
		self.rect.y -= 2

		#si se puede salta

		if len(plataforma_col_lista) > 0 or self.rect.bottom >= (SCREEN_HEIGHT - 70):
			self.vel_y = -9
			#self.vel_x = 6

	def ir_izq(self):
		self.vel_x = -3

	def ir_der(self):
		self.vel_x = 3

	def no_mover(self):
		self.vel_x = 0

class Plataforma(pygame.sprite.Sprite):
	def __init__ (self, ancho, alto):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface([ancho,alto])
		self.image.fill(GREEN)

		self.rect = self.image.get_rect()

class Nivel(object):
	#lista sprite todos los niveles

	plataforma_lista = None
	enemigos_lista = None

	fondo = None
	mov_fondo = 0
    #limite = -1000

	def __init__(self,jugador):
		self.plataforma_lista = pygame.sprite.Group()
		self.enemigos_lista = pygame.sprite.Group()
		self.jugador = jugador

	def update(self):
		self.plataforma_lista.update()
		self.enemigos_lista.update()

	def draw(self, pantalla):
		pantalla.fill(BLUE)
		pantalla.blit(self.fondo,(self.mov_fondo // 2,0))

		self.plataforma_lista.draw(pantalla)
		self.enemigos_lista.draw(pantalla)

	def Mover_fondo(self, mov_x):
		self.mov_fondo += mov_x

		for platforma in self.plataforma_lista:
			platforma.rect.x += mov_x

		for enemigos in self.enemigos_lista:
			enemigos.rect.x += mov_x

class Nivel_01(Nivel):
	def __init__(self, jugador):
		Nivel.__init__(self, jugador)

		self.fondo = pygame.image.load("img/NinjaVsEsmad_back01.png").convert()
		self.limite = -4000

		nivel = [ 	[50,100,100,500],[50,10,300,500],[50,100,500,500],[50,10,700,500],[50,200,850,350],[50,10,1000,500],

		[50,100,200,400],[50,100,600,400],

		[50,10,300,300],[50,100,500,300],[50,10,700,300],
		]

		for plataforma in nivel:
			bloque = Plataforma(plataforma[0], plataforma[1])
			bloque.rect.x = plataforma[2]
			bloque.rect.y = plataforma[3]
			bloque.jugador = self.jugador
			self.plataforma_lista.add(bloque)


class Nivel_02(Nivel):
	def __init__(self,jugador):
		Nivel.__init__(self,jugador)

		self.fondo = pygame.image.load("img/NinjaVsEsmad_back01.png").convert()
		self.limite = -6000

		nivel = [ 	[50,10,100,300],[50,10,300,300],[50,10,500,300],[50,10,700,300],[50,10,900,300],[50,10,1100,300],

					[50,10,200,400],[50,10,600,400],

					[50,10,300,500],[50,10,500,500],[50,10,700,500],
				]

		for plataforma in nivel:
			bloque = Plataforma(plataforma[0], plataforma[1])
			bloque.rect.x = plataforma[2]
			bloque.rect.y = plataforma[3]
			bloque.jugador = self.jugador
			self.plataforma_lista.add(bloque)


def text_objects(text, font, color = BLACK):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def boton(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(WHITE)

        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("A bit Racey", largeText)
        TextRect.center = ((SCREEN_WIDHT/2),(SCREEN_HEIGHT/2))
        screen.blit(TextSurf, TextRect)

        boton("GO!",150,450,100,50,GREEN,RED,intro)
        boton("Quit",550,450,100,50,RED,GREEN,main)

        pygame.display.update()
        clock.tick(15)

def intro():
    font = pygame.font.Font(None, 36)
    listo = False
    ver_inst = True
    pag = 1
    while listo == False and ver_inst:
    	for event in pygame.event.get():
    		if event.type == pygame.QUIT:
    			listo = True
    		if event.type == pygame.MOUSEBUTTONDOWN:
    			pag += 1
    			if pag == 3:
    				ver_inst = False

    	screen.fill(BLACK)

    	if pag == 1:
    		image = pygame.image.load("img/intro.png")
    		screen.blit(image,(0,0))

    	if pag == 2:
    		texto = font.render("Pagina 2", True, WHITE)
    		screen.blit(texto, (10,100))

    	pygame.display.update()
        clock.tick(20)

def main():
	jugador = Jugador()

	nivel_lista = []
	nivel_lista.append( Nivel_01(jugador) )
	nivel_lista.append( Nivel_02(jugador) )
	nivel_lista.append( Nivel_01(jugador) )


	nivel_actual_no = 0
	nivel_actual = nivel_lista[nivel_actual_no]

	activos_sp_lista = pygame.sprite.Group()
	jugador.nivel = nivel_actual

	jugador.rect.x = 340
	jugador.rect.y = (SCREEN_HEIGHT - 70) - jugador.rect.height
	activos_sp_lista.add(jugador)

	fin = False
	reloj = pygame.time.Clock()

	while not fin:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				fin = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					jugador.ir_izq()
				if event.key == pygame.K_RIGHT:
					jugador.ir_der()
				if event.key == pygame.K_UP:
					jugador.salto()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT and jugador.vel_x < 0:
					jugador.no_mover()
				if event.key == pygame.K_RIGHT and jugador.vel_x > 0:
					jugador.no_mover()

		activos_sp_lista.update()
		nivel_actual.update()

		#avanza a la derecha
		if jugador.rect.right >= 400:
			dif = jugador.rect.x - 400
			jugador.rect.x = 400
			nivel_actual.Mover_fondo(-dif)

		#avanza a la izquierda
		if jugador.rect.right <= 120:
			dif = 120 - jugador.rect.x
			jugador.rect.x = 120
			nivel_actual.Mover_fondo(dif)

		#final del nivel
		pos_actual = jugador.rect.x + nivel_actual.mov_fondo
		print pos_actual
		if (pos_actual < nivel_actual.limite):
			jugador.rect.x = 120
			if (nivel_actual_no < len(nivel_lista)-1):
				nivel_actual_no += 1
				nivel_actual = nivel_lista[nivel_actual_no]
				jugador.nivel = nivel_actual

		if jugador.rect.left < 0:
			jugador.rect.left = 0

		nivel_actual.draw(screen)
		activos_sp_lista.draw(screen)
		reloj.tick(60)
		pygame.display.flip()

if __name__ == "__main__":
        #menu()
        intro()
    	main()
