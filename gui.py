import pygame




class GUI:
    def __init__(self, screen, x,y,width,height):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.heigth = height

        self.font = pygame.font.Font('freesansbold.ttf', 32)

        # self.texts

    def draw_text(self,x,y,text):
        white = (255, 255, 255)
        black = (0, 0, 0)

        text = self.font.render(text, True, white, black)
        textRect = text.get_rect()

        # set the center of the rectangular object.
        textRect.x = self.x + x
        textRect.y = self.y + y

        self.screen.blit(text, textRect)