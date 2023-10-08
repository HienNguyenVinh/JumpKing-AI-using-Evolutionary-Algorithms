from subclass import *
import pygame
import os

pygame.init()


class JumpKing:
    FPS = pygame.time.Clock().tick

    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.levels = MAP_LINES

        self.testing_single_player = False
        self.replaying_best_player = False
        self.clone_of_best_player = None
        self.evolation_speed = 1

        self.player = Player()
        self.player.currentLevelNo = 0

        self.population = Population(50)
        for player in self.population.players:
            player.currentLevelNo = 0


    def UpdatePlayer(self):
        pressedKeys = pygame.key.get_pressed()
        self.player.leftHeld = pressedKeys[pygame.K_LEFT]
        self.player.rightHeld = pressedKeys[pygame.K_RIGHT]
        self.player.jumpHeld = pressedKeys[pygame.K_SPACE]
        self.player.Update()
        self.player.Draw(self.window)

    def UpdatePlayersInPopulation(self):
        if self.population.allPlayerFinished():
            self.population.naturalSelection()
            if self.population.gen % increase_actions_every_X_generations == 0:
                self.population.increase_player_moves(increase_actions_by_amount)

        for i in range(evolation_speed):
            self.population.Update()

    def DrawPlayer(self):
        self.window.blit(self.levels[self.player.currentLevelNo].bg, (0, 0))
        self.UpdatePlayer()

    def DrawPopulation(self):
        self.window.blit(self.levels[self.population.current_highest_level_no].bg, (0, 0))
        self.population.Draw(self.window)

    def run(self):
        while (True):
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

                    if e.type == pygame.K_b:
                        self.replaying_best_player = True
                        self.clone_of_best_player = self.population.clone_of_best_player_from_pre_generation
                        self.evolation_speed = 1


            if self.testing_single_player:
                self.UpdatePlayer()
                self.DrawPlayer()
            elif self.replaying_best_player:
                if not self.clone_of_best_player.has_finished_actions:
                    for _ in range(self.evolation_speed):
                        self.clone_of_best_player.Update()
                        self.clone_of_best_player.Draw(self.window)
                else:
                    self.replaying_best_player = False
            else:
                self.UpdatePlayersInPopulation()
                self.DrawPopulation()



            # for obs in self.levels[self.player.currentLevelNo].lines:
            #     obs.Draw(self.window)

            pygame.display.update()
            self.FPS(FPS)


JumpKing().run()