import pygame
screen = pygame.display.set_mode((800, 600))

class Coin:
    def __init__(self, x, y, type="reward"):
        self.levelNo = 0
        self.x = x
        self.y = y
        self.radius = 50
        self.type = type

    def collides_with_player(self, player_to_check):
        player_mid_point = player_to_check.current_pos.copy()
        player_mid_point.x += player_to_check.width / 2
        player_mid_point.y += player_to_check.height / 2
        if ((player_mid_point.x - self.x) ** 2 + (
                player_mid_point.y - self.y) ** 2) ** 0.5 < self.radius + player_to_check.width / 2:
            return True
        return False

    def show(self):
        pygame.draw.circle(screen, (255, 150, 0) if self.type == "reward" else (0, 200, 0, 100), (self.x, self.y), self.radius * 2)

