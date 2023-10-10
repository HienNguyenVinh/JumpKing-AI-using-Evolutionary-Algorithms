from .line import *
from .settings import *
from .coin import *
import json

def DrawMapLevel(window, levelIdx):
    map = MAP_LINES[levelIdx]
    window.blit(map.bg, (0, 0))
    # for line in map.lines:
    #     line.Draw(window)


class Level:
    def __init__(self, bg, lines):
        self.bg = bg
        self.lines = lines
        self.is_blizzard_level = False
        self.is_ice_level = False

        self.coins = []
        self.has_progression_coins = False




class MapLoader:
    def __init__(self, path):
        self.path = path
        with open(path, "r") as f:
            self.data = json.load(f)

    def loadLevels(self):
        levels = []
        for idx in self.data:
            lines = []
            for lineData in self.data[idx]["lines"]:
                lines.append(Line(*lineData))
            levels.append(Level(
                bg = pygame.image.load(os.path.join(IMAGE_PATH, "bg", f"{idx}.png")),
                lines = lines
            ))
            # print(idx)
            if  25 < int(idx) < 33:
                levels[int(idx) - 1].is_blizzard_level = True
            if 36 < int(idx) < 40:
                levels[int(idx) - 1].is_ice_level = True
        return levels

MAP_LINES = MapLoader("subclass/map.json").loadLevels()

MAP_LINES[4].coins.append(Coin(143, 160))
MAP_LINES[5].coins.append(Coin(801, 140))
MAP_LINES[6].coins.append(Coin(419, 541))
MAP_LINES[8].coins.append(Coin(780, 459))
MAP_LINES[16].coins.append(Coin(650, 570))
MAP_LINES[16].coins.append(Coin(195, 339))
MAP_LINES[17].coins.append(Coin(722, 648))
MAP_LINES[17].coins.append(Coin(1184, 781))
MAP_LINES[17].coins.append(Coin(1077, 297))
MAP_LINES[24].coins.append(Coin(971, 514))
MAP_LINES[36].coins.append(Coin(158, 666))
MAP_LINES[37].coins.append(Coin(721, 187))
MAP_LINES[37].coins.append(Coin(1042, 151))
MAP_LINES[42].coins.append(Coin(986, 306))

# MAP_LINES[0].coins.append(Coin(143, 148))

MAP_LINES[1].coins.append(Coin(143, 148, 'progress'))
MAP_LINES[1].coins.append(Coin(155, 142, 'progress'))
MAP_LINES[1].coins.append(Coin(65, 148, 'progress'))
MAP_LINES[2].coins.append(Coin(125, 187, 'progress'))
MAP_LINES[2].coins.append(Coin( 51, 183, 'progress'))
MAP_LINES[3].coins.append(Coin(843, 125, 'progress'))
MAP_LINES[3].coins.append(Coin(411, 170, 'progress'))
MAP_LINES[4].coins.append(Coin(137, 173, 'progress'))
MAP_LINES[5].coins.append(Coin(1122, 65, 'progress'))
MAP_LINES[5].coins.append(Coin(1121, 151, 'progress'))
MAP_LINES[5].coins.append(Coin(1101, 92, 'progress'))
MAP_LINES[6].coins.append(Coin(349, 74, 'progress'))
MAP_LINES[7].coins.append(Coin(154, 293, 'progress'))
MAP_LINES[8].coins.append(Coin(602, 182, 'progress'))
MAP_LINES[12].coins.append(Coin(1135, 37, 'progress'))
MAP_LINES[13].coins.append(Coin(665, 193, 'progress'))
MAP_LINES[13].coins.append(Coin(587, 194, 'progress'))
MAP_LINES[17].coins.append(Coin(975, 147, 'progress'))
MAP_LINES[22].coins.append(Coin(1139, 111, 'progress'))
MAP_LINES[36].coins.append(Coin(686, 205, 'progress'))
MAP_LINES[37].coins.append(Coin(1005, 181, 'progress'))
MAP_LINES[39].coins.append(Coin(365, 187, 'progress'))


MAP_LINES[1].has_progression_coins = True
MAP_LINES[2].has_progression_coins = True
MAP_LINES[3].has_progression_coins = True
MAP_LINES[4].has_progression_coins = True
MAP_LINES[5].has_progression_coins = True
MAP_LINES[6].has_progression_coins = True
MAP_LINES[7].has_progression_coins = True
MAP_LINES[8].has_progression_coins = True
MAP_LINES[12].has_progression_coins = True
MAP_LINES[13].has_progression_coins = True
MAP_LINES[17].has_progression_coins = True
MAP_LINES[22].has_progression_coins = True
MAP_LINES[36].has_progression_coins = True
MAP_LINES[37].has_progression_coins = True
MAP_LINES[39].has_progression_coins = True
    
    
