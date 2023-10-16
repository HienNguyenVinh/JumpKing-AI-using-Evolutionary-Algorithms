from .player import *
from .settings import *

class Population:
    def __init__(self, population_size):
        self.size = population_size
        self.players = [Player() for _ in range(population_size)]
        self.gen = 1

        self.best_player = None
        self.current_highest_player = None
        self.current_showing_level_no = 0
        self.fitness_sum = 0
        self.best_height = 0
        self.current_best_level_reached = 0
        self.new_level_reached = False
        self.reached_best_level_at_action_no = 0
        self.clone_of_best_player_from_pre_generation = None

        self.showing_fail = False
        self.fail_player_no = 0

    def resetAllPlayers(self):
        for player in self.players:
            player.resetPlayer()

    def Update(self):
        for i in range(self.size):
            self.players[i].Update(False)
            if self.players[i].currentLevelNo > 0 and not self.showing_fail:
                self.showing_fail = True
                self.fail_player_no = i
                self.resetAllPlayers()

    def setBestPlayer(self):
        self.best_player = self.players[0]
        self.new_level_reached = False

        for player in self.players:
            if player.best_height_reached > self.best_player.best_height_reached:
                self.best_player = player

        if self.best_player.best_level_reached > self.current_best_level_reached:
            self.current_best_level_reached = self.best_player.best_level_reached
            self.new_level_reached = True
            self.reached_best_level_at_action_no = self.best_player.best_level_reached_on_action_no
            print(f'New level, action number: {self.reached_best_level_at_action_no}')

        self.best_height = self.best_player.best_height_reached

    def setCurrentHighestPlayer(self):
        self.current_highest_player = self.players[0]

        for player in self.players:
            if player.getGlobalHeight() > self.current_highest_player.getGlobalHeight():
                self.current_highest_player = player


    def calcFitnessSum(self):
        self.fitness_sum = 0
        for player in self.players:
            player.calcFitness()
            if player.best_level_reached < self.best_player.best_level_reached:
                player.fitness = 0
            self.fitness_sum += player.fitness

    def selectParent(self):
        rand = random.uniform(0, self.fitness_sum)
        running_sum = 0

        for player in self.players:
            running_sum += player.fitness
            if running_sum > rand:
                return player

        return None

    def naturalSelection(self):
        next_gen = []
        self.setBestPlayer()
        self.calcFitnessSum()

        self.clone_of_best_player_from_pre_generation = self.best_player.clone()
        next_gen.append(self.best_player.clone())

        for i in range(1, len(self.players)):
            parent = self.selectParent()
            baby = parent.clone()

            # if the parent fell to the previous level then mutate the baby at the action that caused them to fall
            if parent.felt_to_previous_level:
                baby.brain.mutate_action_number(parent.felt_on_action_no)

            baby.brain.mutate()
            next_gen.append(baby)

        self.players = []
        for i in range(len(next_gen)):
            self.players.append(next_gen[i])

            if not self.new_level_reached and self.current_best_level_reached != 0:
                self.players[i].loadStartOfBestLevelPlayerState()

        self.gen += 1

    def increase_player_moves(self, increase_by):
        for player in self.players:
            player.brain.increase_moves(increase_by)

    def allPlayerFinished(self):
        for player in self.players:
            if not player.has_finished_actions:
                return False
        return True

    def Draw(self, window):
        self.setCurrentHighestPlayer()
        highest_level_no = self.current_highest_player.currentLevelNo

        if self.current_highest_player.currentLevelNo > self.current_highest_player.best_level_reached:
            highest_level_no -= 1

        current_showing_level_no = highest_level_no

        DrawMapLevel(window, current_showing_level_no)

        for player in self.players:
            # if player.currentLevelNo >= highest_level_no - 1 and player.currentLevelNo <= highest_level_no:
            #     player.Draw(window)
            if player.currentLevelNo == highest_level_no:
                player.alreadyShowingSnow = False
                player.Draw(window, False)
