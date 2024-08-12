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
        

    def rotate_cards(self):
        blit_pos = (0,0)
        # self.card_surf.blit(self.card_rot, blit_pos)
        # self.hands = [card.card_surf.blit(pygame.transform.rotate(card.card_img, rotate_dict[self.player_num]), blit_pos) for card in self.hand]
        # self.hands = []
        for card in self.hand:
            card.draw_card(rot=rotate_dict[self.player_num])
            # self.hands.append(card)
        # self.hands = [card.card_rotation_angle for card in self.hand]
    def print_cards(self):
        print([card.id for card in self.hand])

    def give_hand(self, hand):
        self.hand = hand
        self.rotate_cards()
        
    def choose_card(self, card):
        self.hand.remove(card)
        
    def play_card(self, card_value):

        pass