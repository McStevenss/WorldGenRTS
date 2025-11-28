from enum import Enum


class TileIds(Enum):

    ####### Terrain Tiles ######
    DARKWATER = (13,2)
    DARKWATER2 = (14,2)
    WATER = (15,0)
    WATER2 = (14,4)
    SAND = (2,0)
    GRASS = (0,1)
    DARKGRASS = (4,1)
    LIGHTROCK = (7,1)
    ROCK = (6,1)
    MOUNTAIN = (8,4)
    # TREES = (3,4)
    # TREESTUMP = (3,5)
    # TREETOP = (3,3)

    TREES = (0,4)
    TREESTUMP = (0,5)
    TREETOP = (0,3)

    ############################

    ###### Cursor Tiles #######
    CURSOR = (3,13)
    CURSOR_TL = (4,13)
    CURSOR_TR = (5,13)
    CURSOR_BL = (4,14)
    CURSOR_BR = (5,14)
    ############################

    ####### Entity Tiles #######
    HUMAN_VILLAGE = (1,13)

    ############################


# HEIGHT_THRESHOLDS = [
#     (0,  "DARKWATER"),
#     (0.30,  "WATER"),
#     (0.35,  "SAND"),
#     (0.55,  "GRASS"),
#     (0.60,  "DARKGRASS"),
#     (0.75,  "TREES"),
#     (0.85,  "ROCK"),
#     (120.00,  "MOUNTAIN")
# ]

# HEIGHT_THRESHOLDS = [
#     (0.1,  "DARKWATER"),
#     (0.13,  "DARKWATER2"),
#     (0.20,  "WATER"),
#     (0.21,  "WATER2"),
#     (0.25,  "SAND"),
#     (0.35,  "GRASS"),
#     (0.40,  "DARKGRASS"),
#     (0.55,  "TREES"),
#     (0.65,  "ROCK"),
#     (120.00,  "MOUNTAIN")
# ]

HEIGHT_THRESHOLDS = [
    (0.1,  "DARKWATER"),
    (0.13,  "DARKWATER2"),
    (0.20,  "WATER"),
    (0.21,  "WATER2"),
    (0.25,  "SAND"),
    (0.55,  "GRASS"),
    # (0.55,  "DARKGRASS"),
    # (0.55,  "TREES"),
    (0.65,  "ROCK"),
    (120.00,  "MOUNTAIN")
]