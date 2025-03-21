import pygame
from game import Game
import settings

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre du jeu avec les dimensions définies dans settings.py
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Underwater War")
pygame.display.set_icon(pygame.image.load('assets/icon.png'))

# Lancer le jeu
game = Game(screen)
game.run()
