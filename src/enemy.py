
import random
import pygame
from game_data import *

pygame.init()
pygame.mixer.init()


class Invader(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.init_image()
        self.init_variables()

    # Updating enemy
    def update(self, screen_height, stage):
        if not self.is_positioned:
            if self.rect.centery in range(self.line_index * screen_height // 3 - self.image.get_height() // 2 - 30, self.line_index * screen_height // 3 - 30):
                self.y_velocity = 0
                self.is_positioned = True
        else:
            self.x_velocity = random.randint(
                enemy_min_x_velocity[stage],
                enemy_max_x_velocity[stage]
            )

        midright_rect_x, midright_rect_y = self.rect.midright
        self.rect.midright = (
            midright_rect_x + self.x_velocity,
            midright_rect_y + self.y_velocity
        )

    # Image initialization
    def init_image(self):
        # Flips the image
        self.image = pygame.transform.flip(
            pygame.image.load("..\\assets\\sprites\\enemy.png").convert_alpha(),
            True,
            False
        ).convert_alpha()
        # re-Scaling the image
        self.image = pygame.transform.scale(
            self.image,
            (self.image.get_width() + 50, self.image.get_height() + 50)
        )

    # Variables initialization
    def init_variables(self):
        self.x_velocity = 0
        self.y_velocity = random.randint(12, 18)
        self.line_index = random.randint(1, 3)
        self.rect = self.image.get_rect(center=(random.randint(50, 200), 0))
        self.is_positioned = False