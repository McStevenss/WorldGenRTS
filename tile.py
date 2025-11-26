from config import TileIds

class Tile:
    def __init__(self, position, tile_type: TileIds, tile_height):
        self.position = position
        self.tile_type = tile_type
        self.tile_height = tile_height