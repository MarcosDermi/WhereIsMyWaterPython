import pygame
import os
from lib.Var import ANCHO, ALTO

class Botella:
	@property
	def rect(self):
		return self._rect

	@rect.setter
	def rect(self, value):
		self._rect = value

	@property
	def gotas_recibidas(self):
		return self._gotas_recibidas

	@gotas_recibidas.setter
	def gotas_recibidas(self, value):
		self._gotas_recibidas = value
	def __init__(self, x, y, ancho=60, alto=80):
		self._rect = pygame.Rect(x-ancho//2, y-alto, ancho, alto)
		self._gotas_recibidas = 0
	def draw(self, surf, mostrar_llena=False):
		recipiente_img_path = os.path.join("lib", "Sprite", "Fondos", "agua.png")
		if mostrar_llena:
			recipiente_img_path = os.path.join("lib", "Sprite", "Fondos", "agua (1).png")
		if os.path.exists(recipiente_img_path):
			recipiente_img = pygame.image.load(recipiente_img_path)
			recipiente_img = pygame.transform.scale(recipiente_img, (self._rect.width, self._rect.height))
			surf.blit(recipiente_img, (self._rect.left, self._rect.top))
		else:
			cubo_rect = self._rect.inflate(-10, 0)
			pygame.draw.rect(surf, (200, 200, 220), cubo_rect)
			pygame.draw.rect(surf, (80, 80, 100), cubo_rect, 4)
			pygame.draw.rect(surf, (120, 120, 140), (cubo_rect.left, cubo_rect.top, cubo_rect.width, 12))
			cx = cubo_rect.centerx
			top = cubo_rect.top
			r = cubo_rect.width // 2
			pygame.draw.arc(surf, (80, 80, 100), (cx - r, top - r//2, 2*r, r), 3.14, 0, 4)
	def recibe_gota(self):
		self._gotas_recibidas += 1

class Gota:
	@property
	def x(self):
		return self._x

	@x.setter
	def x(self, value):
		self._x = value

	@property
	def y(self):
		return self._y

	@y.setter
	def y(self, value):
		self._y = value

	@property
	def vx(self):
		return self._vx

	@vx.setter
	def vx(self, value):
		self._vx = value

	@property
	def vy(self):
		return self._vy

	@vy.setter
	def vy(self, value):
		self._vy = value

	@property
	def radio(self):
		return self._radio

	@radio.setter
	def radio(self, value):
		self._radio = value

	@property
	def color(self):
		return self._color

	@color.setter
	def color(self, value):
		self._color = value

	@property
	def viva(self):
		return self._viva

	@viva.setter
	def viva(self, value):
		self._viva = value
	def __init__(self, x, y, vx=0, vy=0, radio=1):
		self._x = x
		self._y = y
		self._vx = vx
		self._vy = vy
		self._radio = radio
		self._color = (50,150,255)
		self._viva = True
	def update(self, bloques, caminos, gotas=None):
		if not self._viva:
			return
		self._vy += 0.020  
		if gotas is not None:
			for otra in gotas:
				if otra is not self and otra._viva:
					dx = self._x - otra._x
					dy = self._y - otra._y
					dist = (dx**2 + dy**2) ** 0.5
					if dist < self._radio*2 and dist > 0:
						self._vx += dx * 0.005
						self._vy += dy * 0.005
		nueva_x = self._x + self._vx
		nueva_y = self._y + self._vy
		bloque_colision = None
		for b in bloques:
			if b.collidepoint(nueva_x, nueva_y):
				bloque_colision = b
		if bloque_colision:
			debajo_libre = not any(b.collidepoint(self._x, self._y + 1) for b in bloques)
			if debajo_libre and self._y + 1 < ALTO:
				self._y += 1
				self._vy = 0.5
			else:
				max_lado = 10
				movido_lateral = False
				for d in range(1, max_lado+1):
					nx_izq = self._x - d
					nx_der = self._x + d
					if nx_izq > self._radio and not any(b.collidepoint(nx_izq, self._y + 1) for b in bloques):
						self._x = nx_izq
						self._y += 1
						movido_lateral = True
					if nx_der < ANCHO - self._radio and not any(b.collidepoint(nx_der, self._y + 1) for b in bloques):
						self._x = nx_der
						self._y += 1
						movido_lateral = True
				if not movido_lateral:
					self._viva = False
			self._vy = 0
		else:
			self._x = nueva_x
			self._y = nueva_y
			if hasattr(self, 'pref_lado'):
				del self.pref_lado
		for seg in caminos:
			if seg.collidepoint(self._x, self._y):
				self._vy *= -0.7
				self._y += self._vy
		if self._x < self._radio or self._x > ANCHO-self._radio:
			self._viva = False
		if self._y > ALTO:
			self._viva = False
	def draw(self, surf):
		if self._viva:
			pygame.draw.circle(surf, self._color, (int(self._x), int(self._y)), self._radio)
