#######################################################################

# This file is part of NinjaVsEsmad.

# NinjaVsEsmad is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# NinjaVsEsmad is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with NinjaVsEsmad.  If not, see <http://www.gnu.org/licenses/>.

#######################################################################

import pygame
from pygame.locals import *

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


class SpriteSheet(object):
	sprite_sheet = None

	def __init__(self, file_name):
		self.sprite_sheet = pygame.image.load(file_name).convert()

	def get_image(self, x, y, width, height):
		image = pygame.Surface([width, height]).convert()
		image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
		image.set_colorkey(BLACK)

		return image

class Ninja( pygame.sprite.Sprite ):
	vel_x = 0
	vel_y = 0

	frames_der = []
	frames_izq = []

	direccion = "R"
	nivel = None

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		sprite_sheet = SpriteSheet("img/ninja.png")

		image = sprite_sheet.get_image(0, 0, 66, 90)
		self.frames_der.append(image)
		image = pygame.transform.flip(image, True, False)
		self.frames_izq.append(image)

		image = sprite_sheet.get_image(66, 0, 66, 90)
		self.frames_der.append(image)
		image = pygame.transform.flip(image, True, False)
		self.frames_izq.append(image)

		image = sprite_sheet.get_image(132, 0, 67, 90)
		self.frames_der.append(image)
		image = pygame.transform.flip(image, True, False)
		self.frames_izq.append(image)

		image = sprite_sheet.get_image(0, 93, 66, 90)
		self.frames_der.append(image)
		image = pygame.transform.flip(image, True, False)
		self.frames_izq.append(image)

		image = sprite_sheet.get_image(66, 93, 66, 90)
		self.frames_der.append(image)
		image = pygame.transform.flip(image, True, False)
		self.frames_izq.append(image)

		image = sprite_sheet.get_image(132, 93, 72, 90)
		self.frames_der.append(image)
		image = pygame.transform.flip(image, True, False)
		self.frames_izq.append(image)

		image = sprite_sheet.get_image(0, 186, 70, 90)
		self.frames_der.append(image)
		image = pygame.transform.flip(image, True, False)
		self.frames_izq.append(image)

		self.image = self.frames_der[0]

		self.rect = self.image.get_rect()

	def update(self):
		self.calc_grav()

		#mov izq der
		self.rect.x += self.vel_x
		pos_x = self.rect.x + self.nivel.mov_x
		if self.direccion == "R":
			frame = (pos_x // 15) % len(self.frames_der)
			self.image = self.frames_der[frame]
		else:
			frame = (pos_x // 15) % len(self.frames_izq)
			self.image = self.frames_izq[frame]

		#revisar colision
		bloque_col_list = pygame.sprite.spritecollide(self, self.nivel.plataforma_lista, False)

		for bloque in bloque_col_list:
				if self.vel_x > 0:
					self.rect.right = bloque.rect.left
				elif self.vel_x < 0:
					self.rect.left = bloque.rect.right

		#mov arriba y abajo
		self.rect.y += self.vel_y

		#revisar colision
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
		self.direccion = "L"

	def ir_der(self):
		self.vel_x = 3
		self.direccion = "R"

	def no_mover(self):
		self.vel_x = 0

#MAPEO DE LAS PLATAFORMAS
METAL_IZQ 	= (560, 70, 70, 40)
METAL_MED	= (490, 140, 70, 40)
METAL_DER	= (560, 140, 70, 70)

class Plataforma(pygame.sprite.Sprite):
	def __init__(self, sprite_data):
		pygame.sprite.Sprite.__init__(self)

		sprite_sheet = SpriteSheet("img/sheet.png")
		self.image = sprite_sheet.get_image(sprite_data[0],sprite_data[1],sprite_data[2],sprite_data[3])

		self.rect = self.image.get_rect()

class PlataformaMovil(Plataforma):
	change_x = 0
	change_y = 0

	lim_top 	= 0
	lim_bottom 	= 0
	lim_left 	= 0
	lim_right 	= 0

	nivel = None
	player = None

	def update(self):
		# Move left/right
		self.rect.x += self.change_x

		# See if we hit the player
		hit = pygame.sprite.collide_rect(self, self.player)
		if hit:
			# We did hit the player. Shove the player around and
			# assume he/she won't hit anything else.

			# If we are moving right, set our right side
			# to the left side of the item we hit
			if self.change_x < 0:
				self.player.rect.right = self.rect.left
			else:
				# Otherwise if we are moving left, do the opposite.
				self.player.rect.left = self.rect.right

		# Move up/down
		self.rect.y += self.change_y

		# Check and see if we the player
		hit = pygame.sprite.collide_rect(self, self.player)
		if hit:
			# We did hit the player. Shove the player around and
			# assume he/she won't hit anything else.

			# Reset our position based on the top/bottom of the object.
			if self.change_y < 0:
				self.player.rect.bottom = self.rect.top
			else:
				self.player.rect.top = self.rect.bottom

		# Check the boundaries and see if we need to reverse
		# direction.
		if self.rect.bottom > self.lim_bottom or self.rect.top < self.lim_top:
			self.change_y *= -1

		cur_pos = self.rect.x - self.nivel.mov_x
		if cur_pos < self.lim_left or cur_pos > self.lim_right:
			self.change_x *= -1

class Nivel(object):
	#lista sprite todos los niveles
	plataforma_lista = None
	enemigos_lista = None

	fondo = None
	mov_x = 0
	mov_y = 0
	limite_x = -1000
	limite_y = -1000

	def __init__(self,jugador):
		self.plataforma_lista = pygame.sprite.Group()
		self.enemigos_lista = pygame.sprite.Group()
		self.jugador = jugador

	def update(self):
		self.plataforma_lista.update()
		self.enemigos_lista.update()

	def draw(self, pantalla):
		pantalla.fill(BLUE)
		pantalla.blit(self.fondo, (self.mov_x // 2,self.mov_y // 2))

		self.plataforma_lista.draw(pantalla)
		self.enemigos_lista.draw(pantalla)

	def Mover_x(self, mov_xx):
		self.mov_x += mov_xx

		for platforma in self.plataforma_lista:
			platforma.rect.x += mov_xx

		for enemigos in self.enemigos_lista:
			enemigos.rect.x += mov_xx

	def Mover_y(self, mov_yy):
		self.mov_y += mov_yy

		for platforma in self.plataforma_lista:
			platforma.rect.y += mov_yy

		for enemigos in self.enemigos_lista:
			enemigos.rect.y += mov_yy

class Nivel_01(Nivel):
	def __init__(self, jugador):
		Nivel.__init__(self, jugador)

		self.fondo = pygame.image.load("img/NinjaVsEsmad_back01.png").convert()
		self.limite_x = -4000
		self.limite_y = -1000

		nivel = [	[METAL_IZQ, 800, 450],
					[METAL_MED, 870, 450],
					[METAL_DER, 940, 450]

					]

		for plataforma in nivel:
			bloque = Plataforma(plataforma[0])
			bloque.rect.x = plataforma[1]
			bloque.rect.y = plataforma[2]
			bloque.jugador = self.jugador
			self.plataforma_lista.add(bloque)

		block = PlataformaMovil(METAL_MED)
		block.rect.x = 1100
		block.rect.y = 450
		block.lim_top = 100
		block.lim_bottom = 450
		block.change_y = 5
		block.lim_left = 1100
		block.lim_right = 1600
		block.change_x = 5
		block.player = self.jugador
		block.nivel = self
		self.plataforma_lista.add(block)


class Nivel_02(Nivel):
	def __init__(self,jugador):
		Nivel.__init__(self,jugador)

		self.fondo = pygame.image.load("img/NinjaVsEsmad_back01.png").convert()
		self.limite_x = -4000
		self.limite_y = -1000

		nivel = [	[METAL_IZQ, 800, 450],
					[METAL_MED, 870, 450],
					[METAL_DER, 940, 450]

					]

		for plataforma in nivel:
			bloque = Plataforma(plataforma[0])
			bloque.rect.x = plataforma[1]
			bloque.rect.y = plataforma[2]
			bloque.jugador = self.jugador
			self.plataforma_lista.add(bloque)


def texto(text, font, color = BLACK):
	txt = font.render(text, True, color)
	return txt, txt.get_rect()

def boton(msg,x,y,w,h,action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	font = pygame.font.SysFont("impact",20)

	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(screen, BLACK,(x,y,w,h))
		txt, txtRect = texto(msg, font, WHITE)
		if click[0] == 1 and action != None:
			action()
	else:
		pygame.draw.rect(screen, WHITE,(x,y,w,h))
		txt, txtRect = texto(msg, font)

	txtRect.center = ( (x+(w/2)), (y+(h/2)) )
	screen.blit(txt, txtRect)

def salir():
	pygame.quit()
	quit()

def intro():
    listo = False
    intro = True
    pag = 1
    while intro:
    	for event in pygame.event.get():
    		if event.type == pygame.QUIT:
    			salir()
    		if event.type == pygame.MOUSEBUTTONDOWN:
    			pag += 1
    			if pag == 3:
    				intro = False

    	screen.fill(BLACK)

    	if pag == 1:
    		image = pygame.image.load("img/0_intro.png")
    		screen.blit(image,(0,0))

    	if pag == 2:
    		image = pygame.image.load("img/1_declaracion.png")
    		screen.blit(image,(0,0))

    	pygame.display.update()
        clock.tick(20)

def instrucciones():
	instrucciones = True
	while instrucciones:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		screen.fill(WHITE)

		image = pygame.image.load("img/3_instrucciones.png")
		screen.blit(image,(0,0))

		boton("Volver",300,520,200,50,menu)

		pygame.display.update()
		clock.tick(15)

def creditos():
	creditos = True
	while creditos:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		screen.fill(BLACK)

		#image = pygame.image.load("img/3_instrucciones.png")
		#screen.blit(image,(0,0))

		boton("Volver",10,10,100,30,menu)

		pygame.display.update()
		clock.tick(15)

def menu():
	menu = True
	while menu:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		screen.fill(WHITE)

		image = pygame.image.load("img/2_menu.png")
		screen.blit(image,(0,0))

		boton("Jugar",300,250,200,50,main)
		boton("Instrucciones",300,310,200,50,instrucciones)
		boton("Creditos",300,370,200,50,creditos)
		boton("Salir",300,440,200,50,salir)

		pygame.display.update()
		clock.tick(15)


def main():
	jugador = Ninja()

	nivel_lista = []
	nivel_lista.append( Nivel_01(jugador) )
	nivel_lista.append( Nivel_02(jugador) )

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
				salir()

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
			nivel_actual.Mover_x(-dif)

		#avanza a la izquierda
		if jugador.rect.right <= 120:
			dif = 120 - jugador.rect.x
			jugador.rect.x = 120
			nivel_actual.Mover_x(dif)

		#final del nivel
		pos_actual_x = jugador.rect.x + nivel_actual.mov_x
		print pos_actual_x
		if (pos_actual_x < nivel_actual.limite_x):
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
		intro()
		menu()
		main()
