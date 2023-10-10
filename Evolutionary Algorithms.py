from subclass import *
import pygame

pygame.init()

clock = pygame.time.Clock()
class JumpKing:
    # FPS = pygame.time.Clock().tick

    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.levels = MAP_LINES

        self.testing_single_player = testing_single_player
        self.replaying_best_player = replaying_best_player
        self.clone_of_best_player = None
        self.evolation_speed = EVOLATION_SPEED

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
        self.player.Update()
        self.player.Draw(self.window)

    def DrawPlayer(self):
        self.window.blit(self.levels[self.player.currentLevelNo].bg, (0, 0))
        # for coin in MAP_LINES[self.player.currentLevelNo].coins:
        #     coin.Draw(self.window)
        self.UpdatePlayer()

    def UpdatePlayersInPopulation(self):
        if self.population.allPlayerFinished():
            self.population.naturalSelection()
            if self.population.gen % increase_actions_every_X_generations == 0:
                self.population.increase_player_moves(increase_actions_by_amount)

        # for i in range(evolation_speed):
        #     self.population.Update()
        self.population.Update()
        self.population.Update()
        self.population.Update()

    def DrawPopulation(self):
        self.population.Draw(self.window)
        # for coin in MAP_LINES[self.population.current_showing_level_no].coins:
        #     coin.Draw(self.window)

    def showPopulationInfo(self):
        font = pygame.font.Font(None, 32)
        text_color = (255, 255, 255)

        fps_text = font.render(f'FPS: {round(clock.get_fps())}', True, text_color)
        gen_text = font.render(f'Gen: {self.population.gen}', True, text_color)
        moves_text = font.render(f'Moves: {len(self.population.players[0].brain.instructions)}', True, text_color)
        height_text = font.render(f'Best Height: {self.population.best_height}', True, text_color)

        self.window.blit(fps_text, (WIDTH - 160, 10))
        self.window.blit(gen_text, (30, 10))
        self.window.blit(moves_text, (200, 10))
        self.window.blit(height_text, (400, 10))

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
                        self.replaying_best_player = True
                        self.clone_of_best_player = self.population.clone_of_best_player_from_pre_generation
                        self.evolation_speed = 1

                    if e.key == pygame.K_r:
                        if self.testing_single_player:
                            self.player.resetPlayer()
                        else:
                            self.population.resetAllPlayers()

                    if e.key == pygame.K_n:
                        self.player.currentLevelNo += 1

                    if e.key == pygame.K_i:
                        print(f"Gen: {self.population.gen}")
                        print(f'Moves: {len(self.population.players[0].brain.instructions)}')
                        print(f"Best height: {self.population.best_height}")
                        print(f"Best level: {self.population.current_best_level_reached}")


            if self.testing_single_player:
                self.UpdatePlayer()
                self.DrawPlayer()
            elif self.replaying_best_player:
                if not self.clone_of_best_player.has_finished_actions:
                    for _ in range(self.evolation_speed):
                        self.clone_of_best_player.Update()
                    self.window.blit(self.levels[self.clone_of_best_player.currentLevelNo].bg, (0, 0))
                    self.clone_of_best_player.Draw(self.window)
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
