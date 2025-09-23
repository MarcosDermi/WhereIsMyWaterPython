import pygame
import sys

pygame.init()

# --- Constantes para formato "app" ---
ANCHO, ALTO = 480, 800   # Pantalla vertical tipo smartphone
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (50, 150, 255)
GRIS = (200, 200, 200)

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Misión Hidratación")
fuente = pygame.font.SysFont("Consolas", 28)

# Estados
MENU, JUGAR, INSTRUCCIONES = "menu", "jugar", "instrucciones"
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
    titulo = fuente.render("💧 Misión Hidratación 💧", True, NEGRO)
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
    texto1 = fuente.render("Objetivo:", True, NEGRO)
    texto2 = fuente.render("Escribe cuántos litros tomar", True, NEGRO)
    texto3 = fuente.render("y dibuja un camino para llenar la botella.", True, NEGRO)
    texto4 = fuente.render("Presiona ESC para volver.", True, NEGRO)

    pantalla.blit(texto1, (30, 100))
    pantalla.blit(texto2, (30, 160))
    pantalla.blit(texto3, (30, 200))
    pantalla.blit(texto4, (30, 600))

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

# --- Bucle principal ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if estado == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    estado = JUGAR
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
    elif estado == JUGAR:
        dibujar_juego()

    pygame.display.flip()
