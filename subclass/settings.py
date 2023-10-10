import pygame
import os

IMAGE_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
SOUND_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds")

POPULATION_SIZE = 100
EVOLATION_SPEED = 3

testing_single_player = False
replaying_best_player = False

current_showing_level_no = 0

FPS = 60
WIDTH = 1200
HEIGHT = 900
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 65


"""
Player
"""
RUN_SPEED = 4
MIN_JUMP_SPEED = 5
MAX_JUMP_SPEED = 22
MAX_JUMP_TIMER = 30
JUMP_SPEED_HORIZONTAL = 8
TERMINAL_VELOCITY = 20
GRAVITY = 0.6

starting_player_actions = 5
increase_actions_by_amount = 5
increase_actions_every_X_generations = 10

evolation_speed = 1

# images
PLAYER_RUN_IMAGE_1 = pygame.image.load(os.path.join(IMAGE_PATH, "poses", "run1.png"))
PLAYER_RUN_IMAGE_2 = pygame.image.load(os.path.join(IMAGE_PATH, "poses", "run2.png"))
PLAYER_RUN_IMAGE_3 = pygame.image.load(os.path.join(IMAGE_PATH, "poses", "run3.png"))
PLAYER_SQUAT_IMAGE = pygame.image.load(os.path.join(IMAGE_PATH, "poses", "squat.png"))
PLAYER_FALLEN_IMAGE = pygame.image.load(os.path.join(IMAGE_PATH, "poses", "fallen.png"))
PLAYER_BUMP_IMAGE = pygame.image.load(os.path.join(IMAGE_PATH, "poses", "bump.png"))
PLAYER_JUMP_IMAGE = pygame.image.load(os.path.join(IMAGE_PATH, "poses", "jump.png"))
PLAYER_IDLE_IMAGE = pygame.image.load(os.path.join(IMAGE_PATH, "poses", "idle.png"))
PLAYER_FALL_IMAGE = pygame.image.load(os.path.join(IMAGE_PATH, "poses", "fall.png"))
