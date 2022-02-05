import pygame 
import random
import spritesheet


class Player:
    def __init__(self, sprites):
        self.x = 0
        self.y = 0
        self.sprites = sprites
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


pygame.init()

# define the colours
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

# set the Dimensions
width = 290 
height = 405

# size of a block
pixel = 64

# set Screen
screen = pygame.display.set_mode((width, height))

ss = spritesheet.spritesheet('fonts.png')
# Sprite is 16x16 pixels at location 0,0 in the file...
images = ss.load_matrix([0, 20, 20, 20],(15,2), -1)

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