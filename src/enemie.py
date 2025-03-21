# enemy.py
import random
import time
import pygame

import settings

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):  # Passer le joueur comme paramètre
        super().__init__()
        self.image = pygame.transform.scale(settings.ENEMIE_IMAGE, (50, 50))
        self.rect = self.image.get_rect()
        self.speed = settings.SCORE / 6 + 1.5 + random.randint(0, 1)
        print(self.speed)
        self.spawn_time = time.time()  # Enregistrer l'heure de spawn de l'ennemi
        self.lifetime = 7  # Durée pendant laquelle l'ennemi reste visible (7 secondes)
        self.player = player  # Garder une référence au joueur
        self.game_over_triggered = False  # Empêcher plusieurs appels de game_over

    def update(self):
        # Déplacer l'ennemi vers le joueur
        if self.player.rect.x > self.rect.x:
            self.rect.x += self.speed
        elif self.player.rect.x < self.rect.x:
            self.rect.x -= self.speed
        if self.player.rect.y > self.rect.y:
            self.rect.y += self.speed
        elif self.player.rect.y < self.rect.y:
            self.rect.y -= self.speed

        elapsed_time = time.time() - self.spawn_time

        # Vérifier si l'ennemi a dépassé son temps de vie
        if elapsed_time >= self.lifetime:
            self.kill()  # Supprimer l'ennemi après 7 secondes
            settings.SCORE += 1  # Incrémenter le score

        # Vérifier si l'ennemi entre en collision avec le joueur
        if self.rect.colliderect(self.player.rect) and not self.game_over_triggered:
            self.game_over()
            self.game_over_triggered = True  # Empêcher plusieurs appels de game_over

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Dessiner l'image de l'ennemi sur l'écran

    def game_over(self):
        print("Game Over!")
        print(settings.SCORE)
        # Tu peux ici ajouter la logique pour finir la partie ou réinitialiser le jeu
