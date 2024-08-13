import pygame
rotate_dict = {
    0:0,
    1:90,
    2:180,
    3:270
}
class Player():
    """
    A player will be associated with his hand
    """
    def __init__(self, player_num):
        self.hand = []
        self.player_num=player_num
        self.played_cards = []
        

    def draw_hand(self, rot=None):
        """
        Visualizes the hand of player
        """
        blit_pos = (0,0)
        for card in self.hand:
            card.draw_card(rot=rotate_dict[self.player_num])

    
    
    def print_hand(self):
        """
        Prints hand of player
        """
        print([card.id for card in self.hand])

    
    def receive_hand(self, hand):
        """
        Player receives his initial hand
        """
        self.hand = hand
        self.draw_hand() # Visualize the hand
        
    
    def played_card(self, card):
        """
        
        """
        self.played_cards.append(card)
        self.hand.remove(card)
