from sun_logic.card import Card, ranks, suits
import random
# from typing import List, Tuple

### NOTE: DONT FORGET THE 10 POINTS FOR THE أرض!!!!!!!!!!!!!
class Sun:
    deck: list[Card] = [Card(rank, suit) for rank in ranks for suit in suits]
    # i don't think there is a better way to do this
    player_hands: list[list[Card]] = [[], [], [], []] # 0 and 2 are a team, 1 and 3 are the other team
    # from now on team 0 (p0 and p2) and team 1 (p1 and p3) will be used
    score: list[int] # team 0, team 1
    next_player: int # indicates which player is expected to play next
    cards_played: list[Card] # keeps track of cards played this round
    rounds_played: int # keeps track of rounds played so far
    # NOTE: currently the user has to start a new game if the rounds are over, playing after rounds are done will raise an error.

    # this feels weird, i think it's actually fine, still feels weird
    def __init__(self) -> None:
        """Creates the object and sets-up a new game."""
        self.new_game()

    def new_game(self, seed: int | None =None) -> None:
        """
        Sets up a new game.

        Resets scores, shuffles deck and deals cards to players, resets `next_player`, `cards_played`, and `rounds_played`.

        `seed`: Used for reproducability. If given will be used to shuffle deck and deal cards. Default: None
        """
        # reset score
        self.score = [0, 0]
        # use seed if given
        if seed:
            random.seed(seed)
        random.shuffle(self.deck)

        # distribute cards
        # (I know this is weird i just didn't want to copy paste like a pleb)
        for i in range(4):
            self.player_hands[i] = self.deck[8*i : 8*(i+1)]

        # reset next_player and round_counter to 0
        self.next_player = 0
        self.cards_played = []
        self.rounds_played = 0

    def end_round(self) -> None:
        """Updates `score` and `round_played`, clears `cards_played`, and determines who plays first next round."""
        self.rounds_played += 1

        first_suit = self.cards_played[0].suit

        # this is a bit of a mess
        # it just iterates over the cards played, while keeping a pointer to whoever played that card
        # and determines who played the strongest card of the appropraite suit
        # while it does that it also sums up the round points

        ### START OF MESSY BIT
        # assume first player and first card are strongest
        strong_player = self.next_player # since the round is over, this points to the player who played first
        strong_card = self.cards_played[0]
        # points for the round
        round_points = 0
        # pointer to player who played the card in the loop
        player_ptr = self.next_player
        for card in self.cards_played:
            # if the card matches the suit and is the strongest so far
            round_points += card.points
            if card.suit == first_suit and card.points > strong_card.points:
                strong_player = player_ptr
                strong_card = card
            player_ptr = (player_ptr + 1) % 4
        ### END OF MESSY BIT
            
        # if this was the last round, add 10 to the round points.
        # (it's baloot rules, the last round has 10 extra points)
        if self.rounds_played == 8:
            round_points += 10
        
        # update score
        if strong_player in [0, 2]:
            self.score[0] = self.score[0] + round_points
        else:
            self.score[1] = self.score[1] + round_points

        # set the next player to be the strong player
        self.next_player = strong_player

        # clear cards_played
        self.cards_played.clear()

    def play(self, card: Card) -> int:
        """
        Plays a card for `next_player`. Checks that `next_player` has the card, and plays it. If round ends calls `end_round`.

        `card`: A `Card` object. The card intended to be played by `next_player`

        Returns: ID of the next_player. (You can use this or ignore it up to you.)
        """
        if card not in self.player_hands[self.next_player]:
            raise ValueError(f"Player {self.next_player}, who was expeceted to play, they do not have the card {card}.")
        
        self.player_hands[self.next_player].remove(card)
        self.cards_played.append(card)
        self.next_player = (self.next_player + 1) % 4 # if the round is over, this points to the player who played first

        # if the round is over, call end_round
        if len(self.cards_played) == 4:
            self.end_round()

        return self.next_player

