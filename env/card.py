from dataclasses import dataclass

ranks = ["7", "8", "9", "10", "J", "Q", "K", "A"]
suits = ["C", "D", "H", "S"]
rank_to_points = {
    "10": 10,
    "J": 2,
    "Q": 3,
    "K": 4,
    "A": 11,
}


@dataclass
class Card:
    rank: str
    suit: str

    def __init__(self, rank: str, suit: str) -> None:
        # input validation, just throw an error if the rank or suit are not in the predefined list
        # NOTE: it's all caps for now, idk if i should upper it, will leave as is for now
        if rank not in ranks:
            raise ValueError(f'Illegal rank "{rank}".')
        if suit not in suits:
            raise ValueError(f'Illegal suit "{suit}".')
        
        self.rank = rank
        self.suit = suit

        # if the card has points, give it the correct amount, else give it zero points
        if rank in rank_to_points:
            self.points = rank_to_points[rank]
        else:
            self.points = 0

    # just a way to print cards out for easy debug, don't expect to actually use this for anything
    def __str__(self) -> str:
        return self.rank + "_" + self.suit
    
    def __repr__(self) -> str:
        return self.rank + "_" + self.suit

    def __hash__(self):
        return hash((self.rank, self.suit))
