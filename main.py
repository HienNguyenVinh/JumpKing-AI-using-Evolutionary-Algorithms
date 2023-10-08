from subclass import *
import pygame
import os
pygame.init()

class JumpKing:
    FPS = pygame.time.Clock().tick
    
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.player = Player()
        self.levels = MAP_LINES
        self.player.currentLevelNo = 0


    def checkEvt(self, evt):
        for e in pygame.event.get():
            if e.type == evt:
                return True
        return False


    def UpdatePlayer(self):
        pressedKeys = pygame.key.get_pressed()
        self.player.leftHeld = pressedKeys[pygame.K_LEFT]
        self.player.rightHeld = pressedKeys[pygame.K_RIGHT]
        self.player.jumpHeld = pressedKeys[pygame.K_SPACE]
        self.player.Update()
        self.player.Draw(self.window)



    def run(self):
        while(True):
            if self.checkEvt(pygame.QUIT): break

            self.window.blit(self.levels[self.player.currentLevelNo].bg, (0, 0))
            self.UpdatePlayer()

            # for obs in self.levels[self.player.currentLevelNo].lines:
            #     obs.Draw(self.window)

            pygame.display.update()
            self.FPS(FPS)


JumpKing().run()