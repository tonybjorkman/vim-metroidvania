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
        self.rect = pygame.Rect(350,0,18,50)
        self.speed_y =0
        self.speed_x = 0
        self.dx = 0
        self.dy = 0
        self.sprites = fonts
        self.sprite_x = 0
        self.sprite_y = 0
        self.image = None
        self.image_xoffset = 6
        self.update_sprite_direction(1)
        self.on_ground = False
        self.run_active = False        
     
    
    
    def run(self, direction):
        print("run direction: ", direction)
        if self.on_ground and self.speed_x < 3 and direction == 1:
            self.speed_x += 1 * direction
        elif self.on_ground and self.speed_x > -3 and direction == -1:
            self.speed_x += 1 * direction
        elif not self.on_ground and self.speed_x < 3 and direction == 1:
            self.speed_x += 1 * direction
        elif not self.on_ground and self.speed_x > -3 and direction == -1:
            self.speed_x += 1 * direction

        player.run_active = True        
        self.move_sprite_wrap_x(direction)

    def update_sprite_direction(self,dir):
        img = self.sprites[self.sprite_y][self.sprite_x]
        if dir == -1:
            img = pygame.transform.flip(img,True,False) 
        self.image = img 

    #wraparound for sprites
    def move_sprite_wrap_x(self, num):
        self.sprite_x += num
        if self.sprite_x < 1:
            self.sprite_x = 6
        if self.sprite_x > 6:
            self.sprite_x = 1
        self.update_sprite_direction(num)
    
    def move_sprite_wrap_y(self, num):
        self.sprite_y += num
        if self.sprite_y < 0:
            self.sprite_y = len(self.sprites)-1
        if self.sprite_y > len(self.sprites)-1:
            self.sprite_y = 0
        self.update_sprite_direction(num)
    
    def jump(self):
        if self.on_ground:
            print("jumped on grouund")
            self.speed_y = -10
    



class WorldUtility:

    def gravity(self, player, objects):
        if player.speed_y < 5:
            player.speed_y += 1
    
    def friction(self,player):
        if not player.run_active and player.on_ground:
            player.speed_x = 0
        

    def run_full_frame(self, player, objects):
        #apply world speeds
        current_move = [0,0]
        #print (player.speed_x)
        self.gravity(player, objects)
        self.friction(player)
        self.friction(player)
        player.dx += round(player.speed_x)
        player.dy += round(player.speed_y)


        dir_x = -1 if player.dx < 0 else 1
        dir_y = -1 if player.dy < 0 else 1
        player.on_ground = False
        while (player.dx != 0 or player.dy != 0):
            
            if abs(player.dx) > 1:
                current_move[0] = 1*dir_x
                player.dx -= 1*dir_x
            elif abs(player.dx) <= 1 and player.dx != 0:
                current_move[0] = player.dx
                player.dx = 0

            player.rect.x += current_move[0]
            if pygame.sprite.spritecollideany(player, objects):
                player.rect.x -= current_move[0]
                player.speed_x = 0
                player.dx = 0
                current_move[0] = 0

            if abs(player.dy) > 1:
                current_move[1] = 1*dir_y
                player.dy -= 1*dir_y
            elif abs(player.dy) <= 1 and player.dy != 0: 
                current_move[1] = player.dy
                player.dy = 0 

            player.rect.y += current_move[1]
            if pygame.sprite.spritecollideany(player, objects):
                player.rect.y -= current_move[1]
                player.speed_y = 0
                player.dy = 0
                if current_move[1] > 0:
                    player.on_ground = True
                current_move[1] = 0
        

        player.run_active = False
        

    def collision_detection(self, player, objects):
        #check collision

        on_ground = False 

        collider = pygame.sprite.spritecollide(player, objects,dokill=False)
        for obj in collider:                        
            #object is below player
            print("collision with " + obj.type)

            if player.rect.bottom >= obj.rect.top and player.rect.bottomright[0] > obj.rect.topleft[0]:
                #player.rect.bottom = obj.rect.top 
                if player.speed_y > 0:
                    player.speed_y = 0
                on_ground = True
                #decrease player speed
                if player.speed_x > 0:
                    player.speed_x -= 0.5
                elif player.speed_x < 0:    
                    player.speed_x += 0.5
                print ("on ground")
            #object is above player
            elif False and player.rect.y < obj.rect.bottom:
                player.rect.top = obj.rect.bottom
                player.speed_y = 0
            #object is to the right of player   
            elif player.rect.right >= obj.rect.left:   
                print("right")
                player.rect.right = obj.rect.left
                if player.speed_x > 0:
                    player.speed_x = 0
            #object is to the left of player
            elif False and player.rect.x + player.rect.width < obj.rect.x:
                player.rect.left = obj.rect.right
                player.speed_x = 0

        player.on_ground = on_ground


class SpriteSheet:

    def __init__(self,file,tilepxsize,numitems,offset=(0,1),spacing=0,alpha=-1) -> None:
        self.sheet = spritesheet.spritesheet(file)
        self.images = self.sheet.load_matrix([offset[0], offset[1], tilepxsize[0], tilepxsize[1]],numitems,alpha,0)

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
        map = ASCIIMap((1,1))
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

class ObjectMap:
    ''' ObjectMap is the  '''

class ASCIIMap:

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
                if self.map[x][y].type in char:
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

    def update_scroll(self, player_xpos ):
        padding=32
        leftborder = self.scroll + padding
        rightborder = self.scroll + self.pixsize[0] - padding
        #print("scroll:"+str(self.scroll) + "player:"+str(player_xpos))
        if player_xpos > rightborder:
            self.scroll += player_xpos - rightborder 
        elif player_xpos < leftborder:
            self.scroll = player_xpos - padding
 

    #def get_map_char(self,x,y):
     #   if x < 0 or y < 0 or x >= self.map.map.shape[0] or y >= self.map.map.shape[1]:
      #      return ' '
       # return self.map.map[x][y]

pygame.init()
pygame.key.set_repeat(1,50)

# define the colours
white = (255, 255, 255)
red = (255, 0, 0)
calpha = (101, 32, 91, 255)
black = (0, 0, 0)

# set the Dimensions
width = 420 
height = 240

# size of a block

# set Screen
screen = pygame.display.set_mode((width, height))

font_sprites = SpriteSheet('fonts.png',(20, 20),(15,8),(0,1),alpha=calpha)
player_sprites = SpriteSheet('player.png',(32,50),(10,10),(0,15))
map = MapFactory().create_char_map('map.txt',font_sprites)
#map.spawn_random_map()
tile_screen = TileScreen((width,height),map)
images = player_sprites.images
player = Player(images)

wgroup = pygame.sprite.Group()
ws = map.get_chars_from_map([chr(x) for x in range(33,120)])
wgroup.add(ws)
# set caption
pygame.display.set_caption("Vim Game")
pygame.display.update()

world = WorldUtility()

# set icon
running = True

while running:
    clock = pygame.time.Clock()
    clock.tick(20)
    # set the image on screen object
    screen.fill(black)
    screen.blit(font_sprites.get_char_image('X'), (90, 50))
    tile_screen.draw_visible_map(screen, map)
    # loop through all events
    
    key = pygame.key.get_pressed()
    movement_released = True
    # check the quit condition

    # movement key control of player

    if key[pygame.K_RIGHT]:
        player.run(1)
        movement_released = False

    if key[pygame.K_LEFT]:
        player.run(-1)
        movement_released = False

    if key[pygame.K_UP]:
        player.jump()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    try:
       pygame.event.pump()
    except:
        #fail silently if game is closed
        pass

    tile_screen.update_scroll(player.rect.x)
    world.run_full_frame(player,wgroup)
    
    pygame.display.set_caption("Vim Game:"+str(player.on_ground))
    #draw rectangle
    pygame.draw.rect(screen, red, (player.rect.x - tile_screen.scroll, player.rect.y, player.rect.width, player.rect.height),1)
    screen.blit(player.image, (player.rect.x - tile_screen.scroll - player.image_xoffset, player.rect.y))
    pygame.display.update()    