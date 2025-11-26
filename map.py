import noise
import numpy as np
from typing import List
from tile import Tile
# from config import TileIds, HEIGHT_MAPPING
from config import TileIds, HEIGHT_THRESHOLDS




class Map:
    def __init__(self, width=50, height=50, seed=42):

        self.width = width
        self.height = height
        self.scale = 10.0         # Larger → smoother terrain
        # self.scale = 10.0       # Larger → smoother terrain
        self.octaves = 5        # More octaves → more detail
        # self.persistence = 0.5   # Amplitude of octaves
        self.persistence = 0.5   # Amplitude of octaves
        self.lacunarity = 4.0    # Frequency of octaves
        self.seed = seed


        self.world_offset_x = 0
        self.world_offset_y = 0

        self.global_min = None
        self.global_max = None
        self.get_global_min_max = True

        self.map_data = self.generate_world()
        
        self.region_data = None

    def generate_region_at(self,x,y, resolution=(200,200), sample_size = 1):
        self.region_data = self.generate_region(x,y,resolution, sample_size)
   
    def generate_falloff_map(self, width, height, exponent=3):
        """
        Generate a falloff map for island generation.
        exponent: controls how sharp the falloff is (higher = sharper edges)
        """
        # Create normalized coordinates from -1 to 1
        x = np.linspace(-1, 1, width)
        y = np.linspace(-1, 1, height)
        xv, yv = np.meshgrid(x, y)
        
        # Compute distance from center (0,0)
        distance = np.sqrt(xv**2 + yv**2)
        
        # Apply falloff curve
        falloff = np.clip(distance**exponent, 0, 1)
        
        return falloff

    def generate_world(self):
        world = np.zeros((self.height, self.width))
        
        for y in range(self.height):
            for x in range(self.width):
                world[y][x] = noise.pnoise2(
                    ((x + self.world_offset_x) / self.scale),
                    ((y + self.world_offset_y)/ self.scale),
                    octaves=self.octaves,
                    persistence=self.persistence,
                    lacunarity=self.lacunarity,
                    repeatx=1024,
                    repeaty=1024,
                    base=self.seed
                )
        
        if self.get_global_min_max:
            self.global_min = world.min()
            self.global_max = world.max()
            self.get_global_min_max = False

        
        # Normalize to 0–1
        world = (world - self.global_min) / (self.global_max - self.global_min)
        
        # This will add a falloff map around the viewed space, better to generate a noise texture probably and apply the falloff map to a bigger map we look around in.
        # Ex create a world of 1024x1024 or similar once and then apply the falloff map to that instead.
        falloff_map = self.generate_falloff_map(self.width,self.height,exponent=10)
        world = np.clip(world - falloff_map, 0, 1)

        map_data = self.process_generated_world(world)
        return map_data

 
    def generate_region(self, wx, wy, resolution=(200,200), sample_size=1):
        #Numpy handles resolution as y,x instead of x,y
        region = np.zeros((resolution[1],resolution[0]))
        
        # How much noise-space one world pixel covers
        noise_span = sample_size / self.scale

        for y in range(resolution[1]):
            for x in range(resolution[0]):

                nx = (wx / self.scale) + (x / resolution[0]) * noise_span
                ny = (wy / self.scale) + (y / resolution[1]) * noise_span

                region[y][x] = noise.pnoise2(
                    nx,
                    ny,
                    octaves=self.octaves+5,
                    persistence=self.persistence,
                    lacunarity=self.lacunarity,
                    repeatx=1024,
                    repeaty=1024,
                    base=self.seed
                )

        region = (region - self.global_min) / (self.global_max - self.global_min)
        region  = self.process_generated_world(region)
        return region


    def get_tile_type(self,value):
        for threshold, tile in HEIGHT_THRESHOLDS:
            if value <= threshold:
                return tile

   
    def process_generated_world(self, noise_data) -> List[List[Tile]]:
        map_data: List[List[Tile]] = []
        H,W = noise_data.shape
        for y in range(H):
            map_data.append([])
            for x in range(W):
                
                tile_height = noise_data[y][x]
                tilename = self.get_tile_type(tile_height)
                try:
                    tile = Tile((x,y), TileIds[tilename], tile_height)
                except:
                    print(f"Failed to get tile {x,y} with tilename '{tilename}' at tileheight {tile_height}")
                map_data[y].append(tile)

        return map_data
    
