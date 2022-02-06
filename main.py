import pygame 
import random
import spritesheet
import math

class Player:

    def __init__(self, fonts):
        self.x = 0
        self.y = 0
        self.sprites = fonts
        self.sprite_x = 0
        self.sprite_y = 0
        self.sprite = None
        self.update_sprite()
     
    def move(self, x, y):
        self.x += x
        self.y += y

    def update_sprite(self):
        self.sprite = self.sprites[self.sprite_y][self.sprite_x]

    #wraparound for sprites
    def move_sprite_wrap_x(self, num):
        self.sprite_x += num
        if self.sprite_x < 0:
            self.sprite_x = len(self.sprites[1])-1
        if self.sprite_x > len(self.sprites[1])-1:
            self.sprite_x = 0
        self.update_sprite()
    
    def move_sprite_wrap_y(self, num):
        self.sprite_y += num
        if self.sprite_y < 0:
            self.sprite_y = len(self.sprites)-1
        if self.sprite_y > len(self.sprites)-1:
            self.sprite_y = 0
        self.update_sprite()
    

class FontSpriteSheet:

    def __init__(self) -> None:
        self.sheet = spritesheet.spritesheet('fonts.png')
        self.images = self.sheet.load_matrix([0, 0, 20, 20],(15,8), -1)

    def get_char(self, char):
        code = ord(char)
        if code < 32 or code > 126:
            code = 32
        return code
    
    # convert between ascii and font sprite
    def ascii_to_index(self, ascii):
        a = ord(ascii)
        index = self.get_char(ascii) - 32
        y = math.floor(index/15)
        x = index%15
        return (x,y)
    
    def get_char_image(self, char):
        index = self.ascii_to_index(char)
        return self.images[index[1]][index[0]]

class Map:
    def __init__(self) -> None:
        self.map = [[chr(32+i+(x*15)) for i in range(15)] for x in range(8)] 

    def draw(self, screen, sprites):
        for y in range(8):
            for x in range(15):
                screen.blit(sprites.get_char_image(self.map[y][x]),(x*20,y*20))



pygame.init()

m = Map()
pass

# define the colours
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

# set the Dimensions
width = 300 
height = 400

# size of a block
pixel = 64

# set Screen
screen = pygame.display.set_mode((width, height))

ss = FontSpriteSheet()
# Sprite is 16x16 pixels at location 0,0 in the file...

images = ss.images
player = Player(images)



# set caption
pygame.display.set_caption("CORONA SCARPER")
#font = pygame.font.SysFont('DejaVuSansMono', 32)
#text = font.render('GeeksForGeeks', True, white, black)
# load the image
gameIcon = pygame.image.load("car.jpg")# create a rectangular object for the
# text surface object
#textRect = text.get_rect()
 
# set the center of the rectangular object.
#textRect.center = (height // 2, width // 2)
    # copying the text surface object
    # to the display surface object
    # at the center coordinate.
#screen.blit(text, textRect)
pygame.display.update()

# set icon
pygame.display.set_icon(gameIcon)
backgroundImg = pygame.image.load("back.jpg")
running = True

while running:
    # set the image on screen object
    screen.blit(backgroundImg, (0, 0))

    screen.blit(ss.get_char_image('x'), (50, 50))
    screen.blit(ss.get_char_image('h'), (70, 50))
    screen.blit(ss.get_char_image(')'), (90, 50))
    m.draw(screen, ss)
    # loop through all events
    for event in pygame.event.get():
            
        # check the quit condition
        if event.type == pygame.QUIT:
            # quit the game
            pygame.quit()

        # movement key control of player
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT:
                player.move_sprite_wrap_x(1)

            if event.key == pygame.K_LEFT:
                player.move_sprite_wrap_x(-1)

            if event.key == pygame.K_UP:
                player.move_sprite_wrap_y(-1)
            
            if event.key == pygame.K_DOWN:
                player.move_sprite_wrap_y(1)

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                pass

        screen.blit(player.sprite, (player.x, player.y))
        pygame.display.update()    