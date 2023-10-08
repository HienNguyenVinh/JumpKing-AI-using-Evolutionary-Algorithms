import math

from .settings import *
from .vector import *
from .line import *
from .levelSetupFunction import *
from .brain import *

def euclidean(x1, y1, x2, y2):
    return ( (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) )**(1/2)

def mapNumber(n, a1, b1, a2, b2):
    r = ((n-a1)*((b2-a2) / (b1-a1))) + a2
    return r

def numberInRange(a, b1, b2):
    return (
        b1 <= a and a <= b2
    ) or (
        b2 <= a and a <= b1
    )

def AreLinesColliding(a1, b1, a2, b2):
    uA = ((b2[0] - a2[0]) * (a1[1] - a2[1]) - (b2[1] - a2[1]) * (a1[0] - a2[0])) / ((b2[1] - a2[1]) * (b1[0] - a1[0]) - (b2[0] - a2[0]) * (b1[1] - a1[1]))
    uB = ((b1[0] - a1[0]) * (a1[1] - a2[1]) - (b1[1] - a1[1]) * (a1[0] - a2[0])) / ((b2[1] - a2[1]) * (b1[0] - a1[0]) - (b2[0] - a2[0]) * (b1[1] - a1[1]))
    if(uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
        intersectionX = a1[0] + (uA * (b1[0] - a1[0]))
        intersectionY = a1[1] + (uA * (b1[1] - a1[1]))
        return [True, intersectionX, intersectionY]
    return [False, 0, 0]


class PlayerState:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.w = PLAYER_WIDTH
        self.h = PLAYER_HEIGHT
        self.velx = 0
        self.vely = 0
        self.pvelx = 0
        self.pvely = 0

        self.jumpStartHeight = 0

        self.currentLevelNo = 0
        self.best_height_reached = 0
        self.best_level_reached = 0
        self.best_level_reached_on_action_no = 0
        self.reached_height_at_step_no = 0

        self.brain_action_number = 0
        self.isOnGround = True

        self.facingRight = True
        self.is_waiting_to_start_action = False
        self.action_started = False

    def clone(self):
        state_clone = PlayerState()
        state_clone.x = self.x
        state_clone.y = self.y
        state_clone.velx = self.velx
        state_clone.vely = self.vely
        state_clone.isOnGround = self.isOnGround

        state_clone.best_height_reached = self.best_height_reached
        state_clone.best_level_reached = self.best_level_reached
        state_clone.reached_height_at_step_no = self.reached_height_at_step_no
        state_clone.best_level_reached_on_action_no = self.best_level_reached_on_action_no
        state_clone.brain_action_number = self.brain_action_number

        state_clone.currentLevelNo = self.currentLevelNo
        state_clone.jumpStartHeight = self.jumpStartHeight
        state_clone.facingRight = self.facingRight

        return state_clone

    def getStateFromPlayer(self, player):
        self.x = player.x
        self.y = player.y
        self.velx = player.velx
        self.vely = player.vely
        self.isOnGround = player.isOnGround

        self.best_height_reached = player.best_height_reached
        self.best_level_reached = player.best_level_reached
        self.reached_height_at_step_no = player.reached_height_at_step_no
        self.best_level_reached_on_action_no = player.best_level_reached_on_action_no
        self.brain_action_number = player.brain.current_instruction_number

        self.currentLevelNo = player.currentLevelNo
        self.jumpStartHeight = player.jumpStartHeight
        self.facingRight = player.facingRight

        self.is_waiting_to_start_action = player.is_waiting_to_start_action
        self.action_started = player.action_started

    def loadStateToPlayer(self, player):
        player.x = self.x
        player.y = self.y
        player.velx = self.velx
        player.vely = self.vely
        player.isOnGround = self.isOnGround

        player.best_height_reached = self.best_height_reached
        player.best_level_reached = self.best_level_reached
        player.reached_height_at_step_no = self.reached_height_at_step_no
        player.best_level_reached_on_action_no = self.best_level_reached_on_action_no
        player.brain.current_instruction_number = self.brain_action_number

        player.currentLevelNo = self.currentLevelNo
        player.jumpStartHeight = self.jumpStartHeight
        player.facingRight = self.facingRight

class Player:
    runCycleIdx = 0
    runCycle = (
        [PLAYER_RUN_IMAGE_1]*6 +
        [PLAYER_RUN_IMAGE_2]*6 +
        [PLAYER_RUN_IMAGE_3]*6 +
        [PLAYER_RUN_IMAGE_3]*6 +
        [PLAYER_RUN_IMAGE_2]*6 +
        [PLAYER_RUN_IMAGE_1]*6
    )
    def __init__(self):
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.w = PLAYER_WIDTH
        self.h = PLAYER_HEIGHT
        self.velx = 0
        self.vely = 0
        self.pvelx = 0
        self.pvely = 0

        self.jumpTimer = 0

        self.jumpStartHeight = 0

        self.currentLevelNo = 0
        self.best_height_reached = 0
        self.best_level_reached = 0
        self.best_level_reached_on_action_no = 0
        self.fitness = 0
        self.num_of_coins_picked_up = 0
        self.felt_to_previous_level = False
        self.has_finished_actions = False
        self.felt_on_action_no = 0
        self.reached_height_at_step_no = 0
        self.get_new_player_state_at_end_of_update = False
        self.player_state_of_best_level = PlayerState()

        self.players_dead = False

        self.is_waiting_to_start_action = False
        self.action_started = False
        self.brain = Brain(starting_player_actions)
        self.current_action = None
        self.ai_action_timer = 0
        self.ai_action_max_time = 0

        self.isOnGround = True
        self.isRunning = False
        self.isSliding = False
        self.isSlidingLeft = False
        self.hasBumped = False
        self.hasFallen = False

        self.facingRight = True

        self.jumpHeld = False
        self.leftHeld = False
        self.rightHeld = False

        self.max_collisions_checks = 20
        self.current_number_of_collision_checks = 0

    def clone(self):
        clone = Player()
        clone.brain = self.brain.clone()
        clone.player_state_of_best_level = self.player_state_of_best_level.clone()
        clone.brain.parent_reached_best_level_at_action_no = self.best_level_reached_on_action_no
        return clone

    def isPlayerOnGround(self, currentLines):
        self.y += 1
        for line in currentLines:
            if not line.isHorizontal: continue
            if self.CheckCollideWithLine(line):
                self.y -= 1
                return True
        self.y -= 1
        return False


    def isPlayerOnDiagonal(self, currentLines):
        self.y += 5
        for line in currentLines:
            if not line.isDiagonal: continue
            if self.CheckCollideWithLine(line):
                self.y -= 5
                return True
        self.y -= 5
        return False


    def isMovingLeft(self):
        return self.velx < 0


    def isMovingRight(self):
        return self.velx > 0


    def isMovingUp(self):
        return self.vely < 0


    def isMovingDown(self):
        return self.vely > 0


    def CheckCollideWithLine(self, line):
        if line.isHorizontal:
            onX = (
                line.x1 < self.x and self.x < line.x2
            ) or (
                line.x1 < self.x+self.w and self.x+self.w < line.x2
            ) or (
                self.x < line.x1 and line.x1 < self.x+self.w 
            ) or (
                self.x < line.x2 and line.x2 < self.x+self.w
            )
            onY = self.y < line.y1 and line.y1 < self.y+self.h
            return onX and onY
        elif line.isVertical:
            onY = (
                line.y1 < self.y and self.y < line.y2
            ) or (
                line.y1 < self.y+self.h and self.y+self.h < line.y2
            ) or (
                self.y < line.y1 and line.y1 < self.y+self.h 
            ) or (
                self.y < line.y2 and line.y2 < self.y+self.h
            )
            onX = self.x < line.x1 and line.x1 < self.x+self.w
            return onX and onY
        else:
            tl = Point(self.x, self.y)
            tr = Point(tl.x+self.w, tl.y)
            bl = Point(tl.x, tl.y+self.h-1) # -1 to let player float on ground so we wont fell into infinite collision
            br = Point(tr.x, tr.y+self.h-1)

            lCollided = AreLinesColliding(tl, bl, line.p1, line.p2)
            rCollided = AreLinesColliding(tr, br, line.p1, line.p2)
            tCollided = AreLinesColliding(tl, tr, line.p1, line.p2)
            bCollided = AreLinesColliding(bl, br, line.p1, line.p2)

            if lCollided[0] or rCollided[0] or tCollided[0] or bCollided[0]:
                cInfo = DiagonalCollisionInfo()
                cInfo.collidePlayerL = lCollided[0]
                cInfo.collidePlayerR = rCollided[0]
                cInfo.collidePlayerT = tCollided[0]
                cInfo.collidePlayerB = bCollided[0]

                if lCollided[0]:
                    cInfo.collisionPoints.append(Point(lCollided[1], lCollided[2]))
                if rCollided[0]:
                    cInfo.collisionPoints.append(Point(rCollided[1], rCollided[2]))
                if tCollided[0]:
                    cInfo.collisionPoints.append(Point(tCollided[1], tCollided[2]))
                if bCollided[0]:
                    cInfo.collisionPoints.append(Point(bCollided[1], bCollided[2]))
                line.SetDiagonalCollisionInfo(cInfo)
                return True
            else:
                return False


    def GetPriorityCollision(self, collidedLines):
        if len(collidedLines) == 2:
            vert = None
            hori = None
            diag = None
            if collidedLines[0].isVertical: vert = collidedLines[0]
            if collidedLines[0].isHorizontal: hori = collidedLines[0]
            if collidedLines[0].isDiagonal: diag = collidedLines[0]
            if collidedLines[1].isVertical: vert = collidedLines[1]
            if collidedLines[1].isHorizontal: hori = collidedLines[1]
            if collidedLines[1].isDiagonal: diag = collidedLines[1]

            if vert is not None and hori is not None:
                if self.isMovingUp():
                    if vert.center.y > hori.center.y:
                        return vert
                    else:
                        return hori
                else:
                    if vert.center.y < hori.center.y:
                        return vert
                    else:
                        return hori
            if hori is not None and diag is not None:
                if diag.center.y > hori.center.y:
                    return hori

        maxXCorrectionAllowed = -self.velx
        maxYCorrectionAllowed = -self.vely
        minCorrection = WIDTH*HEIGHT
        chosenLine = None
        for line in collidedLines:
            if line.isHorizontal:
                if self.isMovingDown():
                    vector = Vector(0, line.y1 - (self.y+self.h))
                    correction = abs( line.y1 - (self.y+self.h) )
                else:
                    vector = Vector(0, line.y1 - self.y)
                    correction = abs( line.y1 - self.y )
            elif line.isVertical:
                if self.isMovingRight():
                    vector = Vector(line.x1 - (self.x+self.w), 0)
                    correction = abs( line.x1 - (self.x+self.w) )
                else:
                    vector = Vector(line.x1 - self.x, 0)
                    correction = abs( line.x1 - self.x )
            else:
                if len(line.diagonalCollisionInfo.collisionPoints)==1:
                    if line.diagonalCollisionInfo.collidePlayerT:
                        vector = Vector(0, max(line.y1, line.y2) - self.y)
                        correction = abs( vector.y )
                    if line.diagonalCollisionInfo.collidePlayerB:
                        vector = Vector(0, min(line.y1, line.y2) - (self.y+self.h))
                        correction = abs( vector.y )
                    if line.diagonalCollisionInfo.collidePlayerL:
                        vector = Vector(0, max(line.x1, line.x2) - self.x)
                        correction = abs( vector.x )
                    if line.diagonalCollisionInfo.collidePlayerR:
                        vector = Vector(0, min(line.x1, line.x2) - (self.x+self.w))
                        correction = abs( vector.x )
                else:
                    pa, pb = line.diagonalCollisionInfo.collisionPoints[:2]
                    center = Point( (pa.x+pb.x)/2, (pa.y+pb.y)/2 )
                    cT = line.diagonalCollisionInfo.collidePlayerT
                    cB = line.diagonalCollisionInfo.collidePlayerB
                    cL = line.diagonalCollisionInfo.collidePlayerL
                    cR = line.diagonalCollisionInfo.collidePlayerR
                    if   cT and cL: 
                        playerCollidedCorner = Point(self.x       , self.y       )
                    elif cT and cR: 
                        playerCollidedCorner = Point(self.x+self.w, self.y       )
                    elif cB and cL: 
                        playerCollidedCorner = Point(self.x       , self.y+self.h)
                    elif cB and cR: 
                        playerCollidedCorner = Point(self.x+self.w, self.y+self.h)
                    else:
                        pccX = self.x+(int(self.isMovingRight())*self.w)
                        pccY = self.y+(int(self.isMovingDown())*self.h)
                        playerCollidedCorner = Point(pccX, pccY)
                    vector = Vector( center.x - playerCollidedCorner.x, center.y - playerCollidedCorner.y )
                    correction = euclidean(center.x, center.y, playerCollidedCorner.x, playerCollidedCorner.y)
            if correction < minCorrection:
                minCorrection = correction
                chosenLine = line
        return chosenLine


    def CheckCollisions(self, lines):
        collidedLines = []
        for line in lines:
            if self.CheckCollideWithLine(line):
                collidedLines.append(line)
        line = self.GetPriorityCollision(collidedLines)
        if not line: return

        potentialLanding = False
        if line.isHorizontal:
            if self.isMovingDown():
                self.y = line.y1 - self.h
                if len(collidedLines) > 1:
                    potentialLanding = True
                    self.velx, self.vely = 0, 0
                else:
                    self.Land()
            else:
                self.vely = -self.vely/2
                self.y = line.y1
        elif line.isVertical:
            if self.isMovingRight():
                self.x = line.x1 - self.w
            elif self.isMovingLeft():
                self.x = line.x1
            else:
                if self.pvelx > 0:
                    self.x = line.x1 - self.w
                else:
                    self.x = line.x1
            self.velx = -self.velx/2
            if not self.isOnGround:
                self.hasBumped = True
        else:
            self.isSliding = True
            self.hasBumped = True
            if len(line.diagonalCollisionInfo.collisionPoints)==1:
                if line.diagonalCollisionInfo.collidePlayerT:
                    self.y = max(line.y1, line.y2)+1
                    self.vely = -self.vely/2
                if line.diagonalCollisionInfo.collidePlayerB:
                    self.isOnGround = True
                    self.y = min(line.y1, line.y2)-self.h-1
                    self.velx, self.vely = 0, 0
                if line.diagonalCollisionInfo.collidePlayerL:
                    self.x = max(line.x1, line.x2)+1
                    if self.isMovingLeft():
                        self.velx = -self.velx/2
                    if not self.isOnGround: self.hasBumped = True
                if line.diagonalCollisionInfo.collidePlayerR:
                    self.x = min(line.x1, line.x2)-self.w-1
                    if self.isMovingRight():
                        self.velx = -self.velx/2
                    if not self.isOnGround: self.hasBumped = True
            else:
                pa, pb = line.diagonalCollisionInfo.collisionPoints[:2]
                center = Point( (pa.x+pb.x)/2, (pa.y+pb.y)/2 )
                cT = line.diagonalCollisionInfo.collidePlayerT
                cB = line.diagonalCollisionInfo.collidePlayerB
                cL = line.diagonalCollisionInfo.collidePlayerL
                cR = line.diagonalCollisionInfo.collidePlayerR
                if   cT and cL: 
                    playerCollidedCorner = Point(self.x       , self.y       )
                elif cT and cR: 
                    playerCollidedCorner = Point(self.x+self.w, self.y       )
                elif cB and cL: 
                    playerCollidedCorner = Point(self.x       , self.y+self.h)
                    self.isSlidingLeft = False
                elif cB and cR: 
                    playerCollidedCorner = Point(self.x+self.w, self.y+self.h)
                    self.isSlidingLeft = True
                else:
                    pccX = self.x+(int(self.isMovingRight())*self.w)
                    pccY = self.y+(int(self.isMovingDown())*self.h)
                    playerCollidedCorner = Point(pccX, pccY)

                self.x += center.x - playerCollidedCorner.x
                self.y += center.y - playerCollidedCorner.y

                lineVector = Vector( line.x2-line.x1, line.y2-line.y1 )
                lineVector = VectorNormalize(lineVector)

                speedMagnitude = VectorDot(Vector(self.velx, self.vely), lineVector)

                self.velx, self.vely = VectorMult(lineVector, speedMagnitude)

                if cT:
                    self.velx, self.vely = 0, 0
                    self.isSliding = False

        if len(collidedLines) > 1:
            self.current_number_of_collision_checks += 1
            if self.current_number_of_collision_checks > self.max_collisions_checks:
                self.has_finished_actions = True
                self.players_dead = True

            if potentialLanding:
                if self.isPlayerOnGround(lines):
                    self.Land()


    def CheckForLevelChange(self):
        if self.y < -self.h:
            self.currentLevelNo += 1
            self.y += HEIGHT
        elif self.y > HEIGHT-self.h:
            if self.currentLevelNo == 0:
                self.currentLevelNo = 1
                self.players_dead = True
                self.has_finished_actions = True

            self.currentLevelNo -= 1
            self.y -= HEIGHT

            if not self.has_finished_actions and self.currentLevelNo < self.best_level_reached - 1:
                self.felt_to_previous_level = True
                self.felt_on_action_no = self.brain.current_instruction_number
                self.has_finished_actions = True


    def ApplyGravity(self):
        if self.isOnGround:
            self.vely = 0
            return
        elif self.isSliding:
            self.vely = min(self.vely + GRAVITY*0.5, TERMINAL_VELOCITY*0.5)
            if self.isSlidingLeft:
                self.velx = max(self.velx - GRAVITY*0.5, -TERMINAL_VELOCITY*0.5)
            else:
                self.velx = min(self.velx + GRAVITY*0.5, TERMINAL_VELOCITY*0.5)
        else:
            self.vely = min(self.vely + GRAVITY, TERMINAL_VELOCITY)


    def Jump(self):
        if not self.isOnGround: return
        verticalJumpSpeed = mapNumber(self.jumpTimer, 0, MAX_JUMP_TIMER, MIN_JUMP_SPEED, MAX_JUMP_SPEED)
        self.vely = -verticalJumpSpeed
        if self.leftHeld:
            self.velx = -JUMP_SPEED_HORIZONTAL
        elif self.rightHeld:
            self.velx = JUMP_SPEED_HORIZONTAL
        else:
            self.velx = 0
        self.hasFallen = False
        self.isOnGround = False
        self.jumpTimer = 0
        self.jumpStartHeight = (HEIGHT - self.y) + HEIGHT * self.currentLevelNo


    def Land(self):
        self.isOnGround = True
        self.isSliding = False
        self.hasBumped = False
        self.hasFallen = False
        if (self.jumpStartHeight - HEIGHT / 2 > (HEIGHT - self.y) + HEIGHT * self.currentLevelNo):
            self.hasFallen = True

        if self.getGlobalHeight() > self.best_height_reached:
            self.best_height_reached = self.getGlobalHeight()
            self.reached_height_at_step_no = self.brain.current_instruction_number

            if self.best_level_reached < self.currentLevelNo:
                self.best_level_reached = self.currentLevelNo
                self.best_level_reached_on_action_no = self.brain.current_instruction_number
                self.get_new_player_state_at_end_of_update = True


        if not self.has_finished_actions and self.currentLevelNo < self.best_level_reached:
            self.felt_to_previous_level = True
            self.felt_on_action_no = self.brain.current_instruction_number
            self.has_finished_actions = True


    def UpdatePlayerSlide(self, lines):
        if self.isSliding:
            if not self.isPlayerOnDiagonal(lines):
                self.isSliding = False


    def UpdatePlayerRun(self, lines):
        self.isRunning = False
        if self.isOnGround:
            if not self.isPlayerOnGround(lines):
                self.isOnGround = False
                return
            if self.jumpHeld:
                self.velx = 0
                self.vely = 0
            else:
                if self.rightHeld:
                    self.hasFallen = False
                    self.isRunning = True
                    self.facingRight = True
                    self.velx = RUN_SPEED
                    self.vely = 0
                elif self.leftHeld:
                    self.hasFallen = False
                    self.isRunning = True
                    self.facingRight = False
                    self.velx = -RUN_SPEED
                    self.vely = 0
                else:
                    self.velx = 0
                    self.vely = 0


    def UpdatePlayerJump(self):
        if not self.jumpHeld and self.jumpTimer>0:
            self.Jump()


    def UpdateJumpTimer(self):
        if self.isOnGround and self.jumpHeld and self.jumpTimer < MAX_JUMP_TIMER:
            self.jumpTimer += 1


    def Update(self):
        if self.players_dead:
            return

        currentLines = MAP_LINES[self.currentLevelNo].lines

        if not self.has_finished_actions and not testing_single_player:
            self.updateAIAction()

        self.UpdatePlayerSlide(currentLines)
        self.ApplyGravity()
        self.UpdatePlayerRun(currentLines)
        self.UpdatePlayerJump()

        self.x += self.velx
        self.y += self.vely

        self.pvelx = self.velx
        self.pvely = self.vely

        self.current_number_of_collision_checks = 0
        self.CheckCollisions(currentLines)
        self.UpdateJumpTimer()
        self.CheckForLevelChange()

        if self.get_new_player_state_at_end_of_update:
            if self.currentLevelNo != 37:
                self.player_state_of_best_level.getStateFromPlayer(self)
            self.get_new_player_state_at_end_of_update = False




    def GetSpriteToDraw(self):
        if self.jumpHeld and self.isOnGround: return PLAYER_SQUAT_IMAGE
        if self.hasFallen: return PLAYER_FALLEN_IMAGE
        if self.hasBumped: return PLAYER_BUMP_IMAGE
        if self.vely < 0: return PLAYER_JUMP_IMAGE
        if self.isRunning:
            self.runCycleIdx = (self.runCycleIdx+1)%len(self.runCycle)
            return self.runCycle[self.runCycleIdx]
        if self.isOnGround: return PLAYER_IDLE_IMAGE
        return PLAYER_FALL_IMAGE

    def getGlobalHeight(self):
        return (HEIGHT - self.y) + HEIGHT * self.currentLevelNo

    def calcFitness(self):
        coin_value = 500000
        score_height = self.best_height_reached - (HEIGHT * self.best_level_reached)
        self.fitness = score_height ** 2 + coin_value * self.num_of_coins_picked_up

    def loadStartOfBestLevelPlayerState(self):
        self.player_state_of_best_level.loadStateToPlayer(self)

    def startCurrentAction(self):
        self.ai_action_max_time = math.floor(self.current_action.hold_time * 30)
        self.ai_action_timer = 0
        if self.current_action.is_jump:
            self.jumpHeld = True
        if self.current_action.x_direction == -1:
            self.leftHeld = True
            self.rightHeld = False
        if self.current_action.x_direction == 1:
            self.leftHeld = False
            self.rightHeld = True

    def endCurrentAction(self):
        if self.current_action.is_jump:
            self.jumpHeld = False
            self.Jump()

        self.leftHeld = False
        self.rightHeld = False
        self.is_waiting_to_start_action = False

    def updateAIAction(self):
        if self.is_waiting_to_start_action and self.isOnGround:
            self.is_waiting_to_start_action = False

        if self.isOnGround and not self.action_started:
            self.current_action = self.brain.get_next_action()
            if not self.current_action:
                self.has_finished_actions = True
                return

            self.startCurrentAction()
            self.action_started = True
        elif self.action_started:
            self.ai_action_timer += 1
            if self.ai_action_timer >= self.ai_action_max_time:
                self.endCurrentAction()
                self.action_started = False

    def Draw(self, window):
        if self.players_dead:
            return

        img = self.GetSpriteToDraw()
        imgW, imgH = img.get_size()
        img = pygame.transform.flip(img, not self.facingRight, False)
        window.blit(img, ( self.x+(self.w/2)-(imgW/2) , self.y+self.h-imgH))