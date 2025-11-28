import noise
from opensimplex import OpenSimplex
import numpy as np
from typing import List
from tile import Tile
# from config import TileIds, HEIGHT_MAPPING
from config import TileIds, HEIGHT_THRESHOLDS
import cv2
import random

BIOME_COLORS = {
    # "OCEAN": (0, 0, 240),
    # "SHALLOWS": (102,102,238),
    "OCEAN": (33, 122, 191),
    "SHALLOWS": (35,142,233),
    "BEACH": (239, 217, 106),


    "ROCK": (96,96,96),
    "DARK_ROCK": (86,86,86),
    "SNOW": (255, 255, 255),
    "FOREST": (0,153,0),

    "TEMPERATE_DESERT": (230, 205, 44),
    "TAIGA": (78, 115, 69),

    # "GRASSLAND": (100, 250, 125),
    "GRASSLAND": (75, 196, 95),
    "TEMPERATE_DECIDUOUS_FOREST": (45, 138, 54),
    "TEMPERATE_RAIN_FOREST": (104, 196, 108),

    "SUBTROPICAL_DESERT": (225, 178, 84),
    "TROPICAL_SEASONAL_FOREST": (47, 171, 29),
    "TROPICAL_RAIN_FOREST": (79, 189, 127),
}


class NoiseData:
    def __init__(self, noise, width, height, octaves, persistence, lacunarity, scale, seed, is_normalized):
        self.noise = noise
        self.width = width
        self.height = height
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.scale = scale
        self.seed = seed
        self.is_normalized = is_normalized

    def save_as_image(self,path):
        cv2.imwrite(path, self.noise*255.0)

class Biome:
    
    @staticmethod
    def SolveBiome(x, y, moisture_map:NoiseData, elevation_map:NoiseData):
        e = elevation_map.noise[y][x]
        m = moisture_map.noise[y][x]

        if e < 0.1: return "OCEAN"
        if e < 0.2: return "SHALLOWS"
        if e < 0.25: return "BEACH"


        if e > 0.85:
            return "SNOW"
        if e > 0.75:
            return "DARK_ROCK"
        if e > 0.65:
            return "ROCK"
        
        if e > 0.6:
            if m < 0.33: return "TEMPERATE_DESERT"
            if m < 0.77: return "FOREST"
            return "TAIGA"
        
        if e > 0.3:
            if m < 0.16: return "TEMPERATE_DESERT"
            if m < 0.50: return "GRASSLAND"
            if m < 0.83: return "TEMPERATE_DECIDUOUS_FOREST"
            return "TEMPERATE_RAIN_FOREST"
        
        if m < 0.16: return "SUBTROPICAL_DESERT"
        if m < 0.33: return "GRASSLAND"
        if m < 0.66: return "TROPICAL_SEASONAL_FOREST"

        return "TROPICAL_RAIN_FOREST"


class Map:
    def __init__(self, width=50, height=50, seed=42):

        self.width = width
        self.height = height
        self.scale = 55.0       # Larger → smoother terrain
        self.octaves = 5        # More octaves → more detail
        self.persistence = 0.4   # Amplitude of octaves
        self.lacunarity = 4.5    # Frequency of octaves
        self.seed = seed

        
        # self.gen = OpenSimplex(seed=self.seed)
        self.gen = OpenSimplex(seed=random.randint(0,10000))
        self.falloff_exponent = 3

        self.world_offset_x = 0
        self.world_offset_y = 0

        self.global_min = None
        self.global_max = None
        self.get_global_min_max = True
        self.falloff_map = self.generate_square_falloff_map(self.width,self.height,exponent=3)

        self.elevation_map = None
        self.moisture_map = None

        self.equator = 0.0
        self.poles = 1.0

        self.__generate_noisemaps()


    def noise(self,nx, ny):
        # Rescale from -1.0:+1.0 to 0.0:1.0
        # return (self.gen.noise2(nx, ny) / 2.0) + 0.5
        return self.gen.noise2(nx, ny)

    def __generate_noisemaps(self):
        
        world_seed = random.randint(0,10000)
        self.gen = OpenSimplex(seed=world_seed)

        self.elevation_map = self.generate_noise(self.width,self.height,self.octaves,self.persistence,self.lacunarity,self.scale,seed=world_seed)
        self.elevation_map.noise = np.clip(self.elevation_map.noise - self.falloff_map, 0, 1)
        print(f"[Map] Done generating elevation map!")
        # self.elevation_map.noise = np.power(self.elevation_map.noise, 1.20)
          
        moisture_seed = random.randint(0,10000)
        self.gen = OpenSimplex(seed=moisture_seed)
        self.moisture_map = self.generate_noise(self.width,self.height,self.octaves,self.persistence,self.lacunarity,self.scale, seed=moisture_seed)
        print(f"[Map] Done generating moisture smap!")



    def generate_noise(self, width, height, octaves, persistence, lacunarity, scale, seed, normalized=True) -> NoiseData:
        noise_map = np.zeros((self.height, self.width))
        
        for y in range(self.height):
            for x in range(self.width):

                nx = x / scale
                ny = y / scale 

                e = ((1 * self.noise(1 * nx, 1 * ny)) +
                     (0.5 * self.noise(2 * nx, 2 * ny)) + 
                     (0.25 * self.noise(4 * nx, 4 * ny)) + 
                    (0.125 * self.noise(8 * nx, 8 * ny))
                    )
                noise_map[y][x] =  e / (1 + 0.5 + 0.25 + 0.125)


        noise_map = (noise_map - noise_map.min()) / (noise_map.max() - noise_map.min())

        return NoiseData(noise_map, width, height, octaves, persistence, lacunarity, scale, seed, normalized)
    


    def export_biome_image(self, path="biomes.png"):
        img = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        emax = self.elevation_map.noise.max()
        emin = self.elevation_map.noise.min()
        for y in range(self.height):
            for x in range(self.width):
                biome = Biome.SolveBiome(
                    x, y,
                    self.moisture_map,
                    self.elevation_map
                )
                e = self.elevation_map.noise[y][x]
                # color = BIOME_COLORS.get(biome, (255, 0, 255))  # fallback magenta
                base_color = np.array(BIOME_COLORS.get(biome, (255, 0, 255)), dtype=np.float32)
                if (base_color[0],base_color[1],base_color[2]) == (255, 0, 255):
                    print("found nothing for elevation:",e, "biome ", biome)
                # Apply shading
                if biome == "OCEAN":
                    # Deep ocean darker, shallow ocean lighter
                    shade = 0.55 + (e * 0.45)     # 0.55 → 1.0
                    # shade = (1.0 * 1-e) + emin 
                    # shade = (emin)
                else:
                    # Land shading
                    # shade = 0.60 + (e * 0.40)     # 0.60 → 1.0
                    shade = max(0,min(0.2+e,1))     # 0.60 → 1.0
                    # shade = (1.0+ emax) * e 

                shaded_color = np.clip(base_color * shade, 0, 255)
                # img[y, x] = shaded_color
                img[y, x] = base_color

                # img[y, x] = color

        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(path, img)
        print(f"[Map][ExportBiomeImage] Biome map saved to {path}")


    def generate_square_falloff_map(self, width, height, exponent=3):
        """
        Generate a square falloff map for island/world edges.
        exponent: controls how sharp the falloff is (higher = sharper edges)
        """
        # Create normalized coordinates from -1 to 1
        x = np.linspace(-1, 1, width)
        y = np.linspace(-1, 1, height)
        xv, yv = np.meshgrid(x, y)
        
        # Square falloff: distance = max(|x|, |y|)
        distance = np.maximum(np.abs(xv), np.abs(yv))
        
        # Apply falloff curve
        falloff = np.clip(distance**exponent, 0, 1)
        
        return falloff
   


if __name__ == "__main__":

    map = Map(512,512,42)
    
    map.elevation_map.save_as_image("debug_images/elevation.png")
    map.moisture_map.save_as_image("debug_images/moisture.png")

    map.export_biome_image("debug_images/biomes.png")
