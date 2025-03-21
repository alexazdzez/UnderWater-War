# game.py

import pygame
from player import Player
import settings
import utils
from enemie import Enemy  # Importation correcte sans boucle
import time


class Game:

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.font = pygame.font.SysFont("Arial", 24)
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.enemy_spawn_time = time.time()  # Temps de départ pour l'apparition des ennemis
        self.enemy_spawn_interval = 2.5  # Intervalle d'apparition des ennemis en secondes

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Gestion du redimensionnement
                if event.type == pygame.VIDEORESIZE:
                    width, height = event.size
                    self.screen = utils.resize_window(self.screen, width, height)

            self.update()
            self.draw()

            # Limiter les FPS
            self.clock.tick(settings.FPS)

    def update(self):
        # Vérifier si c'est le moment d'apparier un nouvel ennemi
        if time.time() - self.enemy_spawn_time >= self.enemy_spawn_interval:
            self.spawn_enemy()  # Appeler la fonction pour faire apparaître un nouvel ennemi
            self.enemy_spawn_time = time.time()  # Réinitialiser le temps de spawn

        # Mettre à jour les éléments du jeu
        self.all_sprites.update()

        # Vérifier les collisions entre l'ennemi et le joueur
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.game_over()

    def draw(self):
        # Dessiner l'écran
        self.screen.blit(settings.BACKGROUND_IMAGE, (0, 0))
        self.screen.blit(pygame.transform.scale(settings.BACKGROUND_IMAGE, (1280, 800)), (0, 0))
        self.all_sprites.draw(self.screen)  # Dessiner tous les sprites

        # Afficher le score ou autre information
        score_text = self.font.render(f"Score: {settings.SCORE}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def spawn_enemy(self):
        """Fonction pour faire apparaître un ennemi."""
        new_enemy = Enemy(self.player)  # Passer le joueur à l'ennemi
        self.enemies.add(new_enemy)  # Ajouter l'ennemi au groupe des ennemis
        self.all_sprites.add(new_enemy)  # Ajouter l'ennemi au groupe des sprites

    def game_over(self):
        print("Game Over!")
        self.running = False  # Arrêter la boucle du jeu
