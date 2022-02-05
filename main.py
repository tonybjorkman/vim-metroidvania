import pygame 
import random
import spritesheet

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
#images = [] 

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

# load the image
backgroundImg = pygame.image.load("back.jpg")

imagenum=0
playerImage = images[0] #pygame.image.load("fly.png")

def next_image(step):
    global playerImage, imagenum
    imagenum+=step
    if imagenum > len(images)-1:
        imagenum = 0
    elif imagenum < 0:
        imagenum = len(images)-1

    playerImage = images[imagenum] #pygame.image.load("fly.png")

# set the position
playerXPosition = (width/2) - (pixel/2)

# So that the player will be
# at height of 20 above the base
playerYPosition = height - pixel - 10	

# set initially 0
playerXPositionChange = 0

# define a function for setting
# the image at particular
# coordinates
def player(x, y):
# paste image on screen object
    screen.blit(playerImage, (x, y))

# load the image
blockImage = pygame.image.load("skull.png")

# set the random position
blockXPosition = random.randint(0,
								(width - pixel))

blockYPosition = 0 - pixel

# set the speed of
# the block
blockXPositionChange = 0
blockYPositionChange = 2

# define a function for setting
# the image at particular
# coordinates
def block(x, y):
# paste image on screen object
    screen.blit(blockImage,
			(x, y))

# define a function for
# collision detection
def crash():
# take a global variable
    global blockYPosition
    print(str(blockYPosition))
    # check conditions
    if playerYPosition < (blockYPosition + pixel):

        if ((playerXPosition > blockXPosition
            and playerXPosition < (blockXPosition + pixel))
            or ((playerXPosition + pixel) > blockXPosition
            and (playerXPosition + pixel) < (blockXPosition + pixel))):

            blockYPosition = 0

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

                next_image(-1)
                playerXPositionChange = 3

            if event.key == pygame.K_LEFT:

                next_image(1)
                playerXPositionChange = -3

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_RIGHT or pygame.K_LEFT:

                playerXPositionChange = 0


        # Boundaries to the Player

        # if it comes at right end,
        # stay at right end and
        # does not exceed
        if playerXPosition >= (width - pixel):
            playerXPosition = (width - pixel)

        # if it comes at left end,
        # stay at left end and
        # does not exceed
        if playerXPosition <= 0:
            playerXPosition = 0

        # Multiple Blocks Movement after each other
        # and condition used because of game over function
        if (blockYPosition >= height - 0 and
            blockYPosition <= (height + 200)):
        
            blockYPosition = 0 - pixel

            # randomly assign value in range
            blockXPosition = random.randint(0, (width - pixel))
        
        
        # movement of Player
        playerXPosition += playerXPositionChange
        
        # movement of Block
        blockYPosition += blockYPositionChange
        
        # player Function Call
        player(playerXPosition, playerYPosition)
        
        # block Function Call
        block(blockXPosition, blockYPosition)
        
        # crash function call
        crash()
        
        # update screen
        pygame.display.update()    