from cards import Card, card_suits, card_values
from player import Player
import random
import pygame
import sys
from settings import *
class Game:
  
    def __init__(self):
         # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE_STRING)
        self.players = [Player(player_num=i) for i in range(4)] # Create all four players
        self.deck = self.generate_deck() 
        self.played_cards = []
        self.deal_hands()
        self.current_player_index = random.randint(0,3)
        self.rounds_played=[]
        self.display_surface = pygame.display.get_surface()

    def render_cards(self):
        card_spacing = 100  # Adjust this value to control the spacing between cards


        screen_width = WIDTH
        screen_height = HEIGHT
        card_spacing = 100  # Adjust this value to control the spacing between cards

        for player in self.players:
            counter = 0
            
            if player.player_num == 0:
                # Player 1: South, cards should be centered at the bottom
                for card in player.hand:
                    x = screen_width // 2 - (len(player.hand) * card_spacing) // 2 + counter * card_spacing
                    y = screen_height - card.card_surf.get_height() - 50  # 50 is a margin from the bottom
                    self.display_surface.blit(card.card_surf, (x, y))
                    counter += 1

            elif player.player_num == 1:
                # Player 2: East, cards should be centered on the right
                for card in player.hand:
                    x = screen_width - card.card_surf.get_width() - 50  # 50 is a margin from the right
                    y = screen_height // 2 - (len(player.hand) * card_spacing) // 2 + counter * card_spacing
                    self.display_surface.blit(card.card_surf, (x, y))
                    counter += 1

            elif player.player_num == 2:
                # Player 3: North, cards should be centered at the top
                for card in player.hand:
                    x = screen_width // 2 - (len(player.hand) * card_spacing) // 2 + counter * card_spacing
                    y = 50  # 50 is a margin from the top
                    self.display_surface.blit(card.card_surf, (x, y))
                    counter += 1

            elif player.player_num == 3:
                # Player 4: West, cards should be centered on the left
                for card in player.hand:
                    x = 50  # 50 is a margin from the left
                    y = screen_height // 2 - (len(player.hand) * card_spacing) // 2 + counter * card_spacing
                    self.display_surface.blit(card.card_surf, (x, y))
                    counter += 1



    def generate_deck(self):
        deck = []
        for suit in card_suits:
            for value in card_values:
                deck.append(Card(value, suit))
        random.shuffle(deck)
        return deck
    
    def deal_hands(self):
        hands = [self.deck[:8], self.deck[8:16], self.deck[16:24], self.deck[24:32]]
        for player, hand in zip(self.players, hands):
            player.give_hand(hand)
        print(self.players[0].print_cards())


    
    def player_turn(self, card_idx):
        '''
        players[current_player_index]
        1st play the card add it to played cards
        2nd choose the card (basically pop it out)
        3rd update the current player index

        Find whose turn it is
        card_played = True / False

        '''
        player = self.players[self.current_player_index]
        card = player.cards[card_idx]
        self.played_cards.apppend(card)
        player.choose_card(card)    
        # if len(self.played_cards) % 4 == 0:
        #     self.rounds_played.append(self.played_cards)
        #     self.played_cards = []

        
        pass

    

    def run(self):
        """
        [
        begining_hand_of_all_players,
        cards_played,
        scores
        ]
        
        [current_player, hand_of_all_players, card_played, round_ended, game_ended, team_1_score, team_2_score, ]
        Current_player: index (0-3)[] (int)
        hand_of_all_players: list_of_cards [] #(it should be disscused with SAID BOWSER)#
        card_played: card index (int)
        round_ended: boolean flag (bool)
        game_ended: boolean flag (bool)
        team_1_score: (int)
        team_2_score: (int)

        [
        [AH, 8H, 7H, 10H]
        ]
        """
        # rounds = [0, 10, 12, '9H', 'AH', 'KH', '10H']
        # pygame.init()
        # pygame.display.set_caption('San!')

        # for round in rounds:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # print('are we here?')
                    pygame.quit()
                    sys.exit()

            # for cards_played in round:
                
            pygame.display.update()
            self.screen.fill(BG_COLOR)
            self.render_cards()

        #     # Check if all 8 rounds were completed
        #     if self.round_ended:
        #         """
        #         1. Animation that round ended.
        #         2. Remove all cards from board
        #         3. Update Score
        #         """
        #         pass
        #     if self.game_ended:
        #         """
        #         1. Animation showing team won and final score
        #         2. Close game
        #         """
        #         break
            
        #     """
        #     1. Find what card is played
        #     2. Transfer card from hand to board
        #     """


        #     # self.player_turn(card_idx=5)
        #     self.current_player_index = (self.current_player_index + 1) % 4 

if __name__ == '__main__':
    game = Game()
    
    game.run()