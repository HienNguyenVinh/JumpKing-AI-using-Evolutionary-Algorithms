import time

from subclass import *
import pygame

pygame.init()

clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

class JumpKing:
    # FPS = pygame.time.Clock().tick

    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.levels = MAP_LINES

        self.testing_single_player = True
        self.replaying_best_player = False
        self.clone_of_best_player = None
        self.evolation_speed = 1

        self.player = Player()
        self.player.currentLevelNo = 0

        self.population = Population(POPULATION_SIZE)
        for player in self.population.players:
            player.currentLevelNo = 0


    def UpdatePlayer(self):
        pressedKeys = pygame.key.get_pressed()
        self.player.leftHeld = pressedKeys[pygame.K_LEFT]
        self.player.rightHeld = pressedKeys[pygame.K_RIGHT]
        self.player.jumpHeld = pressedKeys[pygame.K_SPACE]
        self.player.Update(self.testing_single_player)

    def DrawPlayer(self):
        self.window.blit(self.levels[self.player.currentLevelNo].bg, (0, 0))
        self.player.Draw(self.window, self.testing_single_player)

        level_text = font.render(f'Level: {self.player.currentLevelNo + 1}', True, text_color)
        fps_text = font.render(f'FPS: {round(clock.get_fps())}', True, text_color)
        self.window.blit(fps_text, (WIDTH - 160, 10))
        self.window.blit(level_text, (560, 15))
        # for coin in MAP_LINES[self.player.currentLevelNo].coins:
        #     coin.Draw(self.window)


    def UpdatePlayersInPopulation(self):
        if self.population.allPlayerFinished():
            self.population.naturalSelection()
            if self.population.gen % increase_actions_every_X_generations == 0:
                self.population.increase_player_moves(increase_actions_by_amount)

        for i in range(self.evolation_speed):
            self.population.Update()

    def DrawPopulation(self):
        self.population.Draw(self.window)
        # for coin in MAP_LINES[self.population.current_showing_level_no].coins:
        #     coin.Draw(self.window)

    def showPopulationInfo(self):

        fps_text = font.render(f'FPS: {round(clock.get_fps())}', True, text_color)
        gen_text = font.render(f'Gen: {self.population.gen}', True, text_color)
        moves_text = font.render(f'Moves: {len(self.population.players[0].brain.instructions)}', True, text_color)
        height_text = font.render(f'Best Height: {self.population.best_height}', True, text_color)
        evolution_speed_text = font.render(f'Evolution speed: {self.evolation_speed}', True, text_color)

        self.window.blit(fps_text, (WIDTH - 160, 10))
        self.window.blit(gen_text, (30, 10))
        self.window.blit(moves_text, (200, 10))
        self.window.blit(height_text, (400, 10))
        self.window.blit(evolution_speed_text, (650, 10))


    def run(self):
        while (True):
            clock.tick(FPS)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_DOWN:
                        self.evolation_speed = max(1, min(self.evolation_speed - 1, 50))
                        print(self.evolation_speed)
                    if e.key == pygame.K_UP:
                        self.evolation_speed = max(1, min(self.evolation_speed + 1, 50))
                        print(self.evolation_speed)

                    if e.key == pygame.K_TAB:
                        if self.testing_single_player:
                            self.player.resetPlayer()
                            self.testing_single_player = False
                        else:
                            self.population.resetAllPlayers()
                            self.testing_single_player = True

                    if e.key == pygame.K_b:
                        if not self.testing_single_player:
                            self.replaying_best_player = True
                            self.clone_of_best_player = self.population.clone_of_best_player_from_pre_generation
                            self.evolation_speed = 1
                        else:
                            print('No player had trained')

                    if e.key == pygame.K_r:
                        if self.testing_single_player:
                            self.player.resetPlayer()
                        else:
                            self.population.resetAllPlayers()

                    if e.key == pygame.K_n:
                        # self.player.currentLevelNo = 42
                        if self.player.currentLevelNo < 42:
                            self.player.currentLevelNo += 1


                    if e.key == pygame.K_i:
                        print(f"Gen: {self.population.gen}")
                        print(f'Moves: {len(self.population.players[0].brain.instructions)}')
                        print(f"Best height: {self.population.best_height}")
                        print(f"Best level: {self.population.current_best_level_reached}")
            if self.testing_single_player:
                self.UpdatePlayer()
                self.DrawPlayer()
                if self.player.currentLevelNo == 42 and self.player.x >= 920 and self.player.y < 300:
                    self.player.y = 350

            elif self.replaying_best_player:
                if not self.clone_of_best_player.has_finished_actions:
                    for _ in range(self.evolation_speed):
                        self.clone_of_best_player.Update(self.testing_single_player)
                    self.window.blit(self.levels[self.clone_of_best_player.currentLevelNo].bg, (0, 0))
                    self.clone_of_best_player.alreadyShowingSnow = False
                    self.clone_of_best_player.Draw(self.window, self.replaying_best_player)
                else:
                    self.replaying_best_player = False
            else:
                self.UpdatePlayersInPopulation()
                self.DrawPopulation()
                self.showPopulationInfo()

            # for line in self.levels[self.player.currentLevelNo].lines:
            #     line.Draw(self.window)

            pygame.display.update()
            # self.FPS(FPS)


JumpKing().run()
