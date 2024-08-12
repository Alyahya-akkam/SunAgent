from collections import namedtuple
from settings import *
import pygame, random
CardTuple = namedtuple('Card', ['value', 'suit'])

# List containing all card values in baloot
card_values = [7, 8, 9, 
               10, # Ten
               11, # Jack
               12, # Queen
               13, # King
               1, # Ace
]

# List containing all suit types
card_suits = ['C', # Clubs
              'D', # Diamonds
              'H', # Hearts
              'S', # Spades
            ]


class Card():
    """
    A class to represent each card

    card_value (str): Represents the value of the card. E.g: ('Q': Queen)
    card_suite (str): Represents the suite of the card. E.g: Heart
    """
    def __init__(self, card_value, card_suit):
        self.animation_start_time = pygame.time.get_ticks()
        self.animation_complete = False
        self.uuid = None
        self.position = None
        self.start_position = (800, 500)
        self.orig_position = self.start_position

        self.data = CardTuple(card_value, card_suit)
        self.id = f"{self.data.value}{self.data.suit}"
        self.img = r"C:\Users\scc\Projects\Baloot Agent project\RL part"+f"\Cards\Cards\{self.id}.png"

        
    def draw_card(self, rot):
        # self.card_rotation_angle s= random.uniform(-3, 3)
        self.card_img = pygame.image.load(self.img)
        self.card_img = pygame.transform.scale(self.card_img, (self.card_img.get_width() *1.5 , self.card_img.get_height() *1.5 ))
        self.card_rot = pygame.transform.rotate(self.card_img, rot)
        self.card_bounding_rect = self.card_rot.get_bounding_rect()
        self.card_surf = pygame.Surface(self.card_bounding_rect.size, pygame.SRCALPHA)
        
        # Calculate the position to blit the rotated image onto the surface
        blit_pos = (0, 0)
        self.card_surf.blit(self.card_rot, blit_pos)

        # Random y value for card
        self.card_y = (P1_C1[1] - self.card_surf.get_height() // 2) + random.randint(-20, 20)

