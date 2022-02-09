import pygame 
from pygame import sprite
import random
import spritesheet
import math
import numpy as np
from characters import Character

class Player(sprite.Sprite):

    def __init__(self, fonts):
        sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(350,0,32,64)
        self.dx = 0
        self.dy = 0
        self.sprites = fonts
        self.sprite_x = 0
        self.sprite_y = 0
        self.image = None
        self.direction = 1
        self.update_sprite()
     
    def move(self, x, y):
        self.dx += x
        self.dy += y
        if self.dx>0 and self.direction == 0:
            self.direction = 1
        elif self.dx<0 and self.direction == 1:
            self.direction = 0

        self.move_sprite_wrap_x(1)



        # move the player
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.dx = 0
        self.dy = 0

    def update_sprite(self):
        img = self.sprites[self.sprite_y][self.sprite_x]
        if self.direction == 0:
            img = pygame.transform.flip(img,True,False) 
        self.image = img 

    #wraparound for sprites
    def move_sprite_wrap_x(self, num):
        self.sprite_x += num
        if self.sprite_x < 1:
            self.sprite_x = 6
        if self.sprite_x > 6:
            self.sprite_x = 1
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

class MapFactory:
    def __init__(self) -> None:
        pass    
    
    def create_char_map(self,file,spritesheet):
        map = Map((1,1))
        map.load_map(file)
        #iterate through map and create sprites
        obj_array = np.empty((map.map.shape[0],map.map.shape[1]),dtype=Character)
        for y in range(map.map.shape[1]):
            for x in range(map.map.shape[0]):
                c = Character(map.map[x][y], pygame.Rect((x*20,y*20),(20,20)))
                c.image = spritesheet.get_char_image(c.type)
                obj_array[x][y] = c
        map.map = obj_array
        return map



class Map:

    def __init__(self,size):
        self.resize(size[0],size[1])
        self.scroll = 0
        self.obj_map = None
    
    def resize(self, width, height):
        self.map = np.empty((width,height),dtype=str)
        self.map[:] = ' '

    #load strings from file and load into chararray 
    def load_map(self,file):
        lines = []
        with open(file) as f:
            for line in f:
                lines.append(line) 
        
        # size
        max_width = 0
        for line in lines:
            if len(line) > max_width:
                max_width = len(line)
        height = len(lines)
        self.resize(max_width, height)

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
    
    def get_chars_from_map(self,char):
        chars = []
        for x in range(self.map.shape[0]):
            for y in range(self.map.shape[1]):
                if self.map[x][y].type == char:
                    chars.append(self.map[x][y])
        return chars

class TileScreen:

    def __init__(self,pixsize,map,tilesize=20) -> None:
        self.pixsize = pixsize
        self.tilesize = tilesize
        self.size = tuple((np.array(pixsize)/tilesize).astype(int))
        self.map = map 
        self.scroll = 0

    def draw_visible_map(self, screen, map):
        tile_scroll = math.ceil(self.scroll/self.tilesize)
        for x in range(map.map.shape[0]):
            for y in range(map.map.shape[1]):
                screen.blit(map.map[x][y].image,(x*self.tilesize-self.scroll,y*self.tilesize))

    def update_scroll(self, player_xpos, player_dir):
        padding=32
        leftborder = self.scroll + padding
        rightborder = self.scroll + self.pixsize[0] - padding
        #print("scroll:"+str(self.scroll) + "player:"+str(player_xpos))
        if player_dir == 1 and player_xpos > rightborder:
            self.scroll += player_xpos - rightborder 
        elif player_dir == 0 and player_xpos < leftborder:
            self.scroll = player_xpos - padding
 

    #def get_map_char(self,x,y):
     #   if x < 0 or y < 0 or x >= self.map.map.shape[0] or y >= self.map.map.shape[1]:
      #      return ' '
       # return self.map.map[x][y]

pygame.init()
pygame.key.set_repeat(1,50)

# define the colours
white = (255, 255, 255)
calpha = (101, 32, 91, 255)
black = (0, 0, 0)

# set the Dimensions
width = 420 
height = 240

# size of a block

# set Screen
screen = pygame.display.set_mode((width, height))

font_sprites = SpriteSheet('fonts.png',(20, 20),(15,8),alpha=calpha)
player_sprites = SpriteSheet('player.png',(32,64),(10,10))
map = MapFactory().create_char_map('map.txt',font_sprites)
#map.spawn_random_map()
tile_screen = TileScreen((width,height),map)
images = player_sprites.images
player = Player(images)

wgroup = pygame.sprite.Group()
ws = map.get_chars_from_map('w')
wgroup.add(ws)
# set caption
pygame.display.set_caption("Vim Game")
pygame.display.update()

# set icon
running = True

while running:
    # set the image on screen object
    screen.fill(black)
    colliding_x = font_sprites.get_char_image('x')
    screen.blit(colliding_x, (50, 50))
    screen.blit(font_sprites.get_char_image('h'), (70, 50))
    screen.blit(font_sprites.get_char_image(')'), (90, 50))
    tile_screen.draw_visible_map(screen, map)
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
            
            tile_screen.update_scroll(player.rect.x,player.direction)
            #check collision
            if pygame.sprite.spritecollideany(player,wgroup):
                print("collision")
                

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                pass
        
        

        screen.blit(player.image, (player.rect.x - tile_screen.scroll, player.rect.y))
        pygame.display.update()    