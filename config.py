from enum import Enum


class TileIds(Enum):

    ####### Terrain Tiles ######
    DARKWATER = (13,2)
    WATER = (15,0)
    SAND = (2,0)
    GRASS = (0,1)
    DARKGRASS = (4,1)
    TREES = (0,5)
    LIGHTROCK = (7,1)
    ROCK = (6,1)
    MOUNTAIN = (8,4)
    ############################

    ####### Cursor Tiles #######
    CURSOR = (3,13)
    CURSOR_TL = (4,13)
    CURSOR_TR = (5,13)
    CURSOR_BL = (4,14)
    CURSOR_BR = (5,14)
    ############################

    ####### Entity Tiles #######
    HUMAN_VILLAGE = (1,13)

    ############################


HEIGHT_THRESHOLDS = [
    (0,  "DARKWATER"),
    (0.30,  "WATER"),
    (0.35,  "SAND"),
    (0.55,  "GRASS"),
    (0.60,  "DARKGRASS"),
    (0.75,  "TREES"),
    (0.85,  "ROCK"),
    (120.00,  "MOUNTAIN")
]