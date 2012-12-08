import pygame
import os
import random
from pygame.locals import *
ANCHO = 450
ALTO = 500

def cargar_imagen(filename, transparent = False):
	try:
		image = pygame.image.load(filename)
	except pygame.error, message:
		raise SystemExit, message
	image = image.convert()
	if transparent:
		color = image.get_at((0, 0))
		image.set_colorkey(color, RLEACCEL)
	return image
def load_image(name, colorkey = False):
	fullname = os.path.join("TOOLS", name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error, message:
		print "No se puede cargar la imagen", fullname
		raise SystemExit, message
	if colorkey:
		colorkey = image.get_at((0, 0))
		image.set_colorkey(colorkey, RLEACCEL)
	return (image, image.get_rect())
class MoverPista(pygame.sprite.Sprite):
	def __init__(self, starpos):
		pygame.sprite.Sprite.__init__(self)
		(self.image, self.rect) = load_image("LINEA_PISTA.png", True)
		self.rect.center = starpos
	def update(self):
		if self.rect.bottom <= 0:
			self.kill()
		else:
			self.rect.move_ip(0, 1)
class AutoEnemigo(pygame.sprite.Sprite):
	def __init__(self, starpos):
		pygame.sprite.Sprite.__init__(self)
		self.car_select = random.randint(1,3)
		if self.car_select == 1:
			(self.image, self.rect) = load_image("CPU_1.png", True)
		elif self.car_select == 2:
			(self.image, self.rect) = load_image("CPU_2.png", True)
		elif self.car_select == 3:
			(self.image, self.rect) = load_image("CPU_3.png", True)
		self.rect.center = starpos
	def update(self):
		if self.rect.bottom <= 0:
			self.kill()
		else:
			self.rect.move_ip(0, 2)
class Jugador(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		(self.image, self.rect) = load_image("PLAYER_1.png", True)
		self.rect = self.image.get_rect()
		self.invisible_counter = 0
		self.rect.centerx = 150
		self.rect.centery = 440
	def can_be_killed(self):
		return self.invisible_counter <= 0
	def mover(self, teclas):
		self.rect.center = (self.rect.centerx, self.rect.centery)
		if self.rect.left > 30:
			if teclas[K_LEFT]:
				self.rect.centerx -= 90 # Variable 45
		if self.rect.right <= 260:
			if teclas[K_RIGHT]:
				self.rect.centerx += 90 # Variable 45
		if self.rect.top >= 100:
			if teclas[K_UP]:
				self.rect.centery -= 45
		if self.rect.bottom <= 460:
			if teclas[K_DOWN]:
				self.rect.centery += 45
	def update(self):
		self.update_invisible_counter()
		self.rect.center = (self.rect.centerx, self.rect.centery)
	def update_invisible_counter(self):
		if self.invisible_counter > 0:
			self.invisible_counter -= 1
			if self.invisible_counter > 100:
				self.image.set_alpha(0)
			else:
				self.image.set_alpha(255 - self.invisible_counter * 2)
		else:
			self.image.set_alpha(255)
	def set_invisible(self):
		self.invisible_counter = 200
class JugadorArma(pygame.sprite.Sprite):
	def __init__(self, starpos):
		pygame.sprite.Sprite.__init__(self)
		(self.image, self.rect) = load_image("BALA_PLAYER.png", True)
		self.rect.center = starpos
	def update(self):
		if self.rect.bottom <= 0:
			self.kill()
		else:
			self.rect.move_ip(0, -2)
class Explosion(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self._load_image()
		self.step = 0
		self.delay = 2
		(self.image,self.rect) = load_image("CHOQUE/1.png", True)
		self.rect.center = (x, y)
	def _load_image(self):
		self.frames  = []
		for n in range(1, 8):
			path = "CHOQUE/%d.png"
			new_image = load_image(path % n, True)[0]
			self.frames.append(new_image)
	def update(self):
		self.image = self.frames[self.step]
		if self.delay < 0:
			self.delay = 2
			self.step += 1
			if self.step > 6:
				self.kill()
		else:
			self.delay -= 1
def mostrar_progreso(fuente, visor, puntaje, nivel, jugador, misiles):
	white = (255, 255, 255)
	puntos_image = fuente.render(str(puntaje), 1, white, (0, 0, 0))
	nivel_image = fuente.render(str(nivel), 1, white, (0, 0, 0))
	nombre_image = fuente.render(jugador, 1, white, (0, 0, 0))
	misiles_image = fuente.render(str(misiles), 1, white, (0, 0, 0))
	visor.blit(puntos_image, (360, 175))
	visor.blit(nivel_image, (360, 275))
	visor.blit(misiles_image, (360, 375))
	visor.blit(nombre_image, (310, 460))
def menu(fuente, texto, color, visor, position):
	imprimir = fuente.render(texto, True, color)
	visor.blit(imprimir, position)
def nombre_jug(fuente, caracter, visor):
	letra = fuente.render(caracter, True, (0, 0, 0), (255, 255, 255))
	visor.blit(letra, (10, 260))
def principal():
	pygame.init
	visor = pygame.display.set_mode((ANCHO, ALTO))
	pygame.display.set_caption("Carrera F1")
	fondo_game_1 = cargar_imagen("TOOLS/PISTA_1.jpg")
	fondo_game_2 = cargar_imagen("TOOLS/MENU.jpg")
	visor.blit(fondo_game_1, (0, 0))
	sprites = pygame.sprite.RenderClear()
	linea_pista = pygame.sprite.RenderClear()
	carro_enemigo = pygame.sprite.RenderClear()
	disparo_jugador = pygame.sprite.RenderClear()
	jugador = Jugador()
	sprites.add(jugador)
	reloj = pygame.time.Clock()
	speed1 = 0.2
	speed2 = 0.2
	speed3 = 0.2
	control_time = 90
	opcion = 0
	pygame.font.init()
	fuente1 = pygame.font.Font(None, 40)
	fuente2 = pygame.font.Font("TOOLS/COOPBL.TTF", 55)
	fuente3 = pygame.font.Font("TOOLS/comicbd.ttf", 20)
	fuente4 = pygame.font.Font("TOOLS/ARLRDBD.TTF", 40)
	fuente5 = pygame.font.Font("TOOLS/ARLRDBD.TTF", 20)
	corriendo = True
	puntos = 0
	nivel = 0
	misiles = 1
	nombre = ""
	escogido1 = ""
	escogido2 = ""
	while corriendo:
		reloj.tick(control_time)
		teclas = pygame.key.get_pressed()
		speed1 += 0.2
		for event in pygame.event.get():
			if event.type == QUIT:
				corriendo = False
			elif event.type == pygame.KEYDOWN and opcion == 0:
				if event.key == pygame.K_BACKSPACE:
					if len(nombre) > 0:
						nombre = nombre[0:len(nombre) - 1]
				else:
					nombre = nombre + event.unicode
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				corriendo = False
			jugador.mover(teclas)
			if event.type == KEYDOWN and event.key == K_SPACE and misiles > 0:
				misil_1 = JugadorArma(jugador.rect.midleft)
				misil_2 = JugadorArma(jugador.rect.midright)
				new_misil = [misil_1, misil_2]
				disparo_jugador.add(new_misil)
				sprites.add(new_misil)
				misiles -= 1
		if opcion != 0:
			if speed1 > 10:
				speed2 += 0.6
				line_1 = MoverPista((105, 0))
				line_2 = MoverPista((195, 0))
				new_line = [line_1, line_2]
				linea_pista.add(new_line)
				sprites.add(new_line)
				speed1 = 0
				if speed2 > 2:
					aleatorio = random.randint(1, 3)
					if aleatorio == 1:
						posicion = (60, 0)
					elif aleatorio == 2:
						posicion = (150, 0)
					elif aleatorio == 3:
						posicion = (240, 0)
					auto = AutoEnemigo(posicion)
					new_auto = [auto]
					carro_enemigo.add(new_auto)
					sprites.add(new_auto)
					speed3 += 0.8
					if speed3 > 3:
						misiles += 1
						speed3 = 0.2
					speed2 = 0
					puntos += 10
			for hit in pygame.sprite.groupcollide(carro_enemigo, disparo_jugador, 1, 1):
					(x, y) = hit.rect.center
					sprites.add(Explosion(x, y))
			if jugador.can_be_killed():
				for hit in pygame.sprite.spritecollide(jugador, carro_enemigo, 1):
					(x, y) = hit.rect.center
					sprites.add(Explosion(x, y))
					(x, y) = jugador.rect.center
					sprites.add(Explosion(x, y))
					misiles = 0
					opcion = 0
					puntos = 0
					nivel = 0
					control_time = 90
			sprites.update()
			if puntos > 60:
				nivel += 1
				puntos = 0
				control_time += 30
			mostrar_progreso(fuente1, visor, puntos, nivel, nombre, misiles)
			sprites.clear(visor, fondo_game_1)
			sprites.draw(visor)
		else:
			visor.blit(fondo_game_2, (0, 0))
			menu(fuente2, "CATEGORIAS", (0, 255, 0), visor, (25, 0))
			menu(fuente3, "OPRIMA F1 O F2 PARA SU COCHE: ", (255, 255, 0), visor, (25, 75))
			menu(fuente4, "F1 =", (0, 0, 0), visor, (30, 150))
			menu(fuente4, "F2 =", (0, 0, 0), visor, (210, 150))
			menu(fuente5, "ESCRIBA SU NOMBRE: ", (0, 0, 255), visor, (10, 230))
			menu(fuente5, "PRESIONE F5 PARA CONTINUAR", (255, 255, 255), visor, (30, 470))
			nombre_jug(fuente5, nombre, visor)
			coche_1 = pygame.image.load("TOOLS/PLAYER_1.png")
			coche_2 = pygame.image.load("TOOLS/PLAYER_2.png")
			visor.blit(coche_1, (120, 110))
			visor.blit(coche_2, (300, 110))
			if teclas[K_F1]:
				escogido1 = "E"
				escogido2 = ""
			elif teclas[K_F2]:
				escogido2 = "E"
				escogido1 = ""
			menu(fuente2, escogido1, (255, 0, 0), visor, (130, 145))
			menu(fuente2, escogido2, (255, 0, 0), visor, (310, 145))
			if teclas[K_F5]:
				opcion = 1
				visor.blit(fondo_game_1, (0, 0))
		pygame.display.flip()
if __name__ == '__main__':
	principal()
