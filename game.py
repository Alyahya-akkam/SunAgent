from card_wrapper import CardWrapper
import time
from sun_logic.card import *
from sun_logic.sun import *
from player import Player, rotate_dict
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
        self.game_ended=False
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(GAME_FONT, 36)

    def render_cards(self):
        card_spacing = 100  # Adjust this value to control the spacing between cards
        screen_width = WIDTH
        screen_height = HEIGHT
        card_spacing = 75  # Adjust this value to control the spacing between cards

        for player in self.players:
            counter = 0
            
            if player.player_num == 0:
                # Player 1: South, cards should be centered at the bottom
                for card in player.hand:
                    x = screen_width // 2 - (len(player.hand) * card_spacing) // 2 + counter * card_spacing
                    y = screen_height - card.card_surf.get_height() - 50  # 50 is a margin from the bottom
                    card.save_position((x, y))
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


    def render_played_card(self, cards_played: list):
        card_pos = [-112.5, -37.5, 37.5, 112.5]
        card_spacing = 50
        center_width = WIDTH/2
        center_height = HEIGHT/2
        screen_width = WIDTH
        screen_height = HEIGHT
        for i, card_tuple in enumerate(cards_played):
            card, player_num = card_tuple
            card.draw_card(rot=rotate_dict[player_num])
            if player_num == 0:
                x = screen_width // 2 - card_spacing 
                y = screen_height - card.card_surf.get_height() * 2.5 - screen_width//4  # 50 is a margin from the bottom
                self.display_surface.blit(card.card_surf, (x, y))
            elif player_num == 1:
                x = screen_width - card.card_surf.get_width() * 2.5 - screen_width//2.5  # 50 is a margin from the right
                y = screen_height // 2 - card_spacing
                self.display_surface.blit(card.card_surf, (x, y))
            elif player_num == 2:
                x = screen_width // 2 - card_spacing
                y = card.card_surf.get_height() * 2.5 + 50  # 50 is a margin from the top
                self.display_surface.blit(card.card_surf, (x, y))
            else:
                x = card.card_surf.get_width() * 2.5 + 50  # 50 is a margin from the left
                y = screen_height // 2 - card_spacing
                self.display_surface.blit(card.card_surf, (x, y))

    def convert_cards(self, hands, rounds):
        """
        Converts cards data class to our card class and ensures the same object is referenced in both hands and rounds.
        """
        card_map = {}  # Map to store the mapping from original card to CardWrapper
        
        # Convert hands and store the mapping
        for hand in hands:
            for i in range(len(hand)):
                original_card = hand[i]
                if original_card not in card_map:
                    card_map[original_card] = CardWrapper(original_card.rank, original_card.suit)
                hand[i] = card_map[original_card]

        # Convert rounds using the same mapping
        for round in rounds:
            for i in range(len(round)):
                original_card = round[i]
                round[i] = card_map[original_card]

    
    def deal_hands(self, hands: list):
        """
        Deals the hand to each player
        """
        for player, hand in zip(self.players, hands):
            player.give_hand(hand)


    def render_scores(self, scores):
        """
        Renders the scores for Team 1 and Team 2 at the top right of the screen.
        """
        team1_score_text = f"Team 1:{'':>1} {scores[0]:>4}"
        team2_score_text = f"Team 2: {scores[1]:>4}"

        # Render the text
        team1_score_surface = self.font.render(team1_score_text, True, (255, 255, 255))  # White color
        team2_score_surface = self.font.render(team2_score_text, True, (255, 255, 255))

        # Calculate positions
        screen_width = WIDTH
        margin = 20  # Margin from the top and right edges
        team1_pos = (screen_width - team1_score_surface.get_width() - margin, margin)
        team2_pos = (screen_width - team2_score_surface.get_width() - margin, margin + team1_score_surface.get_height())

        # Blit the text surfaces onto the screen
        self.display_surface.blit(team1_score_surface, team1_pos)
        self.display_surface.blit(team2_score_surface, team2_pos)



    def run(self, game_info: dict):
        """
        game_info (dict): Contains all information about how the game was played
        game_info.rounds (list of lists): Every card played per round in chronological order
        game_info.player (list): Player who starts the round
        game_info.player_hands (list of lists): List containing initial hands of all players
        """

        current_score = [0, 0]
        self.convert_cards(game_info['player_hands'], game_info['rounds'])
        self.deal_hands(game_info['player_hands'])

        clock = pygame.time.Clock()
        delay_ms = 1000  # Delay in milliseconds (1000 ms = 1 second)
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            self.screen.fill(BG_COLOR)  # Clear screen with background color
            self.render_cards()
            self.render_scores(current_score)
            pygame.display.update()  # Update the full display Surface to the screen
            clock.tick(1)
            if not self.game_ended:
                for round, current_player_idx, score in zip(game_info['rounds'], game_info['players'], game_info['scores']):
                    cards_played = []  # Cards that are played per round
                    for card in round:
                        player = self.players[current_player_idx]

                        # Checks if card exists in the current player's hand
                        if card not in player.hand:
                            raise ValueError(f'Card does not exist in player\'s hand "{card.id}".')

                        player.played_card(card)
                        cards_played.append((card, current_player_idx))

                        self.screen.fill(BG_COLOR)  # Clear screen with background color
                        self.render_played_card(cards_played)
                        self.render_cards()
                        self.render_scores(current_score)
                        pygame.display.update()

                        current_player_idx = (current_player_idx + 1) % 4

                        clock.tick(1)  # Wait for 1 second (adjust based on desired delay)
                        player.print_cards()
                        print()
                    current_score = score
                    # self.render_scores(score)
                    pygame.event.pump()
                self.game_ended = True

            clock.tick(60)  # Cap the frame rate at 60 FPS

if __name__ == '__main__':
    game = Game()
    sun_game = Sun()
    game_info = {
        'rounds': [[sun_game.player_hands[j][i] for j in range(4)] for i in range(8)], # Cards that were played.
        'players': [0] * 8,
        'player_hands': sun_game.player_hands, # The intial hands that were dealth.
        'scores': [[1*i, 2*i] for i in range(1, 9)]
    }
    game.run(game_info)

