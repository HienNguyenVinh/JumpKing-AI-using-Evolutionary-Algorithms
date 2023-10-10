import pygame

class Coin:
    def __init__(self, x, y, type="reward"):
        self.levelNo = 0
        self.x = x
        self.y = y
        self.radius = 50
        self.type = type

    def collides_with_player(self, player_to_check):
        player_mid_point_x = player_to_check.x + player_to_check.w // 2
        player_mid_point_y = player_to_check.y + player_to_check.h // 2

        if ((player_mid_point_x - self.x) ** 2 + (
                player_mid_point_y - self.y) ** 2) ** 0.5 < self.radius + player_to_check.w // 2:
            return True
        return False

    def Draw(self, window):
        pygame.draw.circle(window, (255, 150, 0) if self.type == "reward" else (0, 200, 0, 100), (self.x, self.y), self.radius * 2)
