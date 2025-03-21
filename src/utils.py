import pygame

# Fonction utilitaire pour vérifier la collision entre deux rectangles
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# Fonction pour dessiner un texte à l'écran
def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Fonction pour redimensionner la fenêtre du jeu en fonction de la taille de l'écran
def resize_window(screen, width, height):
    return pygame.display.set_mode((width, height), pygame.RESIZABLE)

def sleep(sleep_time):
    sleep_time.sleep(sleep_time)