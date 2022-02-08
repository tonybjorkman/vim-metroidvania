import pygame 
import random
import spritesheet
import math
import numpy as np


class Player:

    def __init__(self, fonts):
        self.x = 350
        self.y = 0
        self.sprites = fonts
        self.sprite_x = 0
        self.sprite_y = 0
        self.sprite = None
        self.update_sprite()
        self.direction = 1
     
    def move(self, x, y):
        self.x += x
        self.y += y
        if x>0 and self.direction == 0:
            self.direction = 1
        elif x<0 and self.direction == 1:
            self.direction = 0

        self.move_sprite_wrap_x(1)

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
    

class SpriteSheet:

    def __init__(self,file,tilepxsize,numitems,spacing=0,alpha=-1) -> None:
        self.sheet = spritesheet.spritesheet(file)
        self.images = self.sheet.load_matrix([0, 1, tilepxsize[0], tilepxsize[1]],numitems,alpha,0)

    def get_char(self, char):
        code = ord(char)
        if code < 32 or code > 126:
            code = 32
        return code
    
    # convert between ascii and font sprite
    def ascii_to_index(self, ascii):
        if ascii == '':
            ascii = ' '
        a = ord(ascii)
        index = self.get_char(ascii) - 32
        y = math.floor(index/15)
        x = index%15
        return (x,y)
    
    def get_char_image(self, char):
        index = self.ascii_to_index(char)
        return self.images[index[1]][index[0]]

class Map:

    def __init__(self,size):
        self.resize(size[0],size[1])
        self.scroll = 0
    
    def resize(self, width, height):
        self.map = np.chararray((width,height))
        self.map[:] = ' '

    #load strings from file and load into chararray 
    def load_map(self,file):
        lines = []
        with open(file) as f:
            for line in f:
                lines.append(line) 
        
        # find the longest line
        max_width = 0
        for line in lines:
            if len(line) > max_width:
                max_width = len(line)
        height = len(lines)

        # resize the map
        self.resize(max_width, height)
        # load the map into the chararray
        for y in range(height):
            for x in range(max_width):
                if x < len(lines[y]):
                    self.map[x][y] = lines[y][x]
                else:
                    self.map[x][y] = ' '

    def char_set(self):
        chrlist = ['i','u','n','e','d','w','b','o','y','p','d','G','$','*','^']
        return chrlist     

    def spawn_random_map(self, density=0.1):
        #self.resize(width, height)
        for x in range(self.map.shape[0]):
            for y in range(self.map.shape[1]):
                if random.random() < density/4:
                    self.map[x][y] = random.choice(self.char_set())
                elif random.random() < density:
                    self.map[x][y] = '#'
                else:
                    self.map[x][y] = ' '

        self.scroll = 0

class TileScreen:
    def __init__(self,pixsize,map,tilesize=20) -> None:
        self.pixsize = pixsize
        self.tilesize = tilesize
        self.size = tuple((np.array(pixsize)/tilesize).astype(int))
        self.map = map 
        self.scroll = 0

    def draw_visible_map(self, screen, sprites):
        tile_scroll = math.ceil(self.scroll/self.tilesize)
        for scrn_x,x in enumerate(range(tile_scroll,self.size[0]+1+tile_scroll)):
            for scrn_y,y in enumerate(range(self.size[1])):
                screen.blit(sprites.get_char_image(self.get_map_char(x,y)),(scrn_x*20,scrn_y*20))

    def update_scroll(self, player_xpos, player_dir):
        padding=32
        leftborder = self.scroll + padding
        rightborder = self.pixsize[0] - padding
        print("scroll:"+str(self.scroll) + "player:"+str(player_xpos))
        if player_dir == 1 and player_xpos > rightborder:
            self.scroll = player_xpos - rightborder
        elif player_dir == 0 and player_xpos < leftborder:
            self.scroll = player_xpos - padding
 

    def get_map_char(self,x,y):
        if x < 0 or y < 0 or x >= self.map.map.shape[0] or y >= self.map.map.shape[1]:
            return ' '
        return self.map.map[x][y]


        

pygame.init()
pygame.key.set_repeat(1,100)
pass

# define the colours
white = (255, 255, 255)

calpha = (101, 32, 91, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

# set the Dimensions
width = 420 
height = 240
map = Map((24,12))
map.load_map('map.txt')
#map.spawn_random_map()
tile_screen = TileScreen((width,height),map)
# size of a block

# set Screen
screen = pygame.display.set_mode((width, height))

font_sprites = SpriteSheet('fonts.png',(20, 20),(15,8),alpha=calpha)
player_sprites = SpriteSheet('player.png',(32,64),(10,10))

images = player_sprites.images
player = Player(images)

# set caption
pygame.display.set_caption("CORONA SCARPER")
pygame.display.update()

# set icon
running = True

while running:
    # set the image on screen object
    screen.fill(black)
    screen.blit(font_sprites.get_char_image('x'), (50, 50))
    screen.blit(font_sprites.get_char_image('h'), (70, 50))
    screen.blit(font_sprites.get_char_image(')'), (90, 50))
    tile_screen.draw_visible_map(screen, font_sprites)
    # loop through all events
    for event in pygame.event.get():
            
        # check the quit condition
        if event.type == pygame.QUIT:
            # quit the game
            pygame.quit()

        # movement key control of player
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT:
                player.move(4,0)
                

            if event.key == pygame.K_LEFT:
                player.move(-4,0)


            if event.key == pygame.K_UP:
                player.move(0,-4)
            
            if event.key == pygame.K_DOWN:
                player.move(0,4)
            
            tile_screen.update_scroll(player.x,player.direction)

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                pass

        screen.blit(player.sprite, (player.x - tile_screen.scroll, player.y))
        pygame.display.update()    