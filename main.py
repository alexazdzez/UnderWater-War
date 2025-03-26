import pygame
import random
import time
import pickle

# Paramètres du jeu
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
PLAYER_SPEED = 5.5
BOOST_SPEED = 8.5
BOOST_DURATION = 1.5
ENEMY_BASE_SPEED = 2.5
ENEMY_LIFETIME = 7.5
ENEMY_SPAWN_INTERVAL = 2500
FPS = 60
SCORE_FILE = "highscore.pkl"

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Underwater War")
pygame.display.set_icon(pygame.image.load('assets/icon.png'))

# Chargement des images
PLAYER_IMAGE = pygame.image.load('assets/fish.png')
ENEMY_IMAGE = pygame.image.load('assets/shark.png')
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load('assets/bg.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))


def load_highscore():
    try:
        with open(SCORE_FILE, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return 0


def save_highscore(score):
    with open(SCORE_FILE, "wb") as f:
        pickle.dump(score, f)


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 48)
        self.running = True
        self.highscore = load_highscore()

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(BACKGROUND_IMAGE, (0, 0))
            text = self.font.render("Underwater War", True, (255, 255, 255))
            start_text = self.font.render("Appuie sur ESPACE pour jouer", True, (255, 255, 255))
            highscore_text = self.font.render(f"Meilleur score: {self.highscore}", True, (255, 255, 255))
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 200))
            self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 400))
            self.screen.blit(highscore_text, (SCREEN_WIDTH // 2 - highscore_text.get_width() // 2, 600))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return


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
        self.score = 0
        self.highscore = load_highscore()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        if self.score > self.highscore:
            save_highscore(self.score)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.running = False

    def update(self):
        if pygame.time.get_ticks() - self.last_enemy_spawn >= ENEMY_SPAWN_INTERVAL:
            self.spawn_enemy()
            self.last_enemy_spawn = pygame.time.get_ticks()
        self.all_sprites.update()
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.game_over()

    def draw(self):
        self.screen.blit(BACKGROUND_IMAGE, (0, 0))
        self.all_sprites.draw(self.screen)
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.player.draw_boost_bar(screen)
        pygame.display.flip()

    def spawn_enemy(self):
        enemy = Enemy(self.player, self)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def add_score(self, amount):
        self.score += amount

    def game_over(self):
        fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade.fill((0, 0, 0))
        for alpha in range(0, 256, 5):
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)
        self.running = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(PLAYER_IMAGE, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.base_speed = PLAYER_SPEED
        self.speed = self.base_speed
        self.boost_speed = 10  # Vitesse du boost
        self.boost_duration = 2000  # 2 secondes en millisecondes
        self.boost_cooldown = 5000  # 5 secondes de recharge
        self.last_boost_time = -self.boost_cooldown  # Pour pouvoir booster dès le début

        # Définir les dimensions de la barre de recharge
        self.bar_width = 200
        self.bar_height = 20
        self.bar_x = (SCREEN_WIDTH - self.bar_width) // 2
        self.bar_y = SCREEN_HEIGHT - 40  # Juste au-dessus du bas de l'écran

    def draw_boost_bar(self, screen):
        current_time = pygame.time.get_ticks()
        # Calcul de la durée restante du cooldown
        if current_time - self.last_boost_time < self.boost_cooldown:
            cooldown_progress = (current_time - self.last_boost_time) / self.boost_cooldown
        else:
            cooldown_progress = 0

        # Dessiner la barre de recharge (vide ou remplie)
        pygame.draw.rect(screen, (0, 0, 0), (self.bar_x, self.bar_y, self.bar_width, self.bar_height))  # Fond de la barre
        pygame.draw.rect(screen, (0, 255, 0), (self.bar_x, self.bar_y, self.bar_width * (1 - cooldown_progress), self.bar_height))  # Barre remplie

    def update(self):
        keys = pygame.key.get_pressed()

        # Vérifier si le boost est disponible
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and current_time - self.last_boost_time >= self.boost_cooldown:
            self.speed = self.boost_speed
            self.last_boost_time = current_time  # Démarrage du boost

        # Fin du boost après la durée définie
        if current_time - self.last_boost_time >= self.boost_duration:
            self.speed = self.base_speed

        # Mouvements du joueur
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Empêcher le joueur de sortir de l'écran
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, game):
        super().__init__()
        self.image = pygame.transform.scale(ENEMY_IMAGE, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([0, SCREEN_WIDTH])
        self.rect.y = random.choice([0, SCREEN_HEIGHT])
        self.speed = ENEMY_BASE_SPEED + game.score / 12
        self.spawn_time = time.time()
        self.lifetime = ENEMY_LIFETIME + game.score / 12
        self.player = player
        self.game = game

    def update(self):
        # Calcul de la direction par rapport à l'axe x et l'axe y
        direction_x = self.player.rect.x - self.rect.x
        direction_y = self.player.rect.y - self.rect.y

        # Vérification si l'ennemi doit se déplacer vers la droite ou la gauche (en x)
        if direction_x > 0:
            self.rect.x += self.speed  # Déplace l'ennemi vers la droite
        elif direction_x < 0:
            self.rect.x -= self.speed  # Déplace l'ennemi vers la gauche

        # Vérification si l'ennemi doit se déplacer vers le bas ou le haut (en y)
        if direction_y > 0:
            self.rect.y += self.speed  # Déplace l'ennemi vers le bas
        elif direction_y < 0:
            self.rect.y -= self.speed  # Déplace l'ennemi vers le haut
        if time.time() - self.spawn_time >= self.lifetime:
            self.kill()
            self.game.add_score(1)
        if self.rect.colliderect(self.player.rect):
            self.game.game_over()


while True:
    menu = Menu(screen)
    menu.run()
    game = Game(screen)
    game.run()
