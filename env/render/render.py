import pygame, sys, random, os, subprocess
from .card_wrapper import *
from ..card import *
from ..sun import *
from .player import *
from .settings import *


class Render:
  

    def __init__(self) -> None:
         # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE_STRING)
        self.players = [Player(player_num=i) for i in range(4)] # Create all four players
        self.game_ended=False
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(GAME_FONT, 36)
        self.card_to_cardwrapper_map = {}  # Map card to card wrapper
        self.cardwrapper_to_card_map = {}
        self.game_running = True


    def render_cards(self) -> None:
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
            if player_num in [0,2]:
                card_width = card.card_surf.get_width()
                card_height = card.card_surf.get_height()
            else:
                card_height = card.card_surf.get_width()
                card_width = card.card_surf.get_height()
            
            if player_num == 0:
                x = screen_width // 2 - card_width//2  #- card_width - card_height 
                y = screen_height//2 + card_width//2  # 50 is a margin from the bottom
                self.display_surface.blit(card.card_surf, (x, y))
            elif player_num == 1:
                x = screen_width//2 + card_width//2 # 50 is a margin from the right
                y = screen_height // 2 - card_width//2
                self.display_surface.blit(card.card_surf, (x, y))
            elif player_num == 2:
                x = screen_width // 2 - card_width//2 
                y = screen_height//2 - card_height - card_width//2  # 50 is a margin from the top
                self.display_surface.blit(card.card_surf, (x, y))
            else:
                x = screen_width//2 - card_height -  card_width//2   # 50 is a margin from the left
                y = screen_height // 2 - card_width//2
                self.display_surface.blit(card.card_surf, (x, y))


    def map_cards(self, hand: list[Card]) -> None:
        """
        Converts cards data class to our card class and ensures the same object is referenced in both hands and rounds.
        """
        
        # Convert hands and store the mapping
        for card in hand:
            original_card = card
            if original_card not in self.card_to_cardwrapper_map:
                card_wrapper = CardWrapper(original_card.rank, original_card.suit)
                self.card_to_cardwrapper_map[original_card] = card_wrapper
                self.cardwrapper_to_card_map[card_wrapper] = original_card        


    def unwrap_card(self, card: CardWrapper) -> Card:
        """
        Converts CardWrapper object to Card object
        """
        return self.cardwrapper_to_card_map[card]


    def wrap_round(self, round: list[Card]) -> None:
        """
        Wraps the cards in round
        """
        for i in range(len(round)):
            round[i] = self.wrap_card(round[i])


    def wrap_card(self, card: Card) -> CardWrapper:
        """
        Converts Card object to CardWrapper object
        """
        return self.card_to_cardwrapper_map[card]


    def deal_hands(self, hands: list) -> None:
        """
        Deals the hand to each player
        """
        for player, hand in zip(self.players, hands):
            self.map_cards(hand) 
            player.receive_hand([self.wrap_card(card) for card in hand])


    def render_scores(self, scores) -> None:
        """
        Renders the scores for Team 1 and Team 2 at the top right of the screen.
        """
        team1_score_text = f"Team 1: {scores[0]:>4}"
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


    def visualize(self, game_info: dict, record: bool = False):
        """
        game_info (dict): Contains all information about how the game was played
        game_info.rounds (list of lists): Every card played per round in chronological order
        game_info.player (list): Player who starts the round
        game_info.player_hands (list of lists): List containing initial hands of all players
        """

        current_score = [0, 0]
        player_hands = game_info['player_hands']
        start_player_idx = game_info['players']
        rounds = game_info['rounds']
        scores = game_info['scores']

        if record:
            if not os.path.exists('frames'):
                os.makedirs('frames')
            frame_count = 0

        self.deal_hands(player_hands)
        

        clock = pygame.time.Clock()
        
        while self.game_running:
            self.screen.fill(BG_COLOR)  # Clear screen with background color
            self.render_cards()
            self.render_scores(current_score)
            pygame.display.update()  # Update the full display Surface to the screen
            clock.tick(1)
            self.game_start = False

            if record:
                pygame.image.save(self.screen, f'frames/frame_{frame_count:04d}.png')
                frame_count += 1
            for round, current_player_idx, score in zip(rounds, start_player_idx, scores):
                self.wrap_round(round)
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
                    
                    if record: 
                        # Save the frame
                        pygame.image.save(self.screen, f'frames/frame_{frame_count:04d}.png')
                        frame_count += 1
                    current_player_idx = (current_player_idx + 1) % 4

                    clock.tick(1)  # Wait for 1 second (adjust based on desired delay)
                current_score = score
                # self.render_scores(score)
                pygame.event.pump()

            clock.tick(60)  # Cap the frame rate at 60 FPS
            pygame.quit()
            self.game_running = False

    # def record_game(self, game_info: dict):
    #     """
    #     game_info (dict): Contains all information about how the game was played
    #     game_info.rounds (list of lists): Every card played per round in chronological order
    #     game_info.player (list): Player who starts the round
    #     game_info.player_hands (list of lists): List containing initial hands of all players
    #     """

    #     current_score = [0, 0]
    #     player_hands = game_info['player_hands']
    #     start_player_idx = game_info['players']
    #     rounds = game_info['rounds']
    #     scores = game_info['scores']

    #     self.deal_hands(player_hands)

    #     clock = pygame.time.Clock()
        
    #     # Create a directory to store frames
    #     if not os.path.exists('frames'):
    #         os.makedirs('frames')
        
    #     frame_count = 0

    #     while self.game_running:
    #         self.screen.fill(BG_COLOR)  # Clear screen with background color
    #         self.render_cards()
    #         self.render_scores(current_score)
    #         pygame.display.update()  # Update the full display Surface to the screen
            
    #         # Save the frame
    #         pygame.image.save(self.screen, f'frames/frame_{frame_count:04d}.png')
    #         frame_count += 1
            
    #         clock.tick(1)
    #         self.game_start = False

    #         for round, current_player_idx, score in zip(rounds, start_player_idx, scores):
    #             self.wrap_round(round)
    #             cards_played = []  # Cards that are played per round
    #             for card in round:
    #                 player = self.players[current_player_idx]

    #                 # Checks if card exists in the current player's hand
    #                 if card not in player.hand:
    #                     raise ValueError(f'Card does not exist in player\'s hand "{card.id}".')

    #                 player.played_card(card)
    #                 cards_played.append((card, current_player_idx))

    #                 self.screen.fill(BG_COLOR)  # Clear screen with background color
    #                 self.render_played_card(cards_played)
    #                 self.render_cards()
    #                 self.render_scores(current_score)
    #                 pygame.display.update()

    #                 # Save the frame
    #                 pygame.image.save(self.screen, f'frames/frame_{frame_count:04d}.png')
    #                 frame_count += 1

    #                 current_player_idx = (current_player_idx + 1) % 4

    #                 clock.tick(1)  # Wait for 1 second (adjust based on desired delay)
    #             current_score = score
    #             pygame.event.pump()

    #         clock.tick(60)  # Cap the frame rate at 60 FPS
    #         pygame.quit()
    #         self.game_running = False

    #     print(f"Total frames captured: {frame_count}")
    def run_game(self, sun_game: Sun) -> None:
        """
        sun_game (Sun): Sun game that we can interact with
        """
        # First player to play
        current_player_idx = sun_game.next_player
        player = self.players[current_player_idx]

        player_hands = sun_game.player_hands
        score = sun_game.score
        self.deal_hands(player_hands) 
        clock = pygame.time.Clock()
        
        while self.game_running:
            self.screen.fill(BG_COLOR)  # Clear screen with background color
            # self.render_input_box()
            self.render_cards()
            self.render_scores(score)
            pygame.display.update()  # Update the full display Surface to the screen
            clock.tick(1)
            self.game_start=False

                
            
            for round in range(8):
                cards_played = []  # Cards that are played per round
                for plays in range(4):
                    card_idx = int(input(f' Player {current_player_idx}: Enter card index to play: '))
                    card = player.hand[card_idx]
                    # Checks if card exists in the current player's hand
                    if card not in player.hand:
                        raise ValueError(f'Card does not exist in player\'s hand "{card.id}".')

                    unwrapped_card = self.unwrap_card(card) # Map back to Card
                    # Play card and append to cards played                        
                    player.played_card(card)
                    cards_played.append((card, current_player_idx))
                    
                    # Play card in sun game
                    current_player_idx = sun_game.play(unwrapped_card)
                    player = self.players[current_player_idx]

                    # Render after play
                    self.screen.fill(BG_COLOR)  # Clear screen with background color
                    self.render_played_card(cards_played)
                    self.render_cards()
                    self.render_scores(score)
                    pygame.display.update()

                    clock.tick(1)  # Wait for 1 second (adjust based on desired delay)

            clock.tick(60)  # Cap the frame rate at 60 FPS
            self.game_running = False

    def create_video(self, frame_rate=1, output_filename="game_recording.mp4"):
        """
        Create a video from the saved frames.
        
        :param frame_rate: Frames per second for the output video (default: 1)
        :param output_filename: Name of the output video file (default: "game_recording.mp4")
        """
        frames_dir = 'frames'
        
        if not os.path.exists(frames_dir):
            print(f"Error: {frames_dir} directory not found.")
            return
        
        try:
            ffmpeg_command = [
                'ffmpeg',
                '-framerate', str(frame_rate),
                '-i', f'{frames_dir}/frame_%04d.png',
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                output_filename
            ]
            
            subprocess.run(ffmpeg_command, check=True)
            print(f"Video created successfully: {output_filename}")
            
            # Optionally, remove the frames after creating the video
            for file in os.listdir(frames_dir):
                os.remove(os.path.join(frames_dir, file))
            os.rmdir(frames_dir)
            print("Frames directory cleaned up.")
            
        except subprocess.CalledProcessError as e:
            print(f"Error creating video: {e}")
        except FileNotFoundError:
            print("Error: FFmpeg not found. Please ensure FFmpeg is installed and accessible in your system PATH.")

if __name__ == '__main__':
    game = Render()
    sun_game = Sun()
    game_info = {
        'rounds': [[sun_game.player_hands[j][i] for j in range(4)] for i in range(8)], # Cards that were played.
        'players': [0] * 8,
        'player_hands': sun_game.player_hands, # The intial hands that were dealth.
        'scores': [[1*i, 2*i] for i in range(1, 9)]
    }
    game.visualize(game_info, record=True)
    game.create_video()
    # game.run_game(sun_game)