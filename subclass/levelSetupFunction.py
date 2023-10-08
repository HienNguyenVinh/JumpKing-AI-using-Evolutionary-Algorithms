from .line import *
from .settings import *
import json

class Level:
    def __init__(self, bg, lines):
        self.bg = bg
        self.lines = lines
        self.is_blizzard_level = False
        self.is_ice_level = False


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
    
    
