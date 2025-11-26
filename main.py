import pygame
from map import Map
from renderer import Renderer
from cursor import Cursor
from gui import GUI

class Engine:
    def __init__(self):

        pygame.init()
        ################# Window Dimensions ####################
        self.screen_width = 1024
        self.screen_height = 1024
        self.size = (self.screen_width, self.screen_height)
        self.display_screen = pygame.display.set_mode(self.size) 
        pygame.display.set_caption("RPGRTS")
        ########################################################

        ################# Game Screen Window ###################
        self.game_screen_width = 400
        self.game_screen_height = 312
        self.screen = pygame.Surface((self.game_screen_width,self.game_screen_height))
        self.game_screen_ratio = (self.game_screen_height/self.game_screen_width)


        self.game_window_width = self.screen_width
        self.game_window_height = self.screen_height * self.game_screen_ratio
        ########################################################

        self.renderer = Renderer(self)
        

        ##################### Map Initiation ####################
        self.map_width = self.game_screen_width//self.renderer.tile_size
        self.map_height = self.game_screen_height//self.renderer.tile_size
        self.map = Map(width=self.map_width, height=self.map_height)
        ########################################################

        self.cursor = Cursor(self,self.map)

        self.GUI = GUI(self.display_screen, 
                       0, 
                       self.game_window_height, 
                       self.screen_width, 
                       self.screen_height-self.game_window_height)

        self.show_zoomin = False
        self.tick_rate = 100
        self.done = False 
        self.should_generate_new_world = False
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(0)

    def handle_events(self):
        keys = pygame.key.get_pressed()
        
        # self.handle_pressed(keys=keys)
        self.cursor.handle_pressed(keys)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            self.cursor.handle_input(event, keys)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.done = True


    def run(self):
        while not self.done:
            self.screen.fill((0,0,0))
            self.display_screen.fill((0,0,0))

            # --- Main event loop
            self.handle_events()

            if not self.show_zoomin:
                self.renderer.draw_map(self.map.map_data)
            else:
                self.renderer.draw_map(self.map.region_data)

            self.renderer.draw_cursor(self.cursor)

            scaled = pygame.transform.scale(self.screen, (self.game_window_width,self.game_window_height))
            self.display_screen.blit(scaled,(0,0))

            self.GUI.draw_text(5,5,f"Cursor: {self.cursor.position[0]+self.map.world_offset_x, self.cursor.position[1]+self.map.world_offset_y}")
            self.GUI.draw_text(5,5+32,f"Size: {self.cursor.size}")
            if self.show_zoomin:
                tile = self.map.region_data[self.cursor.position[1]][self.cursor.position[0]]
                self.GUI.draw_text(5,5+64,f"Tile height: {round(tile.tile_height,2)} tile type: {tile.tile_type.name}")
            # A cursor size of 10x10 on a map resolution of 50x50, means 1 world tile sampled equals 50/10 = 5 blocks.
            # So Resx = resolution on x axis.
            #    Ss = SampleSize
            #    (Resx/Ss, Resy/Ss)
            # So Wx * (Resx/Ss) + RegionX 
            # So Wy * (Resy/Ss) + RegionY

            # So a region tile placed at 7,2 would then be Rx % (Resy/Ss) = 2. tile offset. Rx // (Resy/Ss) = Wx
            # So then that tile would be at Wx, and within that tile it would be at xoffset 2


            pygame.display.flip()
            self.clock.tick(self.tick_rate)
        # Close the window and quit.
        print("Goodbye!")
        pygame.quit()


if __name__ == "__main__":
    game = Engine()
    game.run()