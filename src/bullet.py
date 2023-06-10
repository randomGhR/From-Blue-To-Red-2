
import pygame
from game_data import bullet_velocity

pygame.init()
pygame.mixer.init()


class Bullet(pygame.sprite.Sprite):

    
    def __init__(self, line_index, screen_height, stage):
        super().__init__()
        self.init_image()
        self.line_index = line_index
        self.rect = self.image.get_rect(topright=(
            0,
            (self.line_index + self.line_index - 1) * screen_height // 6
        ))
        self.velocity = bullet_velocity[stage]

    # Updating bullet attributes
    def update(self, screen):
        self.rect.right += self.velocity
        if self.rect.left >= 800 or self.rect.right <= 0:
            self.kill()

        if self.rect.right >= 665:
            pygame.draw.rect(screen, pygame.Color("#FFFF00"), self.rect, 10)

    # Image initialization
    def init_image(self):
        self.image = pygame.image.load("..\\assets\\sprites\\bullet.png").convert_alpha()
        # Re-scaling the image
        self.image = pygame.transform.scale(
            self.image,
            (18, 9)
        ).convert_alpha()