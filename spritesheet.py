
import pygame

class spritesheet(object):
    def __init__(self, filename):
            self.sheet = pygame.image.load(filename).convert()
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey,spacing):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3]-spacing)
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def load_matrix(self,rect, image_count, colorkey = None,spacing = 0):
        "Loads a multiple strips of images and returns them as a list"
        images = []
        ypos = rect[1]
        for y in range(image_count[1]):
            rect[1] = ypos+y*rect[3]
            images.append(self.load_strip(rect,image_count[0],colorkey,spacing))
        return images            
