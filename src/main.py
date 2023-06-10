
import game
import menu
import pygame
import sys as system
from bullet import Bullet

pygame.init()
pygame.mixer.init()


class Engine:
    def __init__(self):
        self.init_window()
        self.init_variables()
        self.play_menu_music()

    # Window initialization
    def init_window(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 450
        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.icon_image = pygame.image.load("..\\assets\\icon.png").convert_alpha()
        pygame.display.set_icon(self.icon_image)
        pygame.display.set_caption("From blue to Red")

    # Variable initialization
    def init_variables(self):
        self.state = "Menu"
        self.game = game.Game(self.window)
        self.menu = menu.Menu(self.window)
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.is_muted = False
        self.sounds = {
            "Bullet hit": pygame.mixer.Sound("..\\assets\\sounds\\sound effects\\hit.wav"),
            "Bullet shoot": pygame.mixer.Sound("..\\assets\\sounds\\sound effects\\shoot.wav"),
            "Enemy hit": pygame.mixer.Sound("..\\assets\\sounds\\sound effects\\spark.wav"),
            "Next stage": pygame.mixer.Sound("..\\assets\\sounds\\sound effects\\next_stage.wav"),
            "Lose": pygame.mixer.Sound("..\\assets\\sounds\\sound effects\\lose.wav"),
        }
        self.sounds["Bullet shoot"].set_volume(0.5)

    # Play theme music
    def play_theme(self):
        music_path = "..\\assets\\sounds\\musics\\stage1.mp3"
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)

    # Play menu music
    def play_menu_music(self):
        music_path = "..\\assets\\sounds\\musics\\menu.mp3"
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
        
    # Event polling
    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.save_data()
                pygame.quit()
                system.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                for sound in self.sounds:
                    self.sounds[sound].set_volume(int(self.is_muted))
                    if sound == self.sounds["Bullet shoot"]:
                        self.sounds[sound].set_volume(int(self.is_muted) / 10)
                pygame.mixer.music.set_volume(int(self.is_muted))
                self.is_muted = not self.is_muted

            if self.state == 'Game':
                if self.game.is_game_active:
                    # Updating player on keypress(move)
                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_UP and self.game.player.line_index > 1:
                            self.game.player.line_index -= 1

                        elif event.key == pygame.K_DOWN and self.game.player.line_index < 3:
                            self.game.player.line_index += 1
                        self.game.player.update()

                        # Shoots on key
                        if event.key == pygame.K_z:
                            self.game.bullets.add(Bullet(self.game.player.line_index, self.SCREEN_HEIGHT, self.game.stage))
                            self.sounds["Bullet shoot"].play()

                        # Parry's on key
                        elif event.key == pygame.K_x:
                            # Parrying if it's not on cooldown and there's any bullet
                            if not self.game.is_parry_on_cooldown and len(self.game.bullets.sprites()) != 0:
                                closest_bullet = self.game.bullets.sprites()[0]
                                if closest_bullet.line_index == self.game.player.line_index:
                                    if closest_bullet.rect.left > 665 and closest_bullet.rect.right < self.game.player.rect.left:
                                        self.game.parry_time = pygame.time.get_ticks()
                                        closest_bullet.velocity *= -1
                                        self.game.player.health += 2

                    # Spawn an enemy on timer
                    elif event.type == self.game.spawn_timer:
                        self.game.spawn_enemy()
                # Resetting game on space button press in fail state
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game.reset()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "Menu"
                        self.play_menu_music()
                        self.game.reset()
            elif self.state == "Menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.state = "Game"
                        self.play_theme()
                        self.game.reset()
                    elif event.key == pygame.K_c:
                        self.state = "Controls"
            elif self.state == "Controls" and event.type == pygame.KEYDOWN:
                self.state = "Menu"

    # Updating game
    def update(self):
        # Polls events
        self.poll_events()

        if self.state == 'Game':
            # Updates game scene
            self.game.update(
                self.sounds["Enemy hit"],
                self.sounds["Bullet hit"],
                self.sounds["Next stage"],
                self.sounds["Lose"]
            )

        pygame.display.update()
        self.clock.tick(self.FPS)

    # Rendering all the components
    def render(self):
        if self.state == "Game":
            self.game.render()
        elif self.state == "Menu":
            self.menu.render()
        elif self.state == "Controls":
            self.menu.render_controls()


engine = Engine()
while True:
    engine.update()
    engine.render()