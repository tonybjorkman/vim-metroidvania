from pygame import sprite
from typing import List
import pygame

class World:
    def __init__(self, name):
        pass

class WordFinder:
    def __init__(self, wordlist):
        self.wordlist = wordlist

    def find_next_word_forward(self,startpos):
        ''' w vim operator'''
        return None
class Word:
    '''
    May contain subwords
    hello.this('are_subwords')
    1    23   4 5           6
    '''

    def __init__(self,startpos,subwords=None):
        self.subwords = []
    
    def add_subword(self, subword):
        self.subwords.append(subword)
    
    def get_subword(self,index):
        return self.subwords[index]
    
    def draw(self, screen):
        for character in self.characters:
            character.draw(screen)

class SubWord():
    '''
    Consists of characters, either all alphanumerical 
    or all special characters
    '''
    def __init__(self, characters):
        self.subword = []

    def get_first_character(self):
        return self.subword[0] 

class Character(sprite.Sprite):
    def __init__(self, type, rect):
        sprite.Sprite.__init__(self)
        self.name = ""
        self.rect = rect 
        self.color = [255, 255, 255]
        self.type = type
        self.image = None
        
    def is_alphanumeric(self):
        if (ord(self.type) >= ord('a') and ord(self.type) <= ord('z')) \
            or (ord(self.type) >= ord('A') and ord(self.type) <= ord('Z')) \
            or (ord(self.type) >= ord('0') and ord(self.type) <= ord('9')) \
            or ord(self.type) == ord('_'):
            return True
        else:
            return False

    def draw(self, screen):
        pass

class Monster(Character):
    def __init__(self, type, rect):
        Character.__init__(self, type, rect)
        self.name = "monster"
        self.health = 100
        self.speed = 1

class WordListFactory:
    def __init__(self):
        self.words = []

    def append_word_from_chars(self, startpos, characters):
        subwords = self._chars_into_subwords(characters)
        self.words.append(Word(startpos,subwords))
    
    def _chars_into_subwords(self, characters):
        ''' splits by transitions between alphanumeric and special characters '''
        if characters is None or []:
            return None
        alphanumeric = characters[0].is_alphanumeric()
        chars_in_subword = []
        subwords = []
        for c in characters:
            if alphanumeric == c.is_alphanumeric():
                chars_in_subword.append(c)
            else:
                alphanumeric == c.is_alphanumeric()
                subwords.append(SubWord(chars_in_subword))
                chars_in_subword = []
        if len(chars_in_subword) > 0:
            subwords.append(SubWord(chars_in_subword))
        return subwords 
        
