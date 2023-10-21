import math

from .vector import *
from .levelSetupFunction import *
from .brain import *
from .settings import *

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

        self.blizzard_force = 0
        self.blizzard_force_acceleration_direction = 1
        self.max_blizzard_force_timer = 0
        self.snow_image_position = 0

    def getStateFromPlayer(self, player):
        self.x = player.x
        self.y = player.y
        self.velx = player.velx
        self.vely = player.vely
        self.isOnGround = player.isOnGround

        self.blizzard_force = player.blizzard_force
        self.blizzard_force_acceleration_direction = player.blizzard_force_acceleration_direction
        self.max_blizzard_force_timer = player.max_blizzard_force_timer
        self.snow_image_position = player.snow_image_position

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

        player.blizzard_force = self.blizzard_force
        player.blizzard_force_acceleration_direction = self.blizzard_force_acceleration_direction
        player.max_blizzard_force_timer = self.max_blizzard_force_timer
        player.snow_image_position = self.snow_image_position

        player.best_height_reached = self.best_height_reached
        player.best_level_reached = self.best_level_reached
        player.reached_height_at_step_no = self.reached_height_at_step_no
        player.best_level_reached_on_action_no = self.best_level_reached_on_action_no
        player.brain.current_instruction_number = self.brain_action_number

        player.currentLevelNo = self.currentLevelNo
        player.jumpStartHeight = self.jumpStartHeight
        player.facingRight = self.facingRight

        player.is_waiting_to_start_action = self.is_waiting_to_start_action
        player.action_started = self.action_started

    def clone(self):
        state_clone = PlayerState()
        state_clone.x = self.x
        state_clone.y = self.y
        state_clone.velx = self.velx
        state_clone.vely = self.vely
        state_clone.isOnGround = self.isOnGround

        state_clone.blizzard_force = self.blizzard_force
        state_clone.blizzard_force_acceleration_direction = self.blizzard_force_acceleration_direction
        state_clone.max_blizzard_force_timer = self.max_blizzard_force_timer
        state_clone.snow_image_position = self.snow_image_position

        state_clone.best_height_reached = self.best_height_reached
        state_clone.best_level_reached = self.best_level_reached
        state_clone.reached_height_at_step_no = self.reached_height_at_step_no
        state_clone.best_level_reached_on_action_no = self.best_level_reached_on_action_no
        state_clone.brain_action_number = self.brain_action_number

        state_clone.currentLevelNo = self.currentLevelNo
        state_clone.jumpStartHeight = self.jumpStartHeight
        state_clone.facingRight = self.facingRight

        return state_clone

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
        self.is_finish = False

        self.isOnGround = False
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

        # for snow level
        self.alreadyShowingSnow = False
        self.blizzard_force = 0
        self.blizzard_force_acceleration_direction = 1
        self.max_blizzard_force_timer = 0
        self.snow_image_position = 0

        # population info
        self.best_level_reached_on_action_no = 0
        self.fitness = 0
        self.felt_to_previous_level = False
        self.has_finished_actions = False
        self.felt_on_action_no = 0
        self.reached_height_at_step_no = 0
        self.get_new_player_state_at_end_of_update = False
        self.player_state_of_best_level = PlayerState()

        self.players_dead = False

        # AI actions
        self.is_waiting_to_start_action = False
        self.action_started = False
        self.brain = Brain(starting_player_actions)
        self.current_action = None
        self.ai_action_timer = 0
        self.ai_action_max_time = 0

        # coins info
        self.num_of_coins_picked_up = 0
        self.coins_picked_up_idx = []
        self.progression_coin_picked_up = False

    def clone(self):
        clone = Player()
        clone.brain = self.brain.clone()
        clone.player_state_of_best_level = self.player_state_of_best_level.clone()
        clone.brain.parent_reached_best_level_at_action_no = self.best_level_reached_on_action_no
        return clone

    def resetPlayer(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.velx = 0
        self.vely = 0
        self.isOnGround = False

        self.jumpTimer = 0
        self.jumpHeld = False
        self.leftHeld = False
        self.rightHeld = False

        self.blizzard_force = 0
        self.blizzard_force_acceleration_direction = 1
        self.max_blizzard_force_timer = 0
        self.snow_image_position = 0

        self.isRunning = False
        self.isSliding = False
        self.isSlidingLeft = False
        self.hasBumped = False
        self.facingRight = True

        self.currentLevelNo = 0

        self.hasFallen = False
        self.jumpStartHeight = 0

        self.ai_action_timer = 0
        self.ai_action_max_time = 0
        self.is_waiting_to_start_action = False
        self.action_started = False

        self.brain.current_instruction_number = 0
        self.current_action = None

        self.players_dead = False
        self.pvelx = 0
        self.pvely = 0
        self.best_height_reached = 0
        self.reached_height_at_step_no = 0

        self.fitness = 0
        self.has_finished_actions = False

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
        # if we are going up and then we hit a verticle and a horizontal and if the midpoint of the vert is lower then
        # we need to do the verticle one first because that should be blocking the horizontal one
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
                # so the player has potentially landed
                #correct the position first then player has landed

                self.y = line.y1 - self.h
                if len(collidedLines) > 1:
                    potentialLanding = True
                    self.velx, self.vely = 0, 0
                else:
                    self.Land()
            else:
                # if moving up then we've hit a roof and we bounce off
                self.vely = -self.vely/2
                self.y = line.y1

        elif line.isVertical:
            if self.isMovingRight():
                self.x = line.x1 - self.w
            elif self.isMovingLeft():
                self.x = line.x1
            else:
                # this means we've hit a wall but we arent moving left or right
                # meaning we prioritised the floor first which stopped our velocity
                # so we need a variable to store the speed we had before any transions were made
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

    def ApplyBlizzardForce(self):
        if not MAP_LINES[self.currentLevelNo].is_blizzard_level:
            return

        if abs(self.blizzard_force) >= MaxBlizzardForce:
            self.max_blizzard_force_timer += 1
            if self.max_blizzard_force_timer > BlizzardMaxSpeedHoldTime:
                self.blizzard_force_acceleration_direction *= -1
                self.max_blizzard_force_timer = 0

        self.blizzard_force += self.blizzard_force_acceleration_direction * BlizzardAccelerationMagnitude

        if abs(self.blizzard_force) > MaxBlizzardForce:
            self.blizzard_force = MaxBlizzardForce * self.blizzard_force_acceleration_direction

        self.snow_image_position += self.blizzard_force * BlizzardImageSpeedMultiplier

        if not self.isOnGround:
            self.velx += self.blizzard_force

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
        # if moving down then weve landed
        self.isOnGround = True
        # if were on an ice level then we slide instead
        if MAP_LINES[self.currentLevelNo].is_ice_level:
            self.vely = 0
            if self.isMovingRight():
                self.velx -= PlayerIceRunAcceleration
            else:
                self.velx += PlayerIceRunAcceleration
        else:
            self.velx = 0
            self.vely = 0

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
                self.player_state_of_best_level.getStateFromPlayer(self)
                self.get_new_player_state_at_end_of_update = True

                # setup coins
                self.num_of_coins_picked_up = 0
                self.progression_coin_picked_up = False
                if not MAP_LINES[self.currentLevelNo].has_progression_coins:
                    self.progression_coin_picked_up = True
                self.coins_picked_up_idx = []


        # if the ai fell to a previous level then stop the actions and record when it happened
        if self.currentLevelNo < self.best_level_reached and not self.has_finished_actions:
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


    def Update(self, single_mode):
        if single_mode:
            if self.players_dead:
                return
        else:
            if self.players_dead or self.has_finished_actions:
                return

        if self.currentLevelNo == 42 and self.x >= 920 * alpha and self.y < 300 * alpha:
            self.is_finish = True

        currentLines = MAP_LINES[self.currentLevelNo].lines

        if not self.has_finished_actions and not single_mode:
            self.updateAIAction()

        self.UpdatePlayerSlide(currentLines)
        self.ApplyGravity()
        self.ApplyBlizzardForce()
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
        self.checkForCoinCollisions()

        if self.get_new_player_state_at_end_of_update:
            if self.currentLevelNo != 37:
                self.player_state_of_best_level.getStateFromPlayer(self)
            self.get_new_player_state_at_end_of_update = False


    def getGlobalHeight(self):
        return (HEIGHT - self.y) + HEIGHT * self.currentLevelNo

    def calcFitness(self):
        # current best fitness max just including height is 640,000, getting a coin has to be the most important thing so
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

    def checkForCoinCollisions(self):
        if self.currentLevelNo < self.best_level_reached:
            return
        current_lv = MAP_LINES[self.currentLevelNo]
        for i in range(len(current_lv.coins)):
            if i not in self.coins_picked_up_idx:
                if current_lv.coins[i].collides_with_player(self):
                    if current_lv.coins[i].type == 'reward':
                        if self.isOnGround:
                            self.coins_picked_up_idx.append(i)
                            self.num_of_coins_picked_up += 1
                            print("Got a coin")
                    else:
                        self.coins_picked_up_idx.append(i)
                        self.num_of_coins_picked_up += 1
                        self.progression_coin_picked_up = True
                        print('Got a progress coin')

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


    def Draw(self, window, single_mode):
        if self.players_dead:
            return

        if not single_mode:
            if self.currentLevelNo == current_showing_level_no - 1:
                if self.y < self.h:
                    self.y = self.y + self.h
                else:
                    return

        img = self.GetSpriteToDraw()
        imgW, imgH = img.get_size()
        img = pygame.transform.flip(img, not self.facingRight, False)
        window.blit(img, ( self.x+(self.w/2)-(imgW/2) , self.y+self.h-imgH))

        # show snow
        if MAP_LINES[self.currentLevelNo].is_blizzard_level and (not self.alreadyShowingSnow or single_mode):
            # window.blit(SnowImage, (0, 0))
            snowDrawPosition = self.snow_image_position
            while snowDrawPosition <= 0:
                snowDrawPosition += WIDTH
            snowDrawPosition = snowDrawPosition % WIDTH

            window.blit(SnowImage, (snowDrawPosition, 0))
            window.blit(SnowImage, (snowDrawPosition - WIDTH, 0))

            self.alreadyShowingSnow = True
