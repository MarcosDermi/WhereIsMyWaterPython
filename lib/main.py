import pygame
import sys
import os

pygame.init()

# --- Constantes para formato "app" ---
ANCHO, ALTO = 480, 800   # Pantalla vertical tipo smartphone
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (50, 150, 255)
GRIS = (200, 200, 200)


pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Aqua survivor")
fuente = pygame.font.SysFont("Consolas", 28)

# --- Cargar textura de tierra para los bloques ---
import urllib.request
TEX_PATH = "tierra_block.jpg"
if not os.path.exists(TEX_PATH):
    url = "https://img.freepik.com/foto-gratis/vista-superior-tierra_23-2148175893.jpg"
    urllib.request.urlretrieve(url, TEX_PATH)
block_texture = pygame.image.load(TEX_PATH)
block_texture = pygame.transform.scale(block_texture, (40, 28))  # tamaño base, se ajusta luego





MENU, JUGAR, INSTRUCCIONES  = "menu", "miniwh2", "instrucciones"
estado = MENU

# Variables de juego
respuesta = ""
mensaje = ""
camino = []

# Posiciones clave
grifo_pos = (ANCHO//2, 120)  # Grifo arriba al centro
botella_rect = pygame.Rect(ANCHO//2 - 40, ALTO - 180, 80, 150)  # Botella abajo

def dibujar_fondo_rejilla():
    pantalla.fill(BLANCO)
    for x in range(0, ANCHO, 20):
        pygame.draw.line(pantalla, GRIS, (x, 0), (x, ALTO))
    for y in range(0, ALTO, 20):
        pygame.draw.line(pantalla, GRIS, (0, y), (ANCHO, y))

def dibujar_menu():
    dibujar_fondo_rejilla()
    titulo = fuente.render("💧 Aqua survivor 💧", True, NEGRO)
    opciones = [
        fuente.render("1. Jugar", True, NEGRO),
        fuente.render("2. Instrucciones", True, NEGRO),
        fuente.render("3. Salir", True, NEGRO)
    ]
    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 150))
    for i, opcion in enumerate(opciones):
        pantalla.blit(opcion, (ANCHO//2 - opcion.get_width()//2, 250 + i*60))

def dibujar_instrucciones():
    dibujar_fondo_rejilla()
    instrucciones = [
        "INSTRUCCIONES DEL MINIJUEGO:",
        "",
        "- El objetivo es llenar el balde con gotas ",
        "  de agua.",
        "- Haz clic en '¡Comenzar!' para iniciar ",
        "  el flujo de agua.",
        "- Puedes eliminar bloques de tierra haciendo ",
        "  clic sobre ellos.",
        "- Dibuja caminos para guiar el agua haciendo",
        "  clicks con el mouse.",
        "- El agua caerá desde la canilla y seguirá ",
        "  el camino que dibujes.",
        "- Cuando el balde se llene con la cantidad ",
        "  objetivo, ganas.",
        "- Presiona ESC para volver al menú principal",
        "  en cualquier momento.",
        "",
        "¡Diviértete sobre el recorrido del agua!"
    ]
    fuente_inst = pygame.font.SysFont("Consolas", 17)
    for i, linea in enumerate(instrucciones):
        texto = fuente_inst.render(linea, True, (0,0,0))
        pantalla.blit(texto, (30, 80 + i*32))

def dibujar_botella():
    # Botella
    pygame.draw.rect(pantalla, BLANCO, botella_rect, 0)
    pygame.draw.rect(pantalla, NEGRO, botella_rect, 3)
    # Cara de la botella
    ojo1 = (botella_rect.centerx - 15, botella_rect.top + 40)
    ojo2 = (botella_rect.centerx + 15, botella_rect.top + 40)
    pygame.draw.circle(pantalla, NEGRO, ojo1, 6)
    pygame.draw.circle(pantalla, NEGRO, ojo2, 6)
    boca_rect = pygame.Rect(botella_rect.centerx - 20, botella_rect.top + 80, 40, 20)
    pygame.draw.arc(pantalla, NEGRO, boca_rect, 3.14, 0, 3)

    if mensaje == "Correcto":
        pygame.draw.rect(pantalla, AZUL, (botella_rect.left, botella_rect.bottom - 60, 80, 60))

def dibujar_grifo():
    # Un grifo simple arriba al centro
    pygame.draw.rect(pantalla, NEGRO, (grifo_pos[0]-20, grifo_pos[1]-20, 40, 20))
    pygame.draw.rect(pantalla, NEGRO, (grifo_pos[0]-5, grifo_pos[1]-20, 10, 40))
    pygame.draw.circle(pantalla, NEGRO, (grifo_pos[0], grifo_pos[1]+20), 10)

def dibujar_juego():
    dibujar_fondo_rejilla()

    # Dibujar grifo y botella
    dibujar_grifo()
    dibujar_botella()

    # Camino dibujado
    if len(camino) > 1:
        pygame.draw.lines(pantalla, AZUL, False, camino, 5)

    # Pregunta
    pregunta = fuente.render("¿Cuántos litros de agua por día?", True, NEGRO)
    pantalla.blit(pregunta, (30, 40))

    # Respuesta escrita
    texto_resp = fuente.render(respuesta, True, NEGRO)
    pantalla.blit(texto_resp, (30, 80))

    # Mensaje de validación
    if mensaje:
        msj = fuente.render(mensaje, True, NEGRO)
        pantalla.blit(msj, (30, 120))

# --- Clases y lógica del minijuego tipo Where is My Water 2 ---
import random

class Botella:
    def __init__(self, x, y, ancho=60, alto=80):
        self.rect = pygame.Rect(x-ancho//2, y-alto, ancho, alto)
        self.gotas_recibidas = 0
    def draw(self, surf):
        # Dibuja un balde (cubo) con borde y manija
        # Cuerpo del balde
        cubo_rect = self.rect.inflate(-10, 0)
        pygame.draw.rect(surf, (200, 200, 220), cubo_rect)
        pygame.draw.rect(surf, (80, 80, 100), cubo_rect, 4)
        # Borde superior (más grueso)
        pygame.draw.rect(surf, (120, 120, 140), (cubo_rect.left, cubo_rect.top, cubo_rect.width, 12))
        # Manija (arco)
        cx = cubo_rect.centerx
        top = cubo_rect.top
        r = cubo_rect.width // 2
        pygame.draw.arc(surf, (80, 80, 100), (cx - r, top - r//2, 2*r, r), 3.14, 0, 4)
    def recibe_gota(self):
        self.gotas_recibidas += 1

class Gota:
    def __init__(self, x, y, vx=0, vy=0, radio=1):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radio = radio
        self.color = (50,150,255)
        self.viva = True
    def update(self, bloques, caminos, gotas=None):
        if not self.viva:
            return
        self.vy += 0.045  # gravedad aumentada para que bajen 50% más rápido
        # Repulsión simple entre gotas cercanas (simula presión de agua)
        if gotas is not None:
            for otra in gotas:
                if otra is not self and otra.viva:
                    dx = self.x - otra.x
                    dy = self.y - otra.y
                    dist = (dx**2 + dy**2)**0.5
                    if dist < self.radio*2 and dist > 0:
                        self.vx += dx * 0.01
                        self.vy += dy * 0.01
        nueva_x = self.x + self.vx
        nueva_y = self.y + self.vy
        bloque_colision = None
        for b in bloques:
            if b.collidepoint(nueva_x, nueva_y):
                bloque_colision = b
                break
        if bloque_colision:
            # Si no puede bajar, buscar moverse lateralmente aunque no haya espacio diagonal
            saltos = [4, 8, 12]
            movido = False
            # Primero intentar bajar en diagonal
            for salto in saltos:
                puede_diag_izq = not any(b.collidepoint(self.x - self.radio - salto, self.y + salto) for b in bloques) and self.x - self.radio - salto > 0 and self.y + salto < ALTO 
                puede_diag_der = not any(b.collidepoint(self.x + self.radio + salto, self.y + salto) for b in bloques) and self.x + self.radio + salto < ANCHO and self.y + salto < ALTO 
                if puede_diag_izq:
                    self.x -= salto
                    self.y += salto
                    movido = True
                    break
                elif puede_diag_der:
                    self.x += salto
                    self.y += salto
                    Movido = True
                    break
            # Si no pudo bajar en diagonal, intentar solo lateral
            if not movido:
                for salto in saltos:
                    puede_izq = not any(b.collidepoint(self.x - self.radio - salto, self.y) for b in bloques) and self.x - self.radio - salto > 0
                    puede_der = not any(b.collidepoint(self.x + self.radio + salto, self.y) for b in bloques) and self.x + self.radio + salto < ANCHO
                    if puede_izq and not puede_der:
                        self.x -= salto
                        break
                    elif puede_der and not puede_izq:
                        self.x += salto
                        break
                    elif puede_izq and puede_der:
                        # Si ambas direcciones están libres, alternar para desbloquear
                        if not hasattr(self, 'pref_lado'):
                            self.pref_lado = 'izq'
                        if self.pref_lado == 'izq':
                            self.x -= salto
                            self.pref_lado = 'der'
                        else:
                            self.x += salto
                            self.pref_lado = 'izq'
                        break
            # Si no pudo moverse, buscar huecos más lejos a izquierda o derecha, y seguir moviéndose hasta poder bajar
            if not movido:
                rango = 50  # hasta 50 pixeles a cada lado
                encontrado = False
                for offset in range(1, rango+1):
                    # Buscar hueco a la izquierda
                    nx = self.x - offset
                    ny = self.y + 1
                    if nx > self.radio and not any(b.collidepoint(nx, ny) for b in bloques):
                        # Verificar que debajo de ese hueco también esté libre para bajar
                        while ny < ALTO and not any(b.collidepoint(nx, ny) for b in bloques):
                            self.x = nx
                            self.y = ny
                            ny += 1
                        encontrado = True
                        break
                    # Buscar hueco a la derecha
                    nx = self.x + offset
                    ny = self.y + 1
                    if nx < ANCHO - self.radio and not any(b.collidepoint(nx, ny) for b in bloques):
                        while ny < ALTO and not any(b.collidepoint(nx, ny) for b in bloques):
                            self.x = nx
                            self.y = ny
                            ny += 1
                        encontrado = True
                        break
                # Si sigue sin encontrar hueco, pero debajo suyo está libre, forzar que baje
                if not encontrado:
                    debajo_libre = not any(b.collidepoint(self.x, self.y + 1) for b in bloques)
                    if debajo_libre and self.y + 1 < ALTO:
                        self.y += 1
                    else:
                        # Buscar lateralmente el hueco más cercano para bajar (despegar de paredes)
                        max_lado = 20  # hasta 20 píxeles a cada lado
                        movido_lateral = False
                        centro = ANCHO // 2
                        for d in range(1, max_lado+1):
                            # Si está más cerca del borde derecho, priorizar izquierda
                            if self.x > centro:
                                # Buscar a la izquierda primero
                                nx = self.x - d
                                if nx > self.radio and not any(b.collidepoint(nx, self.y + 1) for b in bloques):
                                    self.x = nx
                                    self.y += 1
                                    movido_lateral = True
                                    break
                                # Luego derecha
                                nx = self.x + d
                                if nx < ANCHO - self.radio and not any(b.collidepoint(nx, self.y + 1) for b in bloques):
                                    self.x = nx
                                    self.y += 1
                                    movido_lateral = True
                                    break
                            else:
                                # Si está más cerca del borde izquierdo, priorizar derecha
                                nx = self.x + d
                                if nx < ANCHO - self.radio and not any(b.collidepoint(nx, self.y + 1) for b in bloques):
                                    self.x = nx
                                    self.y += 1
                                    movido_lateral = True
                                    break
                                # Luego izquierda
                                nx = self.x - d
                                if nx > self.radio and not any(b.collidepoint(nx, self.y + 1) for b in bloques):
                                    self.x = nx
                                    self.y += 1
                                    movido_lateral = True
                                    break
                        if not movido_lateral:
                            self.viva = False  # atrapada
            self.vy = 0
        else:
            self.x = nueva_x
            self.y = nueva_y
            if hasattr(self, 'pref_lado'):
                del self.pref_lado
        # Rebote con caminos (líneas dibujadas)
        for seg in caminos:
            if seg.collidepoint(self.x, self.y):
                self.vy *= -0.7
                self.y += self.vy
        # Limites pantalla
        if self.x < self.radio or self.x > ANCHO-self.radio:
            self.viva = False
        if self.y > ALTO:
            self.viva = False
    def draw(self, surf):
        if self.viva:
            pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radio)

class MiniWhereIsMyWater:
    LEVELS = [
        {"meta": 30, "max_gotas": 100},
        {"meta": 60, "max_gotas": 200},
        {"meta": 100, "max_gotas": 300},
    ]
    def __init__(self, pantalla, nivel=0):
        self.pantalla = pantalla
        self.nivel = nivel
        # Filas de bloques de tierra según el nivel
        filas_por_nivel = [3, 6, 9]
        filas = filas_por_nivel[self.nivel] if self.nivel < len(filas_por_nivel) else 3
        bloques_por_fila = 12
        bloque_ancho = ANCHO // bloques_por_fila
        self.botella = Botella(ANCHO//2, ALTO-80, ancho=2*bloque_ancho, alto=80)
        self.gotas = []
        self.caminos = []  # lista de rects
        self.dibujando = False
        self.linea_actual = []
        # Crear una estructura de bloques de tierra (filas según nivel)
        self.bloques = []
        bloque_alto = 28
        y_inicio = 180
        for fila in range(filas):
            for col in range(bloques_por_fila):
                self.bloques.append(pygame.Rect(col * bloque_ancho, y_inicio + fila * bloque_alto, bloque_ancho, bloque_alto))
        self.ticks = 0
        self.meta = self.LEVELS[self.nivel]["meta"]
        self.max_gotas = self.LEVELS[self.nivel]["max_gotas"]
        self.gotas_generadas = 0
        self.victoria = False
        self.comenzado = False
        self.boton_rect = pygame.Rect(ANCHO//2 - 80, 120, 160, 50)
        self.final_victoria = False
    def run(self, events):
        if self.final_victoria:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"
            self.pantalla.fill((255,255,255))
            fuente_chica = pygame.font.SysFont("Consolas", 16)
            msj = fuente_chica.render("¡Felicidades! Completaste todos los niveles", True, (0,100,0))
            rect = msj.get_rect(center=(ANCHO//2, ALTO//2))
            self.pantalla.blit(msj, rect)
            msj2 = fuente_chica.render("Presiona ESC para volver al menú", True, (0,100,0))
            rect2 = msj2.get_rect(center=(ANCHO//2, ALTO//2+60))
            self.pantalla.blit(msj2, rect2)
            return None
        if self.comenzado:
            self.ticks += 1
            if self.botella.gotas_recibidas < self.meta:
                if self.ticks % 3 == 0 and not self.victoria and self.gotas_generadas < self.max_gotas:
                    for i in range(5):
                        offset = random.uniform(-5, 5)
                        vx = random.uniform(-0.15, 0.15)
                        self.gotas.append(Gota(ANCHO//2 + offset, 60, vx=vx, vy=0, radio=2))
                    self.gotas_generadas += 1
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
            if not self.comenzado:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.boton_rect.collidepoint(event.pos):
                        self.comenzado = True
                    else:
                        for b in self.bloques[:]:
                            if b.collidepoint(event.pos):
                                self.bloques.remove(b)
                                break
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for b in self.bloques[:]:
                        if b.collidepoint(event.pos):
                            self.bloques.remove(b)
                            break
                    else:
                        self.dibujando = True
                        self.linea_actual = [event.pos]
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.dibujando = False
                    if len(self.linea_actual) > 1:
                        for i in range(len(self.linea_actual)-1):
                            seg = pygame.draw.line(self.pantalla, (100,100,100), self.linea_actual[i], self.linea_actual[i+1], 10)
                            self.caminos.append(seg)
                    self.linea_actual = []
                if event.type == pygame.MOUSEMOTION and self.dibujando:
                    self.linea_actual.append(event.pos)
        for gota in self.gotas:
            gota.update(self.bloques, self.caminos, self.gotas)
            if gota.viva and self.botella.rect.collidepoint(gota.x, gota.y):
                gota.viva = False
                self.botella.recibe_gota()
        self.pantalla.fill((180,140,90))
        for b in self.bloques:
            tex = pygame.transform.scale(block_texture, (b.width, b.height))
            self.pantalla.blit(tex, b)
        for seg in self.caminos:
            pygame.draw.rect(self.pantalla, (100,100,100), seg)
        self.botella.draw(self.pantalla)
        for gota in self.gotas:
            gota.draw(self.pantalla)
        fuente_chica = pygame.font.SysFont("Consolas", 15)
        texto = fuente_chica.render(f"Nivel {self.nivel+1} - Gotas en botella: {self.botella.gotas_recibidas}ml/{self.meta}ml", True, (0,0,0))
        self.pantalla.blit(texto, (20, 20))
        if not self.comenzado:
            pygame.draw.rect(self.pantalla, (0, 180, 80), self.boton_rect, border_radius=12)
            txt = fuente.render("¡Comenzar!", True, (255,255,255))
            self.pantalla.blit(txt, (self.boton_rect.centerx - txt.get_width()//2, self.boton_rect.centery - txt.get_height()//2))
        if self.botella.gotas_recibidas >= self.meta:
            self.victoria = True
            if self.nivel < 2:
                fuente_chica = pygame.font.SysFont("Consolas", 15)
                msj = fuente_chica.render("¡Victoria! Presiona ESPACIO para siguiente nivel", True, (0,100,0))
                rect = msj.get_rect(center=(ANCHO//2, ALTO//2))
                pygame.draw.rect(self.pantalla, (255,255,255), rect.inflate(40, 30))
                pygame.draw.rect(self.pantalla, (0,100,0), rect.inflate(40, 30), 4)
                self.pantalla.blit(msj, rect)
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        return "next"
            else:
                self.final_victoria = True
        return False

# --- Bucle principal ---
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if estado == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    estado = "miniwh2"
                    minijuego = MiniWhereIsMyWater(pantalla)
                elif event.key == pygame.K_2:
                    estado = INSTRUCCIONES
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

        elif estado == INSTRUCCIONES:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                estado = MENU

        elif estado == JUGAR:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        valor = float(respuesta)
                        if 2 <= valor <= 3:  # rango correcto de litros recomendados
                            mensaje = "Correcto"
                        else:
                            mensaje = "Incorrecto"
                    except:
                        mensaje = "Escribe un número"
                elif event.key == pygame.K_BACKSPACE:
                    respuesta = respuesta[:-1]
                else:
                    if event.unicode.isdigit() or event.unicode == ".":
                        respuesta += event.unicode

            # Dibujar camino con mouse
            if pygame.mouse.get_pressed()[0]:
                camino.append(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                estado = MENU
                respuesta = ""
                mensaje = ""
                camino = []


    # Render según estado
    if estado == MENU:
        dibujar_menu()
    elif estado == INSTRUCCIONES:
        dibujar_instrucciones()
    elif estado == "miniwh2":
        resultado = minijuego.run(events)
        if resultado == True:
            estado = MENU
        elif resultado == "next":
            if minijuego.nivel < 2:
                minijuego = MiniWhereIsMyWater(pantalla, nivel=minijuego.nivel+1)
            else:
                minijuego.final_victoria = True
        elif resultado == "menu":
            estado = MENU

    pygame.display.flip()

