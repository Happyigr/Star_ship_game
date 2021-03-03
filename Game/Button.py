import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Button():
    def __init__(self, color, x, y, width, height, text='', text_size=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_size = text_size

    def draw(self, surf, outline=None):
        if outline:
            pygame.draw.rect(surf, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        pygame.draw.rect(surf, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.text_size)
            text = font.render(self.text, 1, (0, 0, 0))
            surf.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y +
                             (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


class Button_img():

    def __init__(self, img, x, y, text='', text_size=None):
        self.image = img
        #  self.image.set_colorkey(WHITE) and self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.text = text
        self.text_size = text_size

    def draw(self, surf):
        surf.blit(self.image, (self.x, self.y))

        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.text_size)
            text = font.render(self.text, 1, (0, 0, 0))
            surf.blit(text, (self.x + (self.rect.width/2 - text.get_width()/2), self.y +
                             (self.rect.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.rect.width:
            if self.y < pos[1] < self.y + self.rect.height:
                return True

        return False
