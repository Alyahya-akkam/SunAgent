import pygame, random
from collections import namedtuple
from ..card import *
from .settings import *

CardTuple = namedtuple('Card', ['value', 'suit'])



class CardWrapper:
    """
    A class to represent each card

    card_value (str): Represents the value of the card. E.g: ('Q': Queen)
    card_suite (str): Represents the suite of the card. E.g: Heart
    """
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.animation_start_time = pygame.time.get_ticks()
        self.animation_complete = False
        self.uuid = None
        self.position = None
        self.start_position = (800, 500)
        self.current_position = None
        self.orig_position = self.start_position
        self.card_img = None
        self.card_bounding_rect = None
        self.card_surf = None
        self.data = CardTuple(rank, suit)
        self.id = f"{self.data.value}{self.data.suit}"
        self.img = f"./graphics/cards/{self.id}.png"

        
    def save_position(self, pos):
        self.current_position = pos

    def draw_card(self, rot):
        # self.card_rotation_angle s= random.uniform(-3, 3)
        self.card_img = pygame.image.load(self.img)
        self.card_img = pygame.transform.scale(self.card_img, (self.card_img.get_width() *1.1 , self.card_img.get_height() *1.1 ))
        self.card_rot = pygame.transform.rotate(self.card_img, rot)
        self.card_bounding_rect = self.card_rot.get_bounding_rect()
        self.card_surf = pygame.Surface(self.card_bounding_rect.size, pygame.SRCALPHA)
        
        # Calculate the position to blit the rotated image onto the surface
        blit_pos = (0, 0)
        self.card_surf.blit(self.card_rot, blit_pos)

        # Random y value for card
        self.card_y = (P1_C1[1] - self.card_surf.get_height() // 2) + random.randint(-20, 20)

    def __eq__(self, other):
        if isinstance(other, CardWrapper):
            return self.id == other.id
        return False
    
    def __hash__(self):
        return hash((self.rank, self.suit))

