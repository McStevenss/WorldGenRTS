import pygame
from map import Map
class Cursor:
    def __init__(self, engine, map: Map):
        self.engine = engine
        self.map = map
        self.position = [self.map.width//2,self.map.height//2]
        self.local_position = [self.map.width//2,self.map.height//2]
        self.size = 6
        self.should_generate_new_world = False

        self.max_world_offset = 50

    def handle_pressed(self,keys):
        if keys[pygame.K_LEFT]:
            if self.map.world_offset_x > -self.max_world_offset:
                self.map.world_offset_x = self.map.world_offset_x - 1
                self.should_generate_new_world = True
    
        if keys[pygame.K_RIGHT]:
            if  self.map.world_offset_x < self.max_world_offset:
                self.map.world_offset_x = self.map.world_offset_x + 1
                self.should_generate_new_world = True

        if keys[pygame.K_UP]:
            if self.map.world_offset_y > -self.max_world_offset:
                self.map.world_offset_y = self.map.world_offset_y - 1
                self.should_generate_new_world = True

        if keys[pygame.K_DOWN]:
            if  self.map.world_offset_y < self.max_world_offset:
                self.map.world_offset_y = self.map.world_offset_y + 1
                self.should_generate_new_world = True

        if self.should_generate_new_world:

            self.map.map_data = self.map.generate_world()
            self.should_generate_new_world = False
  

    def handle_input(self, event, keys):

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w and keys[pygame.K_w]:
                if self.position[1] > 0: 
                    self.position[1] +=-1

            if event.key == pygame.K_s and keys[pygame.K_s]:
                if self.position[1] + self.size < self.map.height:
                    self.position[1] +=1

            if event.key == pygame.K_a and keys[pygame.K_a]:
                if self.position[0] > 0:
                    self.position[0] +=-1

            if event.key == pygame.K_d and keys[pygame.K_d]:
                if self.position[0] + self.size < self.map.width:
                    self.position[0] +=1


            if event.key == pygame.K_k and keys[pygame.K_k]:
                    self.size = self.size + 1
                
            if event.key == pygame.K_j and keys[pygame.K_j]:
                if self.size <= 1:
                    self.size = 1
                else:
                    self.size = self.size - 1

            if event.key == pygame.K_b and keys[pygame.K_b]:
                if self.map.scale > 1:
                    self.map.scale = self.map.scale -1
                if self.map.octaves > 5:
                    self.map.octaves = self.map.octaves - 1
                self.map.map_data = self.map.generate_world()

            if event.key == pygame.K_n and keys[pygame.K_n]:
                self.map.scale = self.map.scale +1
                self.map.octaves = self.map.octaves + 1

                self.map.map_data = self.map.generate_world()


        
            if event.key == pygame.K_RETURN and keys[pygame.K_RETURN]:
                if not self.engine.show_zoomin:
                    wx = self.position[0] + self.map.world_offset_x
                    wy = self.position[1] + self.map.world_offset_y
                    self.map.generate_region_at(wx,wy, resolution=(self.map.width,self.map.height), sample_size=self.size)
                    self.engine.show_zoomin = True
                    self.size=2

            if event.key == pygame.K_BACKSPACE and keys[pygame.K_BACKSPACE]:
                self.engine.show_zoomin = False
                self.size = 6
