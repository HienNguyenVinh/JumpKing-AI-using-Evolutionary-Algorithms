import random

class AIAction:
    def __init__(self, is_jump, hold_time, x_direction):
        self.is_jump = is_jump
        self.hold_time = hold_time  # number between 0 and 1
        self.x_direction = x_direction

    def clone(self):
        return AIAction(self.is_jump, self.hold_time, self.x_direction)

    def mutate(self):
        self.hold_time += random.uniform(-0.3, 0.3)
        self.hold_time = max(0.1, min(1, self.hold_time))

jump_chance = 0.5  # the chance that a random action is a jump
chance_of_full_jump = 0.2

class Brain:
    def __init__(self, size, randomise_instructions=True):
        self.size = size
        self.instructions = []
        self.current_instruction_number = 0
        if randomise_instructions:
            self.randomize(size)
        self.parent_reached_best_level_at_action_no = 0

    def randomize(self, size):
        for i in range(size):
            self.instructions.append(self.get_random_action())

    def get_random_action(self):
        is_jump = random.random() > jump_chance

        hold_time = random.uniform(0.1, 1)
        if random.random() < chance_of_full_jump:
            hold_time = 1

        directions = [-1, -1, -1, 0, 1, 1, 1]
        x_direction = random.choice(directions)

        return AIAction(is_jump, hold_time, x_direction)

    def get_next_action(self):
        if self.current_instruction_number >= len(self.instructions):
            return None
        self.current_instruction_number += 1
        return self.instructions[self.current_instruction_number - 1]

    def clone(self):
        clone = Brain(self.size, False)
        clone.instructions = []
        for i in range(len(self.instructions)):
            clone.instructions.append(self.instructions[i].clone())
        return clone

    def mutate(self):
        mutation_rate = 0.1
        chance_of_new_instruction = 0.02

        for i in range(self.parent_reached_best_level_at_action_no, len(self.instructions)):
            if random.random() < chance_of_new_instruction:
                self.instructions[i] = self.get_random_action()
            elif random.random() < mutation_rate:
                self.instructions[i].mutate()

    def mutate_action_number(self, action_number):
        action_number -= 1  # this is done because I'm a bad programmer
        chance_of_new_instruction = 0.2
        if random.random() < chance_of_new_instruction:
            self.instructions[action_number] = self.get_random_action()
        else:
            self.instructions[action_number].mutate()

    def increase_moves(self, increase_moves_by):
        for i in range(increase_moves_by):
            self.instructions.append(self.get_random_action())
