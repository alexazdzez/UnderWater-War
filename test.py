import pygame
import random
import time

# Paramètres du jeu
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
PLAYER_SPEED = 5
PLAYER_IMAGE = pygame.image.load('assets/fish.png')
ENEMY_IMAGE = pygame.image.load('assets/shark.png')
BACKGROUND_IMAGE = pygame.image.load('assets/bg.png')
FPS = 60  # Nombre de frames par seconde
SCORE = 0
BEST_SCORE = 0
running = True


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
        self.last_enemy_spawn = pygame.time.get_ticks()
        self.enemy_spawn_interval = 2500
        self.score = 0
        self.best_score = 0

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn >= self.enemy_spawn_interval:
            self.spawn_enemy()
            self.last_enemy_spawn = current_time

        self.all_sprites.update()
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.game_over()

    def draw(self):
        background = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(background, (0, 0))
        self.all_sprites.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()

    def spawn_enemy(self):
        new_enemy = Enemy(self.player, self)
        self.enemies.add(new_enemy)
        self.all_sprites.add(new_enemy)

    def add_score(self, amount):
        self.score += amount
        print(f"Score: {self.score}")

    def game_over(self):
        print(f"Game Over! Score final : {self.score}")
        self.running = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(PLAYER_IMAGE, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = PLAYER_SPEED

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Limite aux bords de l'écran
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, game):
        super().__init__()
        self.image = pygame.transform.scale(ENEMY_IMAGE, (50, 50))
        self.rect = self.image.get_rect()
        self.speed = max(1.5, game.score / 6 + random.randint(0, 1))
        self.spawn_time = time.time()
        self.lifetime = max(7, game.score / 6 + 7)
        self.player = player
        self.game = game
        self.game_over_triggered = False

    def update(self):
        if self.player.rect.x > self.rect.x:
            self.rect.x += self.speed
        elif self.player.rect.x < self.rect.x:
            self.rect.x -= self.speed
        if self.player.rect.y > self.rect.y:
            self.rect.y += self.speed
        elif self.player.rect.y < self.rect.y:
            self.rect.y -= self.speed

        if time.time() - self.spawn_time >= self.lifetime:
            self.kill()
            self.game.add_score(1)

        if self.rect.colliderect(self.player.rect) and not self.game_over_triggered:
            self.game.game_over()
            self.game_over_triggered = True


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Underwater War")
    pygame.display.set_icon(pygame.image.load('assets/icon.png'))
    game = Game(screen)
    game.run()
    pygame.quit()
