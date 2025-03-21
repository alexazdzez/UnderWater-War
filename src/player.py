import pygame
import settings

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(settings.PLAYER_IMAGE, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)  # Position initiale du joueur
        self.speed = settings.PLAYER_SPEED

    def update(self):
        # Déplacer le joueur avec les touches fléchées
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Limiter les déplacements du joueur aux bords de la fenêtre
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > settings.SCREEN_WIDTH:
            self.rect.right = settings.SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > settings.SCREEN_HEIGHT:
            self.rect.bottom = settings.SCREEN_HEIGHT

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Dessiner l'image du joueur sur l'écran
