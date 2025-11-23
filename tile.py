from config import TileIds

class Tile:
    def __init__(self, position, tile_type: TileIds):
        self.position = position
        self.tile_type = tile_type