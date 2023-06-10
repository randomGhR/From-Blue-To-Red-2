
import pygame

pygame.init()
pygame.mixer.init()


class Menu:
    def __init__(self, window):
        self.init_variables(window)

    def init_variables(self, window):
        self.window = window
        self.background = pygame.image.load("..\\assets\\backgrounds\\bloody way\\menu.png").convert_alpha()
        self.instruction_font = pygame.font.Font("..\\assets\\fonts\\pocod.ttf", 10)
        self.keyboard_font = pygame.font.Font("..\\assets\\fonts\\pocod.ttf", 19)
        self.font = pygame.font.Font("..\\assets\\fonts\\pocod.ttf", 30)
        self.from_label = self.font.render("From", True, pygame.Color("#FFFFFF")).convert_alpha()
        self.blue_label = self.font.render("Blue", True, pygame.Color("#185ADB")).convert_alpha()
        self.to_label = self.font.render("to", True, pygame.Color("#FFFFFF")).convert_alpha()
        self.red_label = self.font.render("Red", True, pygame.Color("#FF1E00")).convert_alpha()
        self.text = pygame.font.Font("..\\assets\\fonts\\pocod.ttf", 15).render(
            "Press 'Space' to start...",
            True,
            pygame.Color("#FFFFFF")
        ).convert_alpha()
        self.text_rect = self.text.get_rect(center=(
            self.window.get_width() // 2,
            self.window.get_height() // 2
        ))
        self.mute_text = self.instruction_font.render(
            "Press 'M' to mute",
            True,
            pygame.Color("#FFFFFF")
        ).convert_alpha()
        self.mute_rect = self.mute_text.get_rect(topright=(
            self.window.get_width(),
            0
        ))
        self.control_text = self.instruction_font.render("Press 'C' to see controls", True, pygame.Color("#FFFFFF"))
        self.control_rect = self.control_text.get_rect(bottomleft=(0, self.window.get_height()))

    def render(self):
        self.window.fill(pygame.Color("#000000"))
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.from_label, (120, 100))
        self.window.blit(self.blue_label, (290, 100))
        self.window.blit(self.to_label, (450, 100))
        self.window.blit(self.red_label, (550, 100))
        self.window.blit(self.text, self.text_rect)
        self.window.blit(self.mute_text, self.mute_rect)
        self.window.blit(self.control_text, self.control_rect)

    def render_controls(self):
        self.window.fill(pygame.Color("#000000"))

        self.up_image = pygame.image.load("..\\assets\\sprites\\keyboard\\ARROWUP.png").convert_alpha()
        self.up_image = pygame.transform.scale(self.up_image, (self.up_image.get_width() + 50, self.up_image.get_height() + 50)).convert_alpha()
        self.up_rect = self.up_image.get_rect(topleft=(0, 40))
        self.up_label = self.keyboard_font.render("Move up", True, pygame.Color("#FFFFFF")).convert_alpha()
        self.up_label_rect = self.up_label.get_rect(midleft=(self.up_rect.right + 15, self.up_rect.centery))
        self.window.blit(self.up_image, self.up_rect)
        self.window.blit(self.up_label, self.up_label_rect)

        self.down_image = pygame.image.load("..\\assets\\sprites\\keyboard\\ARROWDOWN.png").convert_alpha()
        self.down_image = pygame.transform.scale(self.down_image, (self.down_image.get_width() + 50, self.down_image.get_height() + 50)).convert_alpha()
        self.down_rect = self.down_image.get_rect(topleft=self.up_rect.bottomleft)
        self.down_label = self.keyboard_font.render("Move down", True, pygame.Color("#FFFFFF")).convert_alpha()
        self.down_label_rect = self.down_label.get_rect(midleft=(self.down_rect.right + 15, self.down_rect.centery))
        self.window.blit(self.down_image, self.down_rect)
        self.window.blit(self.down_label, self.down_label_rect)

        self.z_image = pygame.image.load("..\\assets\\sprites\\keyboard\\Z.png").convert_alpha()
        self.z_image = pygame.transform.scale(self.z_image, (self.z_image.get_width() + 50, self.z_image.get_height() + 50)).convert_alpha()
        self.z_rect = self.z_image.get_rect(topleft=self.down_rect.bottomleft)
        self.z_label = self.keyboard_font.render("Shoot", True, pygame.Color("#FFFFFF")).convert_alpha()
        self.z_label_rect = self.z_label.get_rect(midleft=(self.z_rect.right + 15, self.z_rect.centery))
        self.window.blit(self.z_image, self.z_rect)
        self.window.blit(self.z_label, self.z_label_rect)

        self.x_image = pygame.image.load("..\\assets\\sprites\\keyboard\\X.png").convert_alpha()
        self.x_image = pygame.transform.scale(self.x_image, (self.x_image.get_width() + 50, self.x_image.get_height() + 50)).convert_alpha()
        self.x_rect = self.z_image.get_rect(topleft=self.z_rect.bottomleft)
        self.x_label1 = self.keyboard_font.render("Parry bullet to get healed", True, pygame.Color("#FFFFFF")).convert_alpha()
        self.x_label1_rect = self.x_label1.get_rect(midleft=(self.x_rect.right + 15, self.x_rect.top + 15))
        self.x_label2 = self.keyboard_font.render("and change the bullet direction", True, pygame.Color("#FFFFFF")).convert_alpha()
        self.x_label2_rect = self.x_label1.get_rect(midleft=(self.x_label1_rect.left, self.x_label1_rect.bottom + 20))
        self.window.blit(self.x_image, self.x_rect)
        self.window.blit(self.x_label1, self.x_label1_rect)
        self.window.blit(self.x_label2, self.x_label2_rect)

        self.m_image = pygame.image.load("..\\assets\\sprites\\keyboard\\M.png").convert_alpha()
        self.m_image = pygame.transform.scale(self.m_image, (self.m_image.get_width() + 50, self.m_image.get_height() + 50)).convert_alpha()
        self.m_rect = self.z_image.get_rect(topleft=self.x_rect.bottomleft)
        self.m_label = self.keyboard_font.render("Mute", True, pygame.Color("#FFFFFF")).convert_alpha()
        self.m_label_rect = self.m_label.get_rect(midleft=(self.m_rect.right + 15, self.m_rect.centery))
        self.window.blit(self.m_image, self.m_rect)
        self.window.blit(self.m_label, self.m_label_rect)