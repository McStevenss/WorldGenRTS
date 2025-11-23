from texture_loader import TextureLoader 
from tile import Tile
from config import TileIds
from cursor import Cursor
from typing import List
class Renderer:
    def __init__(self, engine):
        self.engine = engine
        self.screen = self.engine.screen
        self.tile_size = 8
        self.texture_loader = TextureLoader(self.tile_size,"TinyRTS_v06/TinyRTS_v07.png")


    def draw_map(self, map_data: List[List[Tile]]) -> None:
        for row in map_data:
            for tile in row:
                x,y = tile.position
                tile_type = tile.tile_type
                texture = self.texture_loader.get_tile(tile_type.value)
                self.screen.blit(texture, (x*self.tile_size,y*self.tile_size))

    def draw_cursor(self, cursor: Cursor):
        
        size = cursor.size
        x = cursor.position[0]
        y = cursor.position[1]

        if size == 1:
            texture = self.texture_loader.get_tile(TileIds.CURSOR.value)
            self.screen.blit(texture, (x*self.tile_size,y*self.tile_size))
        else:
            TL = self.texture_loader.get_tile(TileIds.CURSOR_TL.value)
            TR = self.texture_loader.get_tile(TileIds.CURSOR_TR.value)
            BL = self.texture_loader.get_tile(TileIds.CURSOR_BL.value)
            BR = self.texture_loader.get_tile(TileIds.CURSOR_BR.value)

            self.screen.blit(TL, (x*self.tile_size,y*self.tile_size))
            self.screen.blit(TR, ((x+size-1)*self.tile_size,y*self.tile_size))
            self.screen.blit(BL, (x*self.tile_size,(y+size-1)*self.tile_size))
            self.screen.blit(BR, ((x+size-1)*self.tile_size,(y+size-1)*self.tile_size))





        
        
