from texture_loader import TextureLoader 
from tile import Tile
from config import TileIds
from cursor import Cursor
from typing import List
import cv2
import numpy as np
import pygame
import sys

class Renderer:
    def __init__(self, engine):
        self.engine = engine
        self.screen = self.engine.screen
        self.tile_size = 8
        self.texture_loader = TextureLoader(self.tile_size,"TinyRTS_v06.png")


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
            TL = self.texture_loader.get_tile(TileIds.CURSOR.value)
            TR = self.texture_loader.get_tile(TileIds.CURSOR.value)
            BL = self.texture_loader.get_tile(TileIds.CURSOR.value)
            BR = self.texture_loader.get_tile(TileIds.CURSOR.value)

            self.screen.blit(TL, (x*self.tile_size,y*self.tile_size))
            self.screen.blit(TR, ((x+size-1)*self.tile_size,y*self.tile_size))
            self.screen.blit(BL, (x*self.tile_size,(y+size-1)*self.tile_size))
            self.screen.blit(BR, ((x+size-1)*self.tile_size,(y+size-1)*self.tile_size))


    def surface_to_array(self, surface: pygame.Surface) -> np.ndarray:
        """Convert a Pygame surface to a NumPy array in RGB format."""
        return pygame.surfarray.array3d(surface).transpose(1, 0, 2)  # Pygame uses (width, height)

    def draw_map_to_image(self, map_data: List[List['Tile']]) -> np.ndarray:
        """
        Draws the tile map onto an image array.

        :param map_data: 2D list of Tile objects
        :param tile_size: size of each tile in pixels
        :param texture_loader: object with get_tile(tile_type) returning an image (numpy array)
        :return: NumPy array representing the final image
        """
        height = len(map_data) * self.tile_size
        width = len(map_data[0]) * self.tile_size
        img = np.zeros((height, width, 3), dtype=np.uint8)

        for row in map_data:
            for tile in row:
                x, y = tile.position
                tile_type = tile.tile_type
                texture = self.texture_loader.get_tile(tile_type.value)  # should be a NumPy array (HxWx3)
                texture = self.surface_to_array(texture)
                # Resize texture if needed
                if texture.shape[0] != self.tile_size or texture.shape[1] != self.tile_size:
                    texture = cv2.resize(texture, (self.tile_size, self.tile_size), interpolation=cv2.INTER_NEAREST)
                
                # Compute pixel coordinates
                px, py = x * self.tile_size, y * self.tile_size
                
                # Place texture onto the image
                img[py:py+self.tile_size, px:px+self.tile_size] = texture

        print("tile size",sys.getsizeof(map_data[10][10]))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite("textured_image.png", img)




        
        
