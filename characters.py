from pygame import sprite

class World:
    def __init__(self, name):
        pass

class Word:
    def __init__(self, characters):
        self.characters = characters
    
    def draw(self, screen):
        for character in self.characters:
            character.draw(screen)

class Character(sprite.Sprite):
    def __init__(self, type, rect):
        sprite.Sprite.__init__(self)
        self.name = ""
        self.rect = rect 
        self.color = [255, 255, 255]
        self.type = type
        self.image = None
        
    
    def draw(self, screen):
        pass
