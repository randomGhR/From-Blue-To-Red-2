import math
import pygame
from player import Player
from enemy import Invader
from game_data import stage_differences

pygame.init()
pygame.mixer.init()


class Game:
    def __init__(self, window):
        self.init_variables(window)
        self.update_highest_score()
        self.init_backgrounds()
        self.init_and_update_labels()
        self.init_clock()
        self.init_sprite_groups()

    # Variable initialization
    def init_variables(self, window):
        self.player = Player()
        self.score = 0
        self.highest_score = 0
        self.stage = 1
        self.font = pygame.font.Font("..\\assets\\Fonts\\pocod.ttf", 10)
        self.window = window
        self.window.fill(pygame.Color("Black"))
        self.moon_image_index = 1
        self.model_image_index = 1
        self.kill_counter = 0
        self.start_time = pygame.time.get_ticks()

        self.spawn_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_timer, 950)

        self.parry_time = 0
        self.is_parrying = False
        self.is_parry_on_cooldown = False
        self.is_game_active = True
        self.is_muted = False

    # Background initialization
    def init_backgrounds(self):
        self.scroll = 0
        self.background = pygame.image.load("..\\assets\\backgrounds\\bloody way\\background.png").convert_alpha()
        self.background = pygame.transform.flip(self.background, True, False)
        self.tiles = math.ceil((self.window.get_width() / self.background.get_width())) + 1

    # Clock initialization
    def init_clock(self):
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.ticks = pygame.time.get_ticks()

    # Labels initialization and updating
    def init_and_update_labels(self):
        self.highest_score_label = self.font.render(f"Highest score = {self.highest_score}", True, pygame.Color("White")).convert_alpha()
        self.highest_score_rect = self.highest_score_label.get_rect(topleft=(0, 0))

        self.score_label = self.font.render(f"Score = {self.score}", True, pygame.Color("White")).convert_alpha()
        self.score_rect = self.score_label.get_rect(topleft=self.highest_score_rect.bottomleft)

        self.health_label = self.font.render(f"Health = {self.player.health}", True, pygame.Color("White")).convert_alpha()
        self.health_rect = self.score_label.get_rect(topleft=self.score_rect.bottomleft)

        self.stage_label = self.font.render(f"{self.stage} :Stage", True, pygame.Color("White")).convert_alpha()
        self.stage_rect = self.stage_label.get_rect(center=(self.window.get_width() // 2, 20))

    # Updating player highest score
    def update_highest_score(self):
        try:
            data_file = open(file="..\\data\\data.txt", mode='r')
        except FileNotFoundError:
            open(file="..\\data\\data.txt", mode='w').close()
        else:
            data = data_file.readline().replace('\n', '')
            if len(data) != 0:
                self.highest_score = int(data)
            else:
                self.highest_score = 0
            data_file.close()

    # Spawns an enemy
    def spawn_enemy(self):
        self.enemies.add(Invader())

    # Saving the player highest score
    def save_data(self):
        if self.score >= self.highest_score:
            with open(file="..\\data\\data.txt", mode='w') as data_file:
                data_file.write(str(self.score))

    # Resets game attributes
    def reset(self):
        self.save_data()
        self.bullets.empty()
        self.enemies.empty()
        self.stage = 1
        self.score = 0
        self.player.health = 20
        self.kill_counter = 0
        self.start_time = pygame.time.get_ticks()
        self.is_game_active = True
        pygame.mixer.music.play(-1)

    # Sprites group initialization
    def init_sprite_groups(self):
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

    def render_fail_state(self):
        self.window.fill(pygame.Color("Black"))
        self.moon_image_index += 0.1
        if self.moon_image_index > 60:
            self.moon_image_index = 1
        moon_image = pygame.image.load(f"..\\assets\\backgrounds\\moon\\{math.ceil(self.moon_image_index)}.png").convert_alpha()
        moon_image = pygame.transform.scale(moon_image, (
            moon_image.get_width() + 350,
            moon_image.get_height() + 350
        )).convert_alpha()
        moon_rect = moon_image.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))
        self.window.blit(moon_image, moon_rect)
        self.score_label = pygame.font.Font("..\\assets\\fonts\\pocod.ttf", 30).render(
            f"Score: {self.score}",
            True,
            pygame.Color("White")
        ).convert_alpha()
        self.score_rect = self.score_label.get_rect(center=(self.window.get_width() // 2, moon_rect.centery - 140))
        self.window.blit(self.score_label, self.score_rect)
        self.model_image_index += 0.1
        if self.model_image_index > 4:
            self.model_image_index = 1
        model = pygame.image.load(f"..\\assets\\sprites\\model\\{math.ceil(self.model_image_index)}.png").convert_alpha()
        model = pygame.transform.scale(model, (model.get_width() + 100, model.get_height() + 160)).convert_alpha()
        model_rect = model.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))
        self.window.blit(model, model_rect)
        text = pygame.font.Font("..\\assets\\fonts\\pocod.ttf", 15).render("Press 'Space' to restart...", True, pygame.Color("White")).convert_alpha()
        self.window.blit(text, text.get_rect(center=(
            self.window.get_width() // 2,
            model_rect.bottom + 40
        )))

    def update(self, enemy_hit_sound, bullet_hit_sound, next_stage_sound, lose_sound):
        if self.is_game_active:
            # Updating parry cooldown
            self.is_parry_on_cooldown = self.is_parrying and pygame.time.get_ticks() - self.parry_time < 3

            # Detecting collision between bullets and enemies
            self.kill_counter += len(pygame.sprite.groupcollide(self.bullets, self.enemies, False, True))

            # Detecting collision between player and enemies if players is not invincible
            if not self.player.is_invincible:
                if len(pygame.sprite.spritecollide(self.player, self.enemies, True)) != 0:
                    self.player.health -= 2
                    self.player.is_invincible = True
                    enemy_hit_sound.play()

            # Detecting collision between player and bullets if player is not invincible
            if not self.player.is_invincible:
                if len(pygame.sprite.spritecollide(self.player, self.bullets, True)):
                    self.player.health -= 1
                    bullet_hit_sound.play()

            # Updating background scroller after reaching to the end
            if self.scroll > self.background.get_width():
                self.scroll = 0

            # Plays player running animation
            self.player.update_image()

            # Updates all the enemies
            self.enemies.update(self.window.get_height(), self.stage)

            # Updates all the bullets
            self.bullets.update(self.window)

            # initializing and updating labels
            self.init_and_update_labels()

            # Scrolls background
            self.scroll += 0.5

            # Updating highest score if player scores higher than it
            if self.score >= self.highest_score:
                self.highest_score = self.score

            # Updating score based on survival time
            self.score = pygame.time.get_ticks() // 1000 - self.start_time // 1000

            # Applying damage to player if an enemy reaches the end of the screen
            for enemy in self.enemies.sprites():
                if enemy.rect.left >= self.window.get_width():
                    self.player.health -= 1
                    self.enemies.remove(enemy)

            # Updating player invincibility
            if self.player.is_invincible:
                self.player.invincibility_timer += 0.1
                self.player.image.set_alpha(150)
                if math.floor(self.player.invincibility_timer) == 5:
                    self.player.is_invincible = False
                    self.player.invincibility_timer = 0
                    self.player.image.set_alpha(255)

            # Healing player and resetting kill counter after every 10 kill
            if self.kill_counter >= 20:
                self.player.health += 1
                self.kill_counter = 0

            # Limiting player healing ability to max health
            if self.player.health > 20:
                self.player.health = 20

            # Updating stage
            if self.score > stage_differences[self.stage] and self.stage < 5:
                self.stage += 1
                next_stage_sound.play()
                if self.stage == 2:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load("..\\assets\\sounds\\musics\\final stage.mp3")
                    pygame.mixer.music.play(-1)

        # Updating game active value
        if not self.player.health > 0:
            if self.is_game_active:
                lose_sound.play()
            self.is_game_active = False
            pygame.mixer.music.stop()
            self.save_data()

    # Rendering all the components
    def render(self):
        if self.is_game_active:
            # Drawing background
            for i in range(self.tiles):
                self.window.blit(self.background, (-i * self.background.get_width() + self.scroll, 0))

            # Drawing lines
            for row in range(1, 3):
                start_y_pos = row * self.window.get_height() // 3
                pygame.draw.line(self.window, pygame.Color("#0066cc"), (0, start_y_pos), (self.window.get_width(), start_y_pos), 2)

            # Rendering Player
            self.window.blit(self.player.image, self.player.rect)
            # Rendering enemies
            self.enemies.draw(self.window)
            # Rendering bullets
            self.bullets.draw(self.window)
            # Rendering player highest score
            self.window.blit(self.highest_score_label, self.highest_score_rect)
            # Rendering player score
            self.window.blit(self.score_label, self.score_rect)
            # Rendering player health
            self.window.blit(self.health_label, self.health_rect)
            # Rendering stage
            self.window.blit(self.stage_label, self.stage_rect)
        else:
            self.render_fail_state()
