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
import random
from pygame.locals import *

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

START, STOP = 0, 1
pause = False

# Initialize the game engine
pygame.init()

SCREEN_WIDHT	= 800
SCREEN_HEIGHT 	= 600

SCREEN_SIZE = [SCREEN_WIDHT,SCREEN_HEIGHT]
screen =  pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("NinjaVsEsmad")
clock = pygame.time.Clock()


#audios
you_lose 	= pygame.mixer.Sound('audio/Male/you_lose.ogg')
game_over	= pygame.mixer.Sound('audio/Male/game_over.ogg')
you_win 	= pygame.mixer.Sound('audio/Male/you_win.ogg')
go_go_go 	= pygame.mixer.Sound('audio/Male/war_go_go_go.ogg')
level_up	= pygame.mixer.Sound('audio/Male/level_up.ogg')
pop_button	= pygame.mixer.Sound('audio/twoTone2.ogg')

activos_sp_lista = pygame.sprite.Group()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Explosion, self).__init__()
        sheet = pygame.image.load("img/explosion_strip16.png")
        self.images = []
        for i in range(0, 1536, 96):
            rect = pygame.Rect((i, 0, 96, 96))
            image = pygame.Surface(rect.size)
            image.blit(sheet, (0, 0), rect)
            image.set_colorkey(BLACK)
            self.images.append(image)

        self.image = self.images[0]
        self.index = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.add(activos_sp_lista)

    def update(self):
        self.image = self.images[self.index]
        self.index += 1
        if self.index >= len(self.images):
            self.kill()

class Humo(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		sprite_sheet = SpriteSheet("img/Smoke45Frames.png")

		for j in range(0,5):
			for k in range(0,6):
				image = sprite_sheet.get_image(k*256, j*256, 256, 256)
				self.images.append(image)

		self.image = self.images[0]
		self.index = 0
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.rect = self.image.get_rect()
		#self.add(activos_sp_lista)

	def update(self):
		self.image = self.images[self.index]
		self.index += 1
		if self.index >= len(self.images):
			self.kill()

class Bala( pygame.sprite.Sprite ):
	def __init__(self, px, py, dir, dxx = 0, dyy = 0 ):
		pygame.sprite.Sprite.__init__(self)
		self.dx = dxx
		self.dy = dyy
		self.image = pygame.image.load('img/bala_x.png').convert()
		if dir == "L":
			self.image = pygame.transform.flip(self.image, True, False)
			self.dx = self.dx *  -1
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = (px - (self.rect.w/2), py - (self.rect.h/2))
		

	def update(self):
		x, y = self.rect.center
		x += self.dx
		y += self.dy
		self.rect.center = x, y
		if x >= SCREEN_WIDHT:
			self.kill()

class Bomba( pygame.sprite.Sprite ):

	nivel = None

	def __init__(self, px, py, dxx = 0, dyy = 0 ):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/bomb.png").convert_alpha()
		self.image = pygame.transform.scale(self.image,(32,32))
		#self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = (px - (self.rect.w/2), py - (self.rect.h/2))
		self.dx = dxx
		self.dy = dyy

		self.explosion_sound = pygame.mixer.Sound("audio/Shotgun.ogg")
  		self.explosion_sound.set_volume(0.4)

	def update(self):
		x, y = self.rect.center
		x += self.dx
		y += self.dy
		self.rect.center = x, y
		if y >= SCREEN_HEIGHT - 70:
			self.kill()

	def kill(self):
		x, y = self.rect.center
		if pygame.mixer.get_init():
			self.explosion_sound.play(maxtime=1000)
			#Humo(x, y)
		super(Bomba, self).kill()

class SpriteSheet(object):
	sprite_sheet = None

	def __init__(self, file_name):
		self.sprite_sheet = pygame.image.load(file_name).convert()

	def get_image(self, x, y, width, height):
		image = pygame.Surface([width, height]).convert()
		image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
		image.set_colorkey(BLACK)

		return image

class ScoreBoard(pygame.sprite.Sprite):
	def __init__(self, jugador):
		super(ScoreBoard, self).__init__()
		self.image = pygame.Surface((120, 120)).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = 10
		self.rect.y = 10

		self.font = pygame.font.SysFont("impact",20)

		self.jugador = jugador

	def update(self):
		level = self.font.render("Nivel : {}".format(self.jugador.nivel.nivel_no), True, (150, 50, 50))
		health = self.font.render("Salud : {}%".format(self.jugador.health), True, (150, 50, 50))
		score = self.font.render("Puntos : {}".format(self.jugador.score), True, (150, 50, 50))
		ammo = self.font.render("Balas : {}".format(self.jugador.ammo), True, (150, 50, 50))
		self.image.fill(WHITE)
		self.image.blit(level, (5, 2))
		self.image.blit(health, (5, 32))
		self.image.blit(score, (5, 62))
		self.image.blit(ammo, (5, 92))

	def kill(self):
		super(ScoreBoard, self).kill()

class Ninja( pygame.sprite.Sprite ):
	vel_x = 0
	vel_y = 0

	frames_der = []
	frames_izq = []

	direccion = "R"
	nivel = None

	health = 100
	ammo = 12
	score = 0

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
		self.firing = self.shot = False
		

	def update(self):
		self.calc_grav()
		x, y = self.rect.center

		if self.firing and self.ammo > 0:
			self.shot = Bala(x+30, y+25, self.direccion, 10)
			self.shot.add(self.nivel.disparos_lista)
			#self.shot.add(self.nivel.plataforma_lista)
			self.ammo -= 1
			self.firing = False

		if self.health < 0:
			self.kill()

		#mov izq der
		self.rect.x += self.vel_x
		pos_x = self.rect.x + self.nivel.mov_x
		if self.direccion == "R":
			frame = (pos_x // 15) % len(self.frames_der)
			self.image = self.frames_der[frame]
		else:
			frame = (pos_x // 15) % len(self.frames_izq)
			self.image = self.frames_izq[frame]

		#colision con plataforma
		bloque_col_list = pygame.sprite.spritecollide(self, self.nivel.plataforma_lista, False)

		for bloque in bloque_col_list:
				if self.vel_x > 0:
					self.rect.right = bloque.rect.left
				elif self.vel_x < 0:
					self.rect.left = bloque.rect.right

		#mov arriba y abajo
		self.rect.y += self.vel_y

		#colision con plataforma
		bloque_col_list = pygame.sprite.spritecollide(self, self.nivel.plataforma_lista,False)

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

	def shoot(self, operation):
		if operation == START:
			self.firing = True
		if operation == STOP:
			self.firing = False

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

	def kill(self):
		super(Ninja, self).kill()

class Esmad( pygame.sprite.Sprite ):
	change_x = 0
	change_y = 0

	frames = []

	lim_left = 0
	lim_right = 0

	player = None
	nivel = None

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		sprite_sheet = SpriteSheet("img/esmad.png")

		image = sprite_sheet.get_image(0, 0, 66, 90)
		self.frames.append(image)

		image = sprite_sheet.get_image(66, 0, 66, 90)
		self.frames.append(image)

		image = sprite_sheet.get_image(132, 0, 67, 90)
		self.frames.append(image)

		image = sprite_sheet.get_image(0, 93, 66, 90)
		self.frames.append(image)

		image = sprite_sheet.get_image(66, 93, 66, 90)
		self.frames.append(image)

		image = sprite_sheet.get_image(132, 93, 72, 90)
		self.frames.append(image)

		image = sprite_sheet.get_image(0, 186, 70, 90)
		self.frames.append(image)

		self.image = self.frames[0]

		self.rect = self.image.get_rect()

		self.explosion_sound = pygame.mixer.Sound("audio/Explosion.ogg")
  		self.explosion_sound.set_volume(0.4)
  		self.firing = self.shot = False
  		self.ronda = 0

	def update(self):
		self.calc_grav()

		#mov izq der
		self.rect.x += self.change_x
		pos_x = self.rect.x + self.nivel.mov_x

		frame = (pos_x // 15) % len(self.frames)
		self.image = self.frames[frame]

		#colision con el jugador
		hit = pygame.sprite.collide_rect(self, self.player)
		if hit:
			#self.player.health -= 20 
			if self.change_x < 0:
				self.player.rect.right = self.rect.left
			else:
				self.player.rect.left = self.rect.right

		#colision con las plataformas
		bloque_col_list = pygame.sprite.spritecollide(self, self.nivel.plataforma_lista, False)
		for bloque in bloque_col_list:
				if self.change_x > 0:
					self.rect.right = bloque.rect.left
				elif self.change_x < 0:
					self.rect.left = bloque.rect.right

		#mov arriba y abajo
		self.rect.y += self.change_y

		#colision con el jugador
		hit = pygame.sprite.collide_rect(self, self.player)
		if hit:
			if self.change_y < 0:
				self.player.rect.bottom = self.rect.top
			else:
				self.player.rect.top = self.rect.bottom

		#colision con las plataformas
		bloque_col_list = pygame.sprite.spritecollide(self, self.nivel.plataforma_lista, False)
		for bloque in bloque_col_list:
				if self.change_y > 0:
					self.rect.bottom = bloque.rect.top
				elif self.change_y < 0:
					self.rect.top = bloque.rect.bottom

				self.vel_y = 0

		cur_pos = self.rect.x - self.nivel.mov_x
		if cur_pos < self.lim_left or cur_pos > self.lim_right:
			self.change_x *= -1
			self.ronda += 1
			
		if self.ronda == 4:
			self.firing = True
			self.ronda = 0

		#print self.ronda 
		x, y = self.rect.center

		if self.firing:
			self.bomb = Bomba(x+30, y+25, -6, 1)
			self.bomb.nivel = self.nivel
			self.bomb.add(self.nivel.bomba_lista)
			#self.puff.add(self.nivel.plataforma_lista)
			self.firing = False

	def calc_grav(self):
		if self.change_y == 0:
			self.change_y = 1
		else:
			self.change_y += 0.35

		#esta en el suelo
		if self.rect.y >= (SCREEN_HEIGHT - 70) - self.rect.height and self.change_y >= 0:
			self.change_y = 0
			self.rect.y = (SCREEN_HEIGHT - 70) - self.rect.height

	def no_mover(self):
		self.change_x = 0

	def kill(self):
		x, y = self.rect.center
		if pygame.mixer.get_init():
			self.explosion_sound.play(maxtime=1000)
			Explosion(x, y)
		super(Esmad, self).kill()

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

		hit = pygame.sprite.collide_rect(self, self.player)
		if hit:
			if self.change_x < 0:
				self.player.rect.right = self.rect.left
			else:
				self.player.rect.left = self.rect.right

		# Move up/down
		self.rect.y += self.change_y

		hit = pygame.sprite.collide_rect(self, self.player)
		if hit:
			if self.change_y < 0:
				self.player.rect.bottom = self.rect.top
			else:
				self.player.rect.top = self.rect.bottom

		if self.rect.y > self.lim_bottom or self.rect.y < self.lim_top:
			self.change_y *= -1

		cur_pos = self.rect.x - self.nivel.mov_x
		if cur_pos < self.lim_left or cur_pos > self.lim_right:
			self.change_x *= -1

class Nivel(object):
	#lista sprite todos los niveles
	plataforma_lista = None
	enemigos_lista = None
	disparos_lista = None
	bomba_lista = None
	humo_lista = None

	nivel_no = None

	fondo = None
	mov_x = 0
	mov_y = 0
	limite_x = -1000
	limite_y = -1000

	def __init__(self,jugador):
		self.plataforma_lista = pygame.sprite.Group()
		self.enemigos_lista = pygame.sprite.Group()
		self.disparos_lista = pygame.sprite.Group()
		self.bomba_lista = pygame.sprite.Group()
		self.humo_lista = pygame.sprite.Group()
		self.jugador = jugador

	def update(self):
		self.plataforma_lista.update()
		self.enemigos_lista.update()
		self.disparos_lista.update()
		self.bomba_lista.update()
		self.humo_lista.update()

	def draw(self, pantalla):
		pantalla.fill(BLUE)
		pantalla.blit(self.fondo, (self.mov_x // 2,self.mov_y // 2))

		self.plataforma_lista.draw(pantalla)
		self.enemigos_lista.draw(pantalla)
		self.disparos_lista.draw(pantalla)
		self.bomba_lista.draw(pantalla)
		self.humo_lista.draw(pantalla)

	def Mover_x(self, mov_xx):
		self.mov_x += mov_xx

		for platforma in self.plataforma_lista:
			platforma.rect.x += mov_xx

		for enemigos in self.enemigos_lista:
			enemigos.rect.x += mov_xx

		for disparos in self.disparos_lista:
			disparos.rect.x += mov_xx

		for bomba in self.bomba_lista:
			bomba.rect.x += mov_xx

		for humo in self.humo_lista:
			humo.rect.x += mov_xx

	def Mover_y(self, mov_yy):
		self.mov_y += mov_yy

		for platforma in self.plataforma_lista:
			platforma.rect.y += mov_yy

		for enemigos in self.enemigos_lista:
			enemigos.rect.y += mov_yy

		for disparos in self.disparos_lista:
			disparos.rect.y += mov_yy

		for bomba in self.bomba_lista:
			bomba.rect.y += mov_yy

		for humo in self.humo_lista:
			humo.rect.y += mov_yy

class Nivel_01(Nivel):
	def __init__(self, jugador):
		Nivel.__init__(self, jugador)

		self.fondo = pygame.image.load("img/NinjaVsEsmad_back01.png").convert()
		self.limite_x = -4000
		self.limite_y = -1000

		self.nivel_no = 1

		nivel = [	[METAL_IZQ, 500, 250],
					[METAL_MED, 570, 250],
					[METAL_DER, 640, 250],

					[METAL_IZQ, 800, 350],
					[METAL_MED, 870, 350],
					[METAL_DER, 940, 350],

					[METAL_IZQ, 1580, 450],
					[METAL_DER, 1650, 450],

					[METAL_IZQ, 1790, 350],
					[METAL_DER, 1860, 350],

					[METAL_IZQ, 2000, 350],
					[METAL_DER, 2070, 350],

					[METAL_IZQ, 2210, 450],
					[METAL_DER, 2280, 450],

					[METAL_IZQ, 2420, 350],
					[METAL_DER, 2490, 350],

					[METAL_IZQ, 2630, 350],
					[METAL_DER, 2700, 350]

					
					]

		for i in range(6):
			esmad = Esmad()
			esmad.nivel = self
			#pos = random.randint(400, SCREEN_WIDHT)
			pos = random.randint(SCREEN_WIDHT, (self.limite_x*-1))
			esmad.rect.x = pos
			esmad.rect.y = (SCREEN_HEIGHT - 70) - jugador.rect.height
			esmad.lim_left = pos - random.randint(50,200)
			esmad.lim_right = pos + random.randint(50,200)
			esmad.change_x = random.randint(1,3)
			esmad.change_y = 0
			esmad.player = self.jugador
			self.enemigos_lista.add(esmad)

		for plataforma in nivel:
			bloque = Plataforma(plataforma[0])
			bloque.rect.x = plataforma[1]
			bloque.rect.y = plataforma[2]
			bloque.jugador = self.jugador
			self.plataforma_lista.add(bloque)

		# for i in range(0,80):
		# 	bloque = Plataforma(plataforma[0])
		# 	bloque.rect.x = (i*70)
		# 	bloque.rect.y = 530
		# 	bloque.jugador = self.jugador
		# 	self.plataforma_lista.add(bloque)

		block = PlataformaMovil(METAL_MED)
		block.rect.x = 1100
		block.rect.y = 200
		block.lim_top = 200
		block.lim_bottom = 450
		block.change_y = 1
		block.change_x = 0
		block.player = self.jugador
		block.nivel = self
		self.plataforma_lista.add(block)

		block = PlataformaMovil(METAL_MED)
		block.rect.x = 1200
		block.rect.y = 200
		block.lim_left = 1200
		block.lim_right = 1700
		block.change_y = 0
		block.change_x = 2
		block.player = self.jugador
		block.nivel = self
		self.plataforma_lista.add(block)

		block = PlataformaMovil(METAL_MED)
		block.rect.x = 2800
		block.rect.y = 200
		block.lim_top = 200
		block.lim_bottom = 450
		block.change_y = 1
		block.change_x = 0
		block.player = self.jugador
		block.nivel = self
		self.plataforma_lista.add(block)

		block = PlataformaMovil(METAL_MED)
		block.rect.x = 2900
		block.rect.y = 200
		block.lim_left = 2900
		block.lim_right = 3400
		block.change_y = 0
		block.change_x = 2
		block.player = self.jugador
		block.nivel = self
		self.plataforma_lista.add(block)

class Nivel_02(Nivel):
	def __init__(self,jugador):
		Nivel.__init__(self,jugador)

		self.fondo = pygame.image.load("img/NinjaVsEsmad_back02.png").convert()
		self.limite_x = -1000
		self.limite_y = -2000

		self.nivel_no = 2

		# for i in range(3):
		# 	esmad = Esmad()
		# 	esmad.nivel = self
		# 	#pos = random.randint(400, SCREEN_WIDHT)
		# 	posy = random.randint(SCREEN_HEIGHT, (self.limite_y*-1))
		# 	posx = random.randint(0, SCREEN_WIDHT)
		# 	esmad.rect.x = posx
		# 	esmad.rect.y = posy
		# 	esmad.lim_left = random.randint(0,posx)
		# 	esmad.lim_right = random.randint(posx,SCREEN_WIDHT)
		# 	esmad.change_x = random.randint(1,3)
		# 	esmad.change_y = 0
		# 	esmad.player = self.jugador
		# 	self.enemigos_lista.add(esmad)

		nivel = [	[METAL_MED, 0, 530],
					[METAL_MED, 70, 530],
					[METAL_MED, 140, 530],
					[METAL_MED, 210, 530],
					[METAL_MED, 280, 530],
					[METAL_MED, 350, 530],
					[METAL_MED, 420, 530],
					[METAL_DER, 490, 530],
					
					[METAL_IZQ, 490, 730],
					[METAL_MED, 560, 730],
					[METAL_MED, 630, 730],					
					[METAL_MED, 700, 730],
					[METAL_MED, 770, 730],

					[METAL_IZQ, 350, 930],
					[METAL_DER, 420, 930],
					
					[METAL_IZQ, 210, 1030],
					[METAL_DER, 280, 1030],				

					[METAL_MED, 0, 1230],
					[METAL_MED, 70, 1230],
					[METAL_DER, 140, 1230],

					[METAL_IZQ, 560, 1230],
					[METAL_MED, 630, 1230],
					[METAL_MED, 700, 1230],
					[METAL_DER, 770, 1230],

					[METAL_IZQ, 140, 1430],
					[METAL_MED, 210, 1430],
					[METAL_MED, 280, 1430],
					[METAL_MED, 350, 1430],
					[METAL_MED, 420, 1430],
					[METAL_MED, 490, 1430],
					[METAL_MED, 560, 1430],
					[METAL_MED, 630, 1430],					
					[METAL_MED, 700, 1430],
					[METAL_MED, 770, 1430],

					[METAL_MED, 0, 2750],
					[METAL_MED, 70, 2750],
					[METAL_MED, 140, 2750],
					[METAL_MED, 210, 2750],
					[METAL_DER, 280, 2750],
					#[METAL_MED, 350, 2750],
					#[METAL_MED, 420, 2750],
					[METAL_IZQ, 490, 2750],
					[METAL_MED, 560, 2750],
					[METAL_MED, 630, 2750],
					[METAL_MED, 700, 2750],
					[METAL_MED, 770, 2750]
					]

		for plataforma in nivel:
			bloque = Plataforma(plataforma[0])
			bloque.rect.x = plataforma[1]
			bloque.rect.y = plataforma[2]
			bloque.jugador = self.jugador
			self.plataforma_lista.add(bloque)

		block = PlataformaMovil(METAL_MED)
		block.rect.x = 400
		block.rect.y = 200
		block.lim_top = 200
		block.lim_bottom = 450
		block.change_y = 1
		block.change_x = 0
		block.player = self.jugador
		block.nivel = self
		self.plataforma_lista.add(block)

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
		pygame.mixer.Sound.play(pop_button)
		#pop_button.stop()
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

def unpause():
	global pause
	pygame.mixer.music.unpause()
	pause = False

def paused(score):
	pygame.mixer.music.pause()
	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
				
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					unpause()

		screen.fill(WHITE)

		image = pygame.image.load("img/2_menu.png")
		screen.blit(image,(0,0))

		boton("PAUSA", 			300,240,200,50)

		scr = "Puntaje: "+str(score)
		boton(scr, 				300,300,200,50)

		boton("Continuar",		300,360,200,50,unpause)
		#boton("Menu principal",	300,420,200,50,menu)
		boton("Salir",			300,430,200,50,salir)

		pygame.display.update()
		clock.tick(15)   

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
        clock.tick(15)

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

		image = pygame.image.load("img/4_creditos.png")
		screen.blit(image,(0,0))

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

def end_game(score,msg):
	end_game = True

	if msg == "GAME OVER":
		game_over.play()
	if msg == "YOU WIN":
		you_win.play()

	while end_game:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		screen.fill(WHITE)

		image = pygame.image.load("img/2_menu.png")
		screen.blit(image,(0,0))

		boton(msg, 		300,240,200,50)

		scr = "Puntaje: "+str(score)
		boton(scr, 				300,300,200,50)

		boton("Jugar de nuevo",	300,360,200,50,main)
		boton("Menu principal",	300,420,200,50,menu)
		boton("Salir",			300,490,200,50,salir)

		pygame.display.update()
		clock.tick(15)

def main():
	global pause

	jugador = Ninja()
	jugador.health = 100
	jugador.score = 0
	jugador.ammo = 12
	puntaje = ScoreBoard(jugador)

	nivel_lista = []
	nivel_lista.append( Nivel_01(jugador) )
	nivel_lista.append( Nivel_02(jugador) )

	nivel_actual_no = 0
	nivel_actual = nivel_lista[nivel_actual_no]

	

	jugador.nivel = nivel_actual
	jugador.rect.x = 1000
	jugador.rect.y = (SCREEN_HEIGHT - 70) - jugador.rect.height

	
	pygame.mixer.music.load('audio/Battle.ogg')
	pygame.mixer.music.set_volume(0.4)
	pygame.mixer.music.play(1)
	
	activos_sp_lista.add(jugador)
	activos_sp_lista.add(puntaje)

	fin = False
	reloj = pygame.time.Clock()
	go_go_go.play()

	while not fin:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				fin = True
				salir()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					jugador.ir_izq()
				if event.key == pygame.K_d:
					jugador.ir_der()
				if event.key == pygame.K_w:
					jugador.salto()
				if event.key == pygame.K_SPACE:
					jugador.shoot(START)
				if event.key == pygame.K_ESCAPE:
					pause = True
					paused(jugador.score)

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a and jugador.vel_x < 0:
					jugador.no_mover()
				if event.key == pygame.K_d and jugador.vel_x > 0:
					jugador.no_mover()
				if event.key == pygame.K_SPACE:
					jugador.shoot(STOP)

		activos_sp_lista.update()
		nivel_actual.update()

		hit_esmad_bala = pygame.sprite.groupcollide(nivel_actual.enemigos_lista, nivel_actual.disparos_lista, True, True)
		for k, v in hit_esmad_bala.iteritems():
			k.kill()
			for i in v:
				i.kill()
				jugador.score += 10

		hit_ninja_bomb = pygame.sprite.spritecollide(jugador, nivel_actual.bomba_lista, True)
		for i in hit_ninja_bomb:
			jugador.health -= 50

		hit_ninja_esmad = pygame.sprite.spritecollide(jugador, nivel_actual.enemigos_lista, True)
		for i in hit_ninja_esmad:
			jugador.health -= 20


		#GAME OVER
		if jugador.health <= 0:
			prev_score = jugador.score
			puntaje.kill()
			jugador.kill()
			for i in nivel_actual.enemigos_lista:
				i.kill()
			end_game(prev_score,"GAME OVER")

		#WINNER
		if jugador.score >= 90:
			prev_score = jugador.score
			puntaje.kill()
			jugador.kill()
			for i in nivel_actual.enemigos_lista:
				i.kill()
			end_game(prev_score,"YOU WIN")

		
		#control del nivel 1
		if nivel_actual.nivel_no == 1:
			
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

			#final del nivel 1
			pos_actual_x = jugador.rect.x + nivel_actual.mov_x
			#print pos_actual_x
			if (pos_actual_x < nivel_actual.limite_x):
				jugador.rect.x = 120
				if (nivel_actual_no < len(nivel_lista)-1):
					level_up.play()
					nivel_actual_no += 1
					nivel_actual = nivel_lista[nivel_actual_no]
					jugador.nivel = nivel_actual
					jugador.ammo = 12

			if jugador.rect.left < 0:
				jugador.rect.left = 0

		#control del nivel 2
		if nivel_actual.nivel_no == 2:
			#limita a borde izquierdo
			if jugador.rect.left < 0:
				jugador.rect.left = 0

			for esmad in nivel_actual.enemigos_lista:
				if esmad.rect.left < 0:
					esmad.rect.left = 0

			#limita a borde derecho
			if jugador.rect.right > SCREEN_WIDHT:
				jugador.rect.right = SCREEN_WIDHT

			for esmad in nivel_actual.enemigos_lista:
				if esmad.rect.right > SCREEN_WIDHT:
					esmad.rect.right = SCREEN_WIDHT

			#sube
			if jugador.rect.top >= 400:
				dif = jugador.rect.y - 400
				jugador.rect.y = 400
				nivel_actual.Mover_y(-dif)

			#baja
			if jugador.rect.top <= 120:
				dif = 120 - jugador.rect.y
				jugador.rect.y = 120
				nivel_actual.Mover_y(dif)

			#final del nivel 2
			pos_actual_y = jugador.rect.y + nivel_actual.mov_y
			
			if (pos_actual_y < nivel_actual.limite_y):
				jugador.rect.y = 120
				prev_score = jugador.score
				puntaje.kill()
				jugador.kill()
				for i in nivel_actual.enemigos_lista:
					i.kill()
				end_game(prev_score,"YOU WIN")
				

		nivel_actual.draw(screen)
		activos_sp_lista.draw(screen)
		reloj.tick(60)
		pygame.display.flip()

if __name__ == "__main__":
		intro()
		menu()
		main()
