import pygame

class TextureLoader:
    def __init__(self, spritesheet_tilesize = 8,tileset_path=None):
        self.texture_atlas = {}
        self.tile_size = spritesheet_tilesize

        self.tileset = {}
        self.tileset_texture = None
    
        self.load_tileset(path=tileset_path)


    
    def load_tileset(self,path,transparency_key=None):

        if transparency_key is None:
            tileset = pygame.image.load(path).convert_alpha()
        else:
            tileset = pygame.image.load(path).convert()
            tileset.set_colorkey(transparency_key)

        self.tileset_texture = tileset

        self.process_tileset()


    def process_tileset(self):

        tileset = self.tileset_texture
        tiles_per_row = tileset.get_width() // self.tile_size   
        tiles_per_column = tileset.get_height() // self.tile_size

        for y in range(tiles_per_column):
            for x in range(tiles_per_row):
                # print(x,y)
                tile_img = tileset.subsurface(pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size))
                self.tileset[(x,y)] = tile_img

    def get_tile(self, key):
        return self.tileset[key]
        
        
    
    def load_image(self, path):
        texture = pygame.image.load(path).convert_alpha()
        return texture